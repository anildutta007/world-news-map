# 🌍 World News Map - Interactive Global Cartographic Intelligence

An innovative, visually striking web application by **Anil Dutta** that reimagines global news discovery. Explore the planet through a high-precision interactive world map: click on any sovereign nation or territory to instantly reveal its **Top 5 curated and live news briefings** across six distinct topics, complete with executive AI-style summaries, audio read-aloud narration, and in-depth analytical deep dives.

---

## 🌟 Key Features ("News with a Difference")

- **🗺️ Interactive World Cartography**:
  - Centerpiece interactive vector map powered by Leaflet.js and enriched Natural Earth boundaries (190+ sovereign countries).
  - Hover over any country to inspect its name, flag emoji, capital city, and regional identity.
  - Click on any nation to smoothly fly the camera, drop an animated radar pulse on its capital, and open the on-map news drawer.
  - Multi-theme visual cartography: *Midnight Dark* (default), *Cyberpunk Neon*, *Clean Daylight*, and *Satellite Earth*.
  - Quick-jump continent corridors (World, Europe, Americas, Asia, Africa, Oceania, Middle East).
  - Instant auto-complete search for any nation or capital (press `/`).
  - 🎲 *Explore Random Country* shuffle generator (press `R`).

- **📰 Top 5 News per Nation**:
  - Every country reveals exactly **5 top-priority, high-impact stories**.
  - Dynamic topic filtering across:
    - 🌐 **ALL**: Balanced, high-impact overview across national disciplines
    - 📈 **Economics**: Central banks, interest rates, GDP expansion, inflation, currency stability
    - 💼 **Business**: Hyperscale tech, venture funding, industrial corridors, corporate earnings
    - 🏛️ **Politics**: Parliamentary legislation, democratic governance, diplomatic alliances
    - ⚽ **Sports**: National leagues, international tournaments, Grand Slam tennis, Formula 1
    - 🍜 **Food & Gastronomy**: Michelin recognition, artisan agriculture, food tech, culinary heritage

- **⚡ On-Map Executive Summaries**:
  - News cards float directly over the map in a glassmorphic HUD drawer, preserving continuous global geospatial context.
  - Each story features a crisp 2-to-3 sentence executive synopsis designed for rapid skimming.
  - Real-time capital timezone clock and national currency display.

- **📖 "See More" Deep Dive Reader Modal**:
  - Click **"See More"** on any story to open a distraction-free, full analytical briefing.
  - Includes **Executive Takeaways** checkmarks, multi-paragraph in-depth narrative, **Strategic Impact Rating**, and direct links to original verified sources (*Financial Times*, *Reuters*, *Bloomberg*, *BBC*, *The Economist*, etc.).
  - Story flipping controls: seamlessly flip between Story 1 and 5 (`← Prev Story` / `Next Story →`).

- **🔊 Web Speech Audio Narration (TTS)**:
  - Integrated text-to-speech audio player with animated frequency sound bars.
  - Listen to any single article summary or click *"Brief Me"* to hear the full audio briefing for the selected country.
  - Adjustable playback speeds (1.0x, 1.25x, 1.5x).

- **🔄 Dual Engine: Live Google News RSS & Curated Knowledge Hub**:
  - **Live RSS Mode**: One-click toggle connects to Python proxy (`/api/news`) to fetch live, real-time Google News search feeds for any country and category.
  - **Curated Intelligence Base**: High-fidelity offline knowledge database for major economies + procedural topical synthesizer for all 190+ nations worldwide. Zero empty screens anywhere on earth!

- **📡 Global Breaking Ticker**:
  - Animated horizontal dispatch wire along the footer displaying rolling headlines worldwide.
  - Clicking any headline immediately commands the map to fly to that country and load its news!

---

## 🚀 Quick Start Guide

### Option 1: One-Click Launcher (Recommended)
Double-click `run_world_news.bat` located in the root workspace folder:
```cmd
run_world_news.bat
```
This automatically starts `server.py` on `http://localhost:8088` and launches your default web browser.

### Option 2: Running via Python Terminal
```bash
cd world-news-map
py server.py
```

### Option 3: Direct Browser Launch (100% Offline Capable)
Simply double-click `index.html` in your file explorer. All country boundaries (`countries-geo.js`) and news datasets (`news-database.js`) are locally bundled with zero CORS dependencies.

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|---|---|
| `1` | Switch to **ALL** Category |
| `2` | Switch to **Economics** |
| `3` | Switch to **Business** |
| `4` | Switch to **Politics** |
| `5` | Switch to **Sports** |
| `6` | Switch to **Food** |
| `/` | Focus Country Search Input |
| `R` | Explore Random Country |
| `ESC` | Close Reader Modal or News Panel |

---

## 📁 Project Architecture

```
world-news-map/
├── index.html              # Main responsive web interface
├── styles.css              # Glassmorphic UI, animations, radar pulses
├── app.js                  # Map logic, news loading, TTS narration, search
├── server.py               # Local Python HTTP server & live RSS proxy
├── news-database.js        # Curated news database & procedural synthesizer
├── build_country_data.py   # GeoJSON downloader and metadata enricher
├── test_app.py             # Automated test suite
├── run.bat                 # Local project launcher
└── data/
    ├── countries.geojson   # Enriched Natural Earth 110m boundaries
    └── countries-geo.js    # Zero-CORS script-loadable GeoJSON
```

---

## ⚖️ Legal & Educational Notice
Developed by **Anil Dutta** strictly for educational, informational, and simulation purposes. News summaries are compiled from publicly available RSS feeds and journalistic research.
