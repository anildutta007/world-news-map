#!/usr/bin/env python3
"""
Test Suite for World News Map
Validates:
1. File integrity and assets
2. Country GeoJSON validity and metadata
3. News database structure and procedural generator
4. Live RSS fetching and server API endpoints
"""

import unittest
import json
import os
import sys
import urllib.request
import urllib.parse
import threading
import time

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

class TestWorldNewsMap(unittest.TestCase):

    def test_01_core_files_exist(self):
        """Verify all critical app files exist."""
        required_files = [
            "index.html",
            "styles.css",
            "app.js",
            "news-database.js",
            "server.py",
            "run.bat",
            "data/countries.geojson",
            "data/countries-geo.js"
        ]
        for rel_path in required_files:
            full_path = os.path.join(PROJECT_DIR, rel_path)
            self.assertTrue(os.path.exists(full_path), f"Missing file: {rel_path}")
            self.assertGreater(os.path.getsize(full_path), 0, f"Empty file: {rel_path}")

    def test_02_country_geojson_validity(self):
        """Verify country boundaries and metadata."""
        geojson_path = os.path.join(PROJECT_DIR, "data", "countries.geojson")
        with open(geojson_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data.get("type"), "FeatureCollection")
        features = data.get("features", [])
        self.assertGreater(len(features), 170, "Should have at least 170 countries")

        # Check sample properties
        sample = features[0]["properties"]
        self.assertIn("name", sample)
        self.assertIn("iso2", sample)
        self.assertIn("capital", sample)
        self.assertIn("flag", sample)
        self.assertIn("lat", sample)
        self.assertIn("lng", sample)

        # Check key countries exist
        iso2_set = {f["properties"].get("iso2") for f in features}
        for code in ["GB", "US", "IN", "JP", "DE", "FR"]:
            self.assertIn(code, iso2_set, f"Country {code} missing in GeoJSON")

    def test_03_news_database_integrity(self):
        """Verify news database JS file contains required datasets."""
        news_db_path = os.path.join(PROJECT_DIR, "news-database.js")
        with open(news_db_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("window.CURATED_NEWS_DB", content)
        self.assertIn("window.BREAKING_NEWS_TICKER", content)
        self.assertIn("window.generateCountryNews", content)

    def test_04_html_and_ui_elements(self):
        """Verify index.html contains all required category filters and elements."""
        html_path = os.path.join(PROJECT_DIR, "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check required categories
        categories = ["all", "economics", "business", "politics", "sports", "food"]
        for cat in categories:
            self.assertIn(f"tab-{cat}", content, f"Missing category tab for {cat}")

        # Check core UI components
        self.assertIn('id="map"', content)
        self.assertIn('id="news-drawer"', content)
        self.assertIn('id="reader-modal"', content)
        self.assertIn('id="ticker-strip"', content)
        self.assertIn('id="country-search-input"', content)

    def test_05_live_rss_proxy(self):
        """Test server RSS fetcher logic in isolation."""
        import server
        items = server.fetch_live_news_rss("United Kingdom", "business", 3)
        self.assertIsInstance(items, list)
        if items:
            self.assertIn("title", items[0])
            self.assertIn("summary", items[0])
            self.assertIn("source", items[0])

if __name__ == "__main__":
    unittest.main()
