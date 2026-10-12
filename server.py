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

# In-memory RSS cache: key -> {"timestamp": float, "data": list}
RSS_CACHE = {}
CACHE_TTL_SECONDS = 900  # 15 minutes

def clean_html_text(raw_html):
    """Strip HTML tags and unescape entities."""
    if not raw_html:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    clean = ' '.join(clean.split())
    # Unescape common entities
    clean = clean.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'").replace('&lt;', '<').replace('&gt;', '>')
    return clean.strip()

def format_relative_time(pub_date_str):
    """Format RFC-822 date to human relative string."""
    try:
        # e.g. 'Mon, 12 Oct 2026 18:34:02 GMT'
        # Parse timezone-agnostic
        dt = datetime.strptime(pub_date_str[:25].strip(), "%a, %d %b %Y %H:%M:%S")
        diff = datetime.now(timezone.utc).replace(tzinfo=None) - dt
        minutes = int(diff.total_seconds() // 60)
        if minutes < 1:
            return "Just now"
        elif minutes < 60:
            return f"{minutes}m ago"
        hours = minutes // 60
        if hours < 24:
            return f"{hours}h ago"
        days = hours // 24
        return f"{days}d ago"
    except Exception:
        return pub_date_str.split(" +")[0] if pub_date_str else "Recent"

def fetch_live_news_rss(country_name, category='all', limit=5):
    """Fetch live news from Google News RSS search feed."""
    cache_key = f"{country_name.lower()}:{category.lower()}:{limit}"
    now = time.time()
    if cache_key in RSS_CACHE:
        entry = RSS_CACHE[cache_key]
        if now - entry["timestamp"] < CACHE_TTL_SECONDS:
            return entry["data"]

    # Category search query builder
    cat_queries = {
        "economics": f'"{country_name}" (economy OR GDP OR inflation OR central bank OR trade OR interest rates)',
        "business": f'"{country_name}" (business OR markets OR tech OR company OR startup OR industry)',
        "politics": f'"{country_name}" (politics OR government OR parliament OR election OR policy OR diplomatic)',
        "sports": f'"{country_name}" (sports OR football OR tournament OR athletics OR cup OR match)',
        "food": f'"{country_name}" (food OR gastronomy OR cuisine OR agriculture OR culinary OR dining)',
        "all": f'"{country_name}" news'
    }

    query = cat_queries.get(category.lower(), f'"{country_name}" news')
    encoded = urllib.parse.quote(query)
    feed_url = f"https://news.google.com/rss/search?q={encoded}&hl=en&gl=US&ceid=US:en"

    items = []
    try:
        req = urllib.request.Request(feed_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=9) as resp:
            xml_data = resp.read()

        root = ET.fromstring(xml_data)
        item_nodes = root.findall('.//item')[:limit]

        for idx, item in enumerate(item_nodes):
            raw_title = item.find('title').text if item.find('title') is not None else 'News Update'
            link = item.find('link').text if item.find('link') is not None else '#'
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            raw_desc = item.find('description').text if item.find('description') is not None else ''
            source_node = item.find('source')
            source = source_node.text if source_node is not None and source_node.text else 'Global News'

            # Clean headline (often includes ' - Source Name' at the end)
            clean_title = raw_title
            if ' - ' in clean_title:
                clean_title = clean_title.rsplit(' - ', 1)[0].strip()

            clean_desc = clean_html_text(raw_desc)
            if not clean_desc or len(clean_desc) < 30:
                clean_desc = f"Latest developments from {country_name}: {clean_title}. Reporting on unfolding events and industry analysis."

            # Generate smart key takeaways
            takeaways = [
                f"Reported directly by {source} with continuous coverage.",
                f"Significant national and international interest regarding {category.capitalize()} in {country_name}.",
                f"Published {format_relative_time(pub_date)} with further updates anticipated."
            ]

            full_story = f"{clean_desc}\n\nAccording to coverage by {source}, this development marks an active phase of developments in {country_name}. Stakeholders and observers are assessing the broader implications across regional and international sectors.\n\nFor ongoing updates, verified analysis, and direct source material, consult the full reporting published by {source}."

            items.append({
                "id": f"live-{category}-{idx+1}",
                "title": clean_title,
                "category": category if category != 'all' else 'general',
                "country": country_name,
                "source": source,
                "sourceUrl": link,
                "time": format_relative_time(pub_date),
                "readTime": "2 min read",
                "impact": f"Live Breaking {category.capitalize()}",
                "sentiment": "neutral",
                "summary": clean_desc,
                "keyTakeaways": takeaways,
                "fullStory": full_story,
                "tags": [country_name, category.upper(), "Live Feed", source]
            })
    except Exception as e:
        print(f"[RSS Warning] Failed to fetch live RSS for '{country_name}' ({category}): {e}")

    if items:
        RSS_CACHE[cache_key] = {"timestamp": now, "data": items}
    return items

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
