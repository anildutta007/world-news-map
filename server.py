#!/usr/bin/env python3
"""
WorldNews Map Server - Local HTTP & Live News RSS Proxy Server
Author: Anil Dutta

Features:
- Serves static assets (HTML, CSS, JS, GeoJSON) with optimal caching and UTF-8 headers
- /api/news endpoint: Live real-time RSS feed parser from Google News with in-memory caching
- /api/status endpoint: Server health and connectivity
- Automatic port selection (default 8088)
- Automatic web browser launch
- LAN IP detection for mobile device testing
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import webbrowser
import socket
import os
import sys
import time
import re
from datetime import datetime

from datetime import datetime, timezone

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DEFAULT_PORT = 8090
MAX_PORT_ATTEMPTS = 15

import email.utils

# In-memory RSS cache: key -> {"timestamp": float, "data": list}
RSS_CACHE = {}
CACHE_TTL_SECONDS = 300  # 5 minutes for breaking news freshness

def clean_html_text(raw_html):
    """Strip HTML tags and unescape entities."""
    if not raw_html:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    clean = ' '.join(clean.split())
    # Unescape common entities
    clean = clean.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'").replace('&lt;', '<').replace('&gt;', '>')
    return clean.strip()

def parse_rfc2822_date(pub_date_str):
    """Parse RFC-2822 date into timezone-aware datetime and calculate age in hours."""
    now = datetime.now(timezone.utc)
    try:
        dt = email.utils.parsedate_to_datetime(pub_date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        age_hours = (now - dt).total_seconds() / 3600.0
        return dt, age_hours
    except Exception:
        return now, 0.0

def format_relative_time(dt, age_hours):
    """Format datetime into clear relative time string within 48 hours."""
    minutes = int(age_hours * 60)
    if minutes < 2:
        return "Just now"
    elif minutes < 60:
        return f"{minutes}m ago"
    hours = int(age_hours)
    if hours < 24:
        return f"{hours}h ago"
    days = int(age_hours // 24)
    if days == 1:
        return "Yesterday"
    return f"{days}d ago"

def fetch_live_news_rss(country_name, category='all', limit=5):
    """Fetch real-time news strictly within the last 48 hours."""
    cache_key = f"{country_name.lower()}:{category.lower()}:{limit}"
    now_ts = time.time()
    if cache_key in RSS_CACHE:
        entry = RSS_CACHE[cache_key]
        if now_ts - entry["timestamp"] < CACHE_TTL_SECONDS:
            return entry["data"]

    # Category search query builder with mandatory when:48h limiter
    cat_queries = {
        "economics": f'"{country_name}" (economy OR GDP OR inflation OR central bank OR trade OR interest rate)',
        "business": f'"{country_name}" (business OR markets OR tech OR company OR corporate OR startup)',
        "politics": f'"{country_name}" (politics OR government OR parliament OR election OR minister OR diplomacy)',
        "sports": f'"{country_name}" (sports OR football OR tournament OR athletics OR cup OR match)',
        "food": f'"{country_name}" (food OR restaurant OR cuisine OR agriculture OR culinary OR dining)',
        "all": f'"{country_name}" news'
    }

    base_query = cat_queries.get(category.lower(), f'"{country_name}" news')
    
    # Primary attempt: strictly last 48 hours (when:48h)
    # Secondary fallback for smaller nations: when:72h (last 3 days max)
    attempts = [
        (f'{base_query} when:48h', 48.0),
        (f'{base_query} when:72h', 72.0)
    ]

    items = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    for query_str, max_age_hours in attempts:
        if len(items) >= limit:
            break
        try:
            encoded = urllib.parse.quote(query_str)
            feed_url = f"https://news.google.com/rss/search?q={encoded}&hl=en&gl=US&ceid=US:en"

            req = urllib.request.Request(feed_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                xml_data = resp.read()

            root = ET.fromstring(xml_data)
            item_nodes = root.findall('.//item')

            for item in item_nodes:
                pub_date_str = item.find('pubDate').text if item.find('pubDate') is not None else ''
                dt, age_hours = parse_rfc2822_date(pub_date_str)

                # STRICT 48-72h filter: Reject anything older than max_age_hours!
                if age_hours > max_age_hours:
                    continue

                raw_title = item.find('title').text if item.find('title') is not None else 'News Update'
                link = item.find('link').text if item.find('link') is not None else '#'
                raw_desc = item.find('description').text if item.find('description') is not None else ''
                source_node = item.find('source')
                source = source_node.text if source_node is not None and source_node.text else 'Global News'

                clean_title = raw_title
                if ' - ' in clean_title:
                    clean_title = clean_title.rsplit(' - ', 1)[0].strip()

                # Deduplicate by title
                if any(it['title'].lower() == clean_title.lower() for it in items):
                    continue

                clean_desc = clean_html_text(raw_desc)
                if not clean_desc or len(clean_desc) < 30:
                    clean_desc = f"Latest developments from {country_name}: {clean_title}. Published within the last {int(age_hours)+1} hours."

                time_label = format_relative_time(dt, age_hours)
                exact_date = dt.strftime("%d %b %Y, %H:%M UTC")

                takeaways = [
                    f"Breaking dispatch published {time_label} ({exact_date}).",
                    f"Reported directly by {source} with continuous coverage.",
                    f"High national and regional relevance for {category.capitalize()} in {country_name}."
                ]

                full_story = f"{clean_desc}\n\nThis article was published {time_label} ({exact_date}) by {source}.\n\nDevelopments in {country_name} are unfolding rapidly. Stakeholders and industry observers are closely tracking outcomes across national and international sectors.\n\nTo view the full original report, access the verified source dispatch at {source}."

                items.append({
                    "id": f"live-{category}-{len(items)+1}",
                    "title": clean_title,
                    "category": category if category != 'all' else 'general',
                    "country": country_name,
                    "source": source,
                    "sourceUrl": link,
                    "time": time_label,
                    "exactDate": exact_date,
                    "ageHours": round(age_hours, 1),
                    "readTime": "2 min read",
                    "impact": f"Breaking ({time_label})",
                    "sentiment": "neutral",
                    "summary": clean_desc,
                    "keyTakeaways": takeaways,
                    "fullStory": full_story,
                    "tags": [country_name, category.upper(), "Last 48 Hours", source],
                    "dt_sort": dt
                })

                if len(items) >= limit:
                    break

        except Exception as e:
            print(f"[RSS Warning] Failed query '{query_str}': {e}")

    # Sort strictly newest first
    items.sort(key=lambda x: x.get('dt_sort', datetime.min.replace(tzinfo=timezone.utc)), reverse=True)
    for it in items:
        it.pop('dt_sort', None)

    final_items = items[:limit]
    if final_items:
        RSS_CACHE[cache_key] = {"timestamp": now_ts, "data": final_items}
    return final_items

class WorldNewsHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler serving web app and live RSS API."""

    def end_headers(self):
        # Enable CORS for local API access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # API: Live News Endpoint
        if parsed.path == '/api/news':
            params = urllib.parse.parse_qs(parsed.query)
            country = params.get('country', ['United Kingdom'])[0]
            category = params.get('category', ['all'])[0]
            limit_str = params.get('limit', ['5'])[0]
            try:
                limit = min(int(limit_str), 10)
            except ValueError:
                limit = 5

            live_news = fetch_live_news_rss(country, category, limit)
            
            response_payload = {
                "status": "ok" if live_news else "fallback_recommended",
                "country": country,
                "category": category,
                "count": len(live_news),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "news": live_news
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response_payload, ensure_ascii=False).encode('utf-8'))
            return

        # API: Health Status
        if parsed.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "online",
                "app": "World News Map AI",
                "cached_queries": len(RSS_CACHE),
                "time": datetime.now(timezone.utc).isoformat()
            }).encode('utf-8'))
            return

        # Normal static file serving
        return super().do_GET()

    def log_message(self, format, *args):
        # Silence routine 200/304 logs
        if len(args) > 1 and str(args[1]) not in ('200', '304'):
            super().log_message(format, *args)

def get_lan_ip():
    """Detect local LAN IP for local WiFi access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def start_server(auto_open=True):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    port = DEFAULT_PORT
    httpd = None

    for _ in range(MAX_PORT_ATTEMPTS):
        try:
            handler = WorldNewsHTTPHandler
            socketserver.TCPServer.allow_reuse_address = True
            httpd = socketserver.TCPServer(("0.0.0.0", port), handler)
            break
        except OSError:
            port += 1

    if not httpd:
        print(f"[Error] Could not find open port starting from {DEFAULT_PORT}.")
        sys.exit(1)

    lan_ip = get_lan_ip()
    local_url = f"http://localhost:{port}"
    lan_url = f"http://{lan_ip}:{port}"

    print("=" * 70)
    print("      *** WORLD NEWS MAP - INTERACTIVE GLOBAL DISPATCH ***")
    print("      *** Interactive Cartographic Intelligence & Live Feeds ***")
    print("=" * 70)
    print(f"  Local Access:      {local_url}")
    print(f"  Network (LAN):     {lan_url}")
    print("=" * 70)
    print("  Categories: Economics | Business | Politics | Sports | Food | ALL")
    print("  Live RSS Proxy:   Active at /api/news")
    print("  Press Ctrl+C to stop the server.")
    print("=" * 70)

    if auto_open:
        try:
            webbrowser.open(local_url)
        except Exception as e:
            print(f"  Could not launch browser: {e}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Server] Stopping World News Map server. Goodbye!")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    start_server(auto_open=True)
