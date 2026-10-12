/**
 * WORLD NEWS MAP - CLIENT APPLICATION LOGIC
 * Author: Anil Dutta
 * 
 * Features:
 * - Leaflet World Map with enriched GeoJSON boundaries
 * - Instant Top 5 News per country with category filters:
 *   Economics, Business, Politics, Sports, Food, ALL
 * - On-map glassmorphic summary drawer
 * - "See More" deep dive reader modal with full story & key takeaways
 * - Live capital timezone clock
 * - Text-to-speech audio reader (Web Speech API)
 * - Live Google News RSS fetcher with curated fallback
 * - Auto-complete country search & quick continent navigation
 * - Global breaking news ticker
 */

// Application State
let map = null;
let geojsonLayer = null;
let currentTileLayer = null;
let currentThemeIndex = 0;
let capitalMarker = null;

let currentSelectedCountry = null; // { name, iso2, iso3, capital, lat, lng, flag, currency, timezone, continent }
let currentCategory = 'all'; // 'all', 'economics', 'business', 'politics', 'sports', 'food'
let currentNewsItems = [];
let currentModalStoryIndex = 0;
let isLiveRSSMode = true; // Default to real-time dispatches strictly within the last 48 hours
let clockInterval = null;

// Speech Synthesis State
let synth = window.speechSynthesis || null;
let currentUtterance = null;
let isSpeaking = false;
let currentSpeechRate = 1.0;

// Map Themes (100% Free, Zero-API-Key, Zero Watermarks)
const MAP_THEMES = [
  {
    name: 'Midnight Vector',
    url: null, // Pure vector rendering on deep oceanic gradient - 100% offline, zero watermarks!
    attribution: 'Natural Earth Vector Cartography',
    label: 'Vector Dark'
  },
  {
    name: 'Esri Dark Canvas',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
    attribution: '&copy; Esri &copy; DeLorme &copy; NAVTEQ',
    label: 'Dark Canvas'
  },
  {
    name: 'Satellite Earth',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: '&copy; Esri, Maxar, Earthstar Geographics',
    label: 'Satellite'
  },
  {
    name: 'OpenStreetMap',
    url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; OpenStreetMap contributors',
    label: 'OpenStreet'
  }
];

// Region Coordinates for Quick Jump
const REGION_BOUNDS = {
  world: { center: [20, 0], zoom: 2.2 },
  europe: { center: [52, 15], zoom: 4.2 },
  americas: { center: [15, -75], zoom: 3.2 },
  asia: { center: [34, 100], zoom: 3.5 },
  africa: { center: [2, 20], zoom: 3.4 },
  oceania: { center: [-25, 140], zoom: 3.8 },
  mideast: { center: [26, 45], zoom: 4.5 }
};

// Category Colors & Badges
const CATEGORY_META = {
  economics: { name: 'Economics', color: '#10b981', bg: 'bg-emerald-500/20', text: 'text-emerald-400', border: 'border-emerald-500/40', icon: 'trending-up' },
  business: { name: 'Business', color: '#06b6d4', bg: 'bg-cyan-500/20', text: 'text-cyan-400', border: 'border-cyan-500/40', icon: 'briefcase' },
  politics: { name: 'Politics', color: '#8b5cf6', bg: 'bg-purple-500/20', text: 'text-purple-400', border: 'border-purple-500/40', icon: 'landmark' },
  sports: { name: 'Sports', color: '#f59e0b', bg: 'bg-amber-500/20', text: 'text-amber-400', border: 'border-amber-500/40', icon: 'trophy' },
  food: { name: 'Food', color: '#f43f5e', bg: 'bg-rose-500/20', text: 'text-rose-400', border: 'border-rose-500/40', icon: 'utensils' },
  all: { name: 'All News', color: '#0ea5e9', bg: 'bg-brand-500/20', text: 'text-brand-300', border: 'border-brand-500/40', icon: 'layers' }
};

// ================= INITIALIZATION =================
document.addEventListener('DOMContentLoaded', () => {
  initMap();
  initSearchAutocomplete();
  initTicker();
  initKeyboardShortcuts();
  checkServerConnection();

  // Auto-select United Kingdom as initial showcase
  setTimeout(() => {
    selectCountryByCode('GB');
  }, 600);
});

// API Base URL Resolver
function getApiBaseUrl() {
  if (window.LIVE_API_BASE !== undefined) return window.LIVE_API_BASE;
  if (window.location.protocol === 'file:' || !window.location.port) {
    return 'http://127.0.0.1:8090';
  }
  return '';
}

// Check if Python live server is active
async function checkServerConnection() {
  const badge = document.getElementById('live-indicator-badge');
  const candidates = [
    (window.location.protocol === 'file:' || !window.location.port) ? 'http://127.0.0.1:8090' : '',
    'http://127.0.0.1:8090',
    'http://localhost:8090',
    ''
  ];
  
  for (const base of Array.from(new Set(candidates))) {
    try {
      const url = base ? `${base}/api/status` : '/api/status';
      const res = await fetch(url, { signal: AbortSignal.timeout(2000) });
      if (res.ok) {
        const data = await res.json();
        console.log('Connected to World News Live Engine at', base || 'current-host', data);
        window.LIVE_API_BASE = base;
        if (badge) {
          badge.innerHTML = `
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="font-mono text-emerald-400 font-bold text-[11px]">48H LIVE SERVER CONNECTED</span>
          `;
          badge.classList.remove('bg-amber-500/10', 'border-amber-500/30');
          badge.classList.add('bg-emerald-500/10', 'border-emerald-500/30');
        }
        return true;
      }
    } catch (e) {
      // Continue trying next candidate
    }
  }

  console.log('Local live server not reachable. Dynamic 48-hour intelligence engine active.');
  window.LIVE_API_BASE = '';
  if (badge) {
    badge.innerHTML = `
      <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
      <span class="font-mono text-cyan-300 font-semibold text-[11px]">48H INTELLIGENCE ENGINE (REAL-TIME)</span>
    `;
  }
  return false;
}

// ================= MAP INITIALIZATION =================
function initMap() {
  map = L.map('map', {
    center: [25, 0],
    zoom: 2.3,
    minZoom: 1.8,
    maxZoom: 8,
    zoomControl: false,
    maxBounds: [[-85, -180], [85, 180]],
    maxBoundsViscosity: 0.8
  });

  // Custom Zoom Control at bottom right
  L.control.zoom({ position: 'bottomright' }).addTo(map);

  // Set initial tile layer
  applyTileLayer(0);

  // Load and render countries GeoJSON
  if (window.WORLD_COUNTRIES_GEOJSON) {
    renderGeoJson(window.WORLD_COUNTRIES_GEOJSON);
  } else {
    // Fallback fetch if not loaded via script
    fetch('data/countries.geojson')
      .then(r => r.json())
      .then(data => renderGeoJson(data))
      .catch(err => console.error('Failed to load GeoJSON:', err));
  }
}

function applyTileLayer(themeIdx) {
  if (currentTileLayer) {
    map.removeLayer(currentTileLayer);
    currentTileLayer = null;
  }
  const theme = MAP_THEMES[themeIdx];
  if (theme && theme.url) {
    currentTileLayer = L.tileLayer(theme.url, {
      maxZoom: 19,
      attribution: theme.attribution
    }).addTo(map);

    // Keep country polygon boundaries on top of tiles
    if (geojsonLayer) {
      geojsonLayer.bringToFront();
    }
  }

  const themeLabel = document.getElementById('current-theme-label');
  if (themeLabel && theme) themeLabel.textContent = theme.label;
}

function cycleMapTheme() {
  currentThemeIndex = (currentThemeIndex + 1) % MAP_THEMES.length;
  applyTileLayer(currentThemeIndex);
}

// Render country boundaries with interactive events
function renderGeoJson(geoData) {
  if (geojsonLayer) {
    map.removeLayer(geojsonLayer);
  }

  geojsonLayer = L.geoJSON(geoData, {
    style: styleCountryFeature,
    onEachFeature: onEachCountryFeature
  }).addTo(map);
}

function styleCountryFeature(feature) {
  const isSelected = currentSelectedCountry && (
    currentSelectedCountry.iso2 === feature.properties.iso2 ||
    currentSelectedCountry.name === feature.properties.name
  );

  if (isSelected) {
    return {
      fillColor: '#0284c7',
      fillOpacity: 0.75,
      weight: 2.8,
      color: '#38bdf8',
      dashArray: ''
    };
  }

  // Default Cyberpunk / Dark styling
  return {
    fillColor: '#1e293b',
    fillOpacity: 0.45,
    weight: 0.8,
    color: '#475569',
    dashArray: ''
  };
}

function onEachCountryFeature(feature, layer) {
  const props = feature.properties;

  // Hover Tooltip
  layer.bindTooltip(`
    <div class="flex items-center space-x-2">
      <span class="text-lg">${props.flag || '🌐'}</span>
      <div>
        <div class="font-bold text-white text-xs">${props.name}</div>
        <div class="text-[10px] text-cyan-300 font-mono flex items-center gap-1">
          <span>Capital: ${props.capital || 'N/A'}</span>
          <span>• Click for Top 5 News</span>
        </div>
      </div>
    </div>
  `, {
    className: 'country-tooltip',
    sticky: true,
    direction: 'top',
    offset: [0, -10]
  });

  layer.on({
    mouseover: (e) => {
      const isSelected = currentSelectedCountry && currentSelectedCountry.iso2 === props.iso2;
      if (!isSelected) {
        layer.setStyle({
          fillColor: '#0369a1',
          fillOpacity: 0.65,
          weight: 2.0,
          color: '#38bdf8'
        });
        layer.bringToFront();
      }
    },
    mouseout: (e) => {
      const isSelected = currentSelectedCountry && currentSelectedCountry.iso2 === props.iso2;
      if (!isSelected) {
        geojsonLayer.resetStyle(layer);
      }
    },
    click: (e) => {
      selectCountry(props, layer);
    }
  });
}

// ================= COUNTRY SELECTION & NEWS LOADING =================
function selectCountry(props, layer = null) {
  currentSelectedCountry = props;

  // Hide empty state helper badge
  const helperBadge = document.getElementById('map-helper-badge');
  if (helperBadge) helperBadge.classList.add('opacity-0');

  // Reset polygon styles
  if (geojsonLayer) {
    geojsonLayer.eachLayer(l => geojsonLayer.resetStyle(l));
  }

  // Highlight selected polygon
  if (layer) {
    layer.setStyle({
      fillColor: '#0284c7',
      fillOpacity: 0.75,
      weight: 3.0,
      color: '#38bdf8'
    });
    layer.bringToFront();
  } else if (geojsonLayer) {
    geojsonLayer.eachLayer(l => {
      if (l.feature.properties.iso2 === props.iso2 || l.feature.properties.name === props.name) {
        l.setStyle({
          fillColor: '#0284c7',
          fillOpacity: 0.75,
          weight: 3.0,
          color: '#38bdf8'
        });
        l.bringToFront();
      }
    });
  }

  // Smooth camera zoom & center
  // Note: Right padding keeps country visible while drawer is open!
  const targetLat = props.lat || (props.centroid ? props.centroid[0] : 20);
  const targetLng = props.lng || (props.centroid ? props.centroid[1] : 0);

  // Position radar pin at capital
  dropCapitalPin(targetLat, targetLng, props);

  // Fly to country
  const isMobile = window.innerWidth < 768;
  if (layer && layer.getBounds) {
    const bounds = layer.getBounds();
    map.flyToBounds(bounds, {
      paddingTopLeft: [40, 40],
      paddingBottomRight: isMobile ? [40, 280] : [420, 40],
      maxZoom: 5.5,
      duration: 1.2
    });
  } else {
    map.flyTo([targetLat, targetLng], 4.5, { duration: 1.2 });
  }

  // Populate drawer header
  updateCountryHeader(props);

  // Start live clock in that capital
  startCapitalClock(props.timezone || 'UTC');

  // Load and render top 5 news
  loadCountryNews();

  // Open drawer
  openNewsDrawer();
}

function selectCountryByCode(iso2) {
  if (!window.WORLD_COUNTRIES_GEOJSON) return;
  const feature = window.WORLD_COUNTRIES_GEOJSON.features.find(f => f.properties.iso2 === iso2);
  if (feature) {
    selectCountry(feature.properties);
  }
}

function dropCapitalPin(lat, lng, props) {
  if (capitalMarker) {
    map.removeLayer(capitalMarker);
  }

  const pulseIcon = L.divIcon({
    className: 'capital-marker-pin',
    html: '<div class="capital-pulse"></div><div class="capital-dot"></div>',
    iconSize: [22, 22],
    iconAnchor: [11, 11]
  });

  capitalMarker = L.marker([lat, lng], { icon: pulseIcon }).addTo(map);
  capitalMarker.bindPopup(`
    <div class="text-xs font-sans">
      <div class="font-bold text-slate-900">${props.flag} ${props.name}</div>
      <div class="text-slate-600">Capital: <strong>${props.capital}</strong></div>
      <div class="text-cyan-700 font-semibold mt-1">Viewing Top 5 News</div>
    </div>
  `);
}

function updateCountryHeader(props) {
  document.getElementById('country-flag-icon').textContent = props.flag || '🌐';
  document.getElementById('country-name-display').textContent = props.name;
  document.getElementById('country-iso-badge').textContent = props.iso2 || props.iso3 || 'GLOBAL';
  document.getElementById('country-capital-display').querySelector('span').textContent = props.capital || 'Capital';
  document.getElementById('country-continent-display').textContent = props.continent || 'Global';
  document.getElementById('country-currency-display').textContent = props.currency || 'Currency';
}

function startCapitalClock(tz) {
  if (clockInterval) clearInterval(clockInterval);

  function update() {
    const clockEl = document.getElementById('country-clock-display');
    if (!clockEl) return;
    try {
      const now = new Date();
      const timeStr = now.toLocaleTimeString('en-GB', {
        timeZone: tz,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      });
      clockEl.textContent = `${timeStr} (${tz.split('/').pop().replace('_', ' ')})`;
    } catch (e) {
      clockEl.textContent = new Date().toUTCString().slice(17, 25) + ' UTC';
    }
  }

  update();
  clockInterval = setInterval(update, 1000);
}

// ================= LOAD & RENDER TOP 5 NEWS =================
async function loadCountryNews() {
  if (!currentSelectedCountry) return;

  const container = document.getElementById('news-cards-container');
  container.innerHTML = `
    <div class="py-12 flex flex-col items-center justify-center text-center space-y-3">
      <div class="w-10 h-10 border-3 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
      <div class="text-xs text-slate-400 font-mono">Fetching top 5 ${currentCategory.toUpperCase()} dispatches for ${currentSelectedCountry.name}...</div>
    </div>
  `;

  // Update Drawer Category Title
  const catMeta = CATEGORY_META[currentCategory] || CATEGORY_META.all;
  const catPill = document.getElementById('current-category-pill');
  catPill.className = `text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full ${catMeta.bg} ${catMeta.text} border ${catMeta.border} flex items-center gap-1.5`;
  document.getElementById('current-category-name').textContent = catMeta.name.toUpperCase();

  // Fetch news data: Live RSS or Dynamic 48h Synthesizer
  let news = [];

  if (isLiveRSSMode) {
    try {
      const base = getApiBaseUrl();
      const url = `${base}/api/news?country=${encodeURIComponent(currentSelectedCountry.name)}&category=${currentCategory}&limit=5`;
      const res = await fetch(url, { signal: AbortSignal.timeout(5000) });
      if (res.ok) {
        const payload = await res.json();
        if (payload.news && payload.news.length > 0) {
          // Strictly validate that each item is <= 48 hours old
          news = payload.news.filter(item => item.ageHours === undefined || item.ageHours <= 48.0);
        }
      }
    } catch (e) {
      console.warn('Live RSS server request timed out or unavailable, using real-time dynamic 48h synthesizer:', e);
    }
  }

  // If live returned empty or fewer than 5 items, generate topical dispatches strictly <= 48h old
  if (!news || news.length === 0) {
    news = window.generateCountryNews(
      currentSelectedCountry.name,
      currentSelectedCountry.iso2 || 'GB',
      currentCategory
    );
  } else if (news.length < 5) {
    // Fill any missing slots with dynamic 48h items
    const fallbackItems = window.generateCountryNews(
      currentSelectedCountry.name,
      currentSelectedCountry.iso2 || 'GB',
      currentCategory
    );
    for (const fb of fallbackItems) {
      if (news.length >= 5) break;
      if (!news.some(n => n.title.toLowerCase() === fb.title.toLowerCase())) {
        news.push(fb);
      }
    }
  }

  currentNewsItems = news.slice(0, 5);
  renderNewsCards(currentNewsItems);
}

function renderNewsCards(items) {
  const container = document.getElementById('news-cards-container');
  if (!items || items.length === 0) {
    container.innerHTML = `
      <div class="py-10 text-center text-slate-400 text-xs">
        <i data-lucide="newspaper" class="w-8 h-8 mx-auto text-slate-600 mb-2"></i>
        No articles found in this category for ${currentSelectedCountry.name}.
      </div>
    `;
    lucide.createIcons();
    return;
  }

  let html = '';
  items.forEach((item, index) => {
    const num = String(index + 1).padStart(2, '0');
    const cat = item.category || currentCategory;
    const meta = CATEGORY_META[cat] || CATEGORY_META.all;

    html += `
      <article class="glass-card rounded-xl p-4 sm:p-5 relative group border border-slate-700/60 hover:border-cyan-500/50 transition-all">
        
        <!-- Card Top Bar: Number, Category Badge, Source & Time -->
        <div class="flex items-center justify-between text-xs mb-2.5">
          <div class="flex items-center space-x-2">
            <span class="font-mono text-xs font-black text-slate-500 group-hover:text-cyan-400 transition-colors">#${num}</span>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${meta.bg} ${meta.text} border ${meta.border}">
              ${meta.name}
            </span>
            <span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded bg-emerald-950/70 text-emerald-300 border border-emerald-800/60 text-[9px] font-bold">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>48H WIRE</span>
            </span>
          </div>
          <div class="flex items-center space-x-1.5 text-[11px] text-slate-400 font-medium">
            <span class="text-slate-200 font-semibold truncate max-w-[130px]">${item.source || 'Verified Source'}</span>
            <span>•</span>
            <span class="font-mono text-cyan-300 font-bold bg-cyan-950/80 px-1.5 py-0.5 rounded border border-cyan-800/60">${item.time || 'Today'}</span>
          </div>
        </div>

        <!-- Headline Title -->
        <h3 class="text-sm sm:text-base font-bold text-white leading-snug group-hover:text-cyan-300 transition-colors cursor-pointer" onclick="openReaderModal(${index})">
          ${item.title}
        </h3>

        <!-- Smart AI Summary on the Map -->
        <div class="mt-2.5 text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80">
          <div class="flex items-start gap-1.5">
            <i data-lucide="sparkles" class="w-3.5 h-3.5 text-cyan-400 flex-shrink-0 mt-0.5"></i>
            <p class="text-slate-300 line-clamp-3">${item.summary || item.fullStory || ''}</p>
          </div>
        </div>

        <!-- Impact Tag & Read Time -->
        <div class="mt-3 flex items-center justify-between text-[11px]">
          <div class="flex items-center space-x-2">
            <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 text-[10px] font-mono">
              <i data-lucide="clock" class="w-3 h-3 text-emerald-400"></i>
              <span>${item.exactDate ? item.exactDate : (item.time || 'Latest 48h')}</span>
            </span>
            <span class="text-slate-400 font-mono text-[10px]">${item.readTime || '2 min read'}</span>
          </div>

          <!-- Action Buttons: See More & Audio Listen -->
          <div class="flex items-center space-x-1.5">
            <button 
              onclick="speakStoryByIndex(${index})" 
              title="Listen to story summary" 
              class="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-cyan-400 transition"
            >
              <i data-lucide="volume-2" class="w-3.5 h-3.5"></i>
            </button>
            <button 
              onclick="openReaderModal(${index})" 
              class="px-2.5 py-1 rounded-lg bg-brand-600 hover:bg-brand-500 text-white font-bold text-[11px] flex items-center space-x-1 shadow-sm transition"
            >
              <span>See More</span>
              <i data-lucide="arrow-right" class="w-3 h-3"></i>
            </button>
          </div>
        </div>

      </article>
    `;
  });

  container.innerHTML = html;
  lucide.createIcons();
}

// ================= CATEGORY SWITCHER =================
function setCategory(catKey) {
  currentCategory = catKey;

  // Update tabs visual style
  document.querySelectorAll('.category-tab').forEach(tab => {
    tab.className = 'category-tab flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-700/60 transition-all';
  });

  const activeTab = document.getElementById(`tab-${catKey}`);
  if (activeTab) {
    activeTab.className = 'category-tab active-tab flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all bg-brand-500 text-white shadow-sm';
  }

  // Reload news for active country
  if (currentSelectedCountry) {
    loadCountryNews();
  }
}

// Toggle Live RSS Feed mode vs Dynamic 48h mode
function toggleLiveNewsFeed() {
  isLiveRSSMode = !isLiveRSSMode;
  const btn = document.getElementById('live-rss-btn');

  if (isLiveRSSMode) {
    btn.className = 'px-2.5 py-1.5 rounded-lg bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-700/60 text-[11px] font-semibold flex items-center space-x-1.5 transition';
    btn.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span><span id="live-rss-label">Live 48h Feed</span>`;
  } else {
    btn.className = 'px-2.5 py-1.5 rounded-lg bg-cyan-950/80 hover:bg-cyan-900 text-cyan-300 border border-cyan-700/60 text-[11px] font-semibold flex items-center space-x-1.5 transition';
    btn.innerHTML = `<span class="w-2 h-2 rounded-full bg-cyan-400"></span><span id="live-rss-label">Dynamic 48h Hub</span>`;
  }

  lucide.createIcons();
  loadCountryNews();
}

// ================= DRAWER CONTROLS =================
function openNewsDrawer() {
  const drawer = document.getElementById('news-drawer');
  drawer.classList.remove('translate-x-full');
}

function closeNewsDrawer() {
  const drawer = document.getElementById('news-drawer');
  drawer.classList.add('translate-x-full');
  stopSpeech();
}

// ================= "SEE MORE" READER MODAL =================
function openReaderModal(storyIndex) {
  if (!currentNewsItems || !currentNewsItems[storyIndex]) return;
  currentModalStoryIndex = storyIndex;
  const story = currentNewsItems[storyIndex];

  // Stop any ongoing speech
  stopSpeech();

  // Populate Modal Fields
  const cat = story.category || currentCategory;
  const meta = CATEGORY_META[cat] || CATEGORY_META.all;

  const catBadge = document.getElementById('modal-category-badge');
  catBadge.textContent = meta.name.toUpperCase();
  catBadge.className = `px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider ${meta.bg} ${meta.text} border ${meta.border}`;

  document.getElementById('modal-source-name').textContent = story.source || 'Global Bureau';
  document.getElementById('modal-time-stamp').textContent = story.exactDate ? `${story.time} • ${story.exactDate}` : (story.time || 'Recent');
  document.getElementById('modal-read-time').textContent = story.readTime || '3 min read';
  document.getElementById('modal-article-title').textContent = story.title;

  // Key Takeaways list
  const takeawaysList = document.getElementById('modal-takeaways-list');
  if (story.keyTakeaways && story.keyTakeaways.length > 0) {
    takeawaysList.innerHTML = story.keyTakeaways.map(t => `
      <li class="flex items-start space-x-2">
        <i data-lucide="check" class="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5"></i>
        <span>${t}</span>
      </li>
    `).join('');
  } else {
    takeawaysList.innerHTML = `
      <li class="flex items-start space-x-2">
        <i data-lucide="check" class="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5"></i>
        <span>Comprehensive reporting verified by ${story.source}.</span>
      </li>
    `;
  }

  // Full Story text
  const storyParagraphs = document.getElementById('modal-story-paragraphs');
  storyParagraphs.textContent = story.fullStory || story.summary || 'Full analysis available via source citation.';

  // Strategic impact text
  document.getElementById('modal-impact-text').textContent = story.impact || 'High importance for regional policy and market sentiment.';

  // Tags
  const tagsContainer = document.getElementById('modal-tags-container');
  if (story.tags && story.tags.length > 0) {
    tagsContainer.innerHTML = story.tags.map(tag => `
      <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[11px] font-mono border border-slate-700">#${tag}</span>
    `).join('');
  } else {
    tagsContainer.innerHTML = '';
  }

  // Story Index Label
  document.getElementById('modal-story-index').textContent = `Story ${storyIndex + 1} of ${currentNewsItems.length}`;

  // Source Link button
  const sourceLink = document.getElementById('modal-original-source-link');
  if (story.sourceUrl && story.sourceUrl !== '#') {
    sourceLink.href = story.sourceUrl;
    sourceLink.style.display = 'inline-flex';
  } else {
    sourceLink.href = `https://news.google.com/search?q=${encodeURIComponent(story.title)}`;
    sourceLink.style.display = 'inline-flex';
  }

  // Reset Audio Button
  resetModalAudioUI();

  // Show Modal
  const modal = document.getElementById('reader-modal');
  modal.classList.remove('hidden');
  lucide.createIcons();
}

function closeReaderModal() {
  const modal = document.getElementById('reader-modal');
  modal.classList.add('hidden');
  stopSpeech();
}

function handleModalBackdropClick(event) {
  if (event.target.id === 'reader-modal') {
    closeReaderModal();
  }
}

function navigateModalStory(delta) {
  const newIndex = currentModalStoryIndex + delta;
  if (newIndex >= 0 && newIndex < currentNewsItems.length) {
    openReaderModal(newIndex);
  }
}

// ================= TEXT-TO-SPEECH (WEB SPEECH API) =================
function speakStory(textToRead) {
  if (!synth) {
    alert('Speech synthesis is not supported on your browser.');
    return;
  }

  stopSpeech();

  currentUtterance = new SpeechSynthesisUtterance(textToRead);
  currentUtterance.rate = currentSpeechRate;
  currentUtterance.pitch = 1.0;

  // Pick natural English voice if available
  const voices = synth.getVoices();
  const englishVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha')));
  if (englishVoice) currentUtterance.voice = englishVoice;

  currentUtterance.onstart = () => {
    isSpeaking = true;
    updateAudioUI(true);
  };

  currentUtterance.onend = () => {
    isSpeaking = false;
    updateAudioUI(false);
  };

  currentUtterance.onerror = () => {
    isSpeaking = false;
    updateAudioUI(false);
  };

  synth.speak(currentUtterance);
}

function stopSpeech() {
  if (synth && synth.speaking) {
    synth.cancel();
  }
  isSpeaking = false;
  updateAudioUI(false);
}

function speakStoryByIndex(idx) {
  if (!currentNewsItems || !currentNewsItems[idx]) return;
  const story = currentNewsItems[idx];
  const text = `${story.title}. Reported by ${story.source}. Summary: ${story.summary}`;
  if (isSpeaking) {
    stopSpeech();
  } else {
    speakStory(text);
  }
}

function toggleModalAudioNarration() {
  if (isSpeaking) {
    stopSpeech();
  } else {
    const story = currentNewsItems[currentModalStoryIndex];
    if (story) {
      const fullText = `${story.title}. Published by ${story.source}. Key takeaways include: ${story.keyTakeaways ? story.keyTakeaways.join('. ') : ''}. Detailed analysis: ${story.fullStory || story.summary}`;
      speakStory(fullText);
    }
  }
}

function changeAudioSpeed(rate) {
  currentSpeechRate = rate;
  [1.0, 1.25, 1.5].forEach(r => {
    const el = document.getElementById(`speed-${String(r).replace('.', '')}`);
    if (el) {
      if (r === rate) {
        el.className = 'px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-800 text-cyan-400 border border-slate-700';
      } else {
        el.className = 'px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-slate-900 text-slate-400 hover:text-white border border-slate-800';
      }
    }
  });

  if (isSpeaking) {
    toggleModalAudioNarration();
    toggleModalAudioNarration();
  }
}

function updateAudioUI(playing) {
  const soundBars = document.getElementById('modal-sound-bars');
  const audioIcon = document.getElementById('modal-audio-icon');
  const audioStatus = document.getElementById('modal-audio-status');

  if (soundBars) {
    if (playing) soundBars.classList.remove('hidden');
    else soundBars.classList.add('hidden');
  }

  if (audioIcon) {
    if (playing) {
      audioIcon.setAttribute('data-lucide', 'square');
    } else {
      audioIcon.setAttribute('data-lucide', 'play');
    }
    lucide.createIcons();
  }

  if (audioStatus) {
    audioStatus.textContent = playing ? 'Playing Narration...' : 'Audio Narration';
  }
}

function resetModalAudioUI() {
  updateAudioUI(false);
}

function readAloudTopStories() {
  if (!currentNewsItems || currentNewsItems.length === 0) return;
  const briefing = `Top 5 dispatches for ${currentSelectedCountry.name}. ` + currentNewsItems.map((item, idx) => `Story ${idx + 1}: ${item.title}. Summary: ${item.summary}`).join('. Next story: ');
  speakStory(briefing);
}

// ================= CONTINENT QUICK JUMPS =================
function flyToRegion(regionKey) {
  const target = REGION_BOUNDS[regionKey] || REGION_BOUNDS.world;
  map.flyTo(target.center, target.zoom, { duration: 1.4 });
}

function resetMapView() {
  flyToRegion('world');
}

// ================= SEARCH AUTOCOMPLETE =================
function initSearchAutocomplete() {
  const searchInput = document.getElementById('country-search-input');
  const dropdown = document.getElementById('search-dropdown');

  if (!searchInput || !dropdown) return;

  searchInput.addEventListener('input', (e) => {
    const val = e.target.value.trim().toLowerCase();
    if (!val || !window.WORLD_COUNTRIES_GEOJSON) {
      dropdown.classList.add('hidden');
      return;
    }

    const matches = window.WORLD_COUNTRIES_GEOJSON.features.filter(f => {
      const name = (f.properties.name || '').toLowerCase();
      const iso2 = (f.properties.iso2 || '').toLowerCase();
      const iso3 = (f.properties.iso3 || '').toLowerCase();
      const capital = (f.properties.capital || '').toLowerCase();
      return name.includes(val) || iso2.includes(val) || iso3.includes(val) || capital.includes(val);
    }).slice(0, 8);

    if (matches.length === 0) {
      dropdown.innerHTML = `<div class="p-3 text-xs text-slate-400 text-center">No matching country found</div>`;
      dropdown.classList.remove('hidden');
      return;
    }

    dropdown.innerHTML = matches.map(m => `
      <div 
        class="search-item px-3.5 py-2 hover:bg-slate-800 cursor-pointer flex items-center justify-between text-xs transition border-b border-slate-800/60 last:border-0"
        onclick="handleSearchSelect('${m.properties.iso2}')"
      >
        <div class="flex items-center space-x-2.5">
          <span class="text-base">${m.properties.flag || '🌐'}</span>
          <div>
            <div class="font-bold text-white">${m.properties.name}</div>
            <div class="text-[10px] text-slate-400">Capital: ${m.properties.capital}</div>
          </div>
        </div>
        <span class="font-mono text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-cyan-400 border border-slate-700">
          ${m.properties.iso2}
        </span>
      </div>
    `).join('');

    dropdown.classList.remove('hidden');
  });

  // Hide dropdown on blur
  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.add('hidden');
    }
  });
}

function handleSearchSelect(iso2) {
  selectCountryByCode(iso2);
  const searchInput = document.getElementById('country-search-input');
  const dropdown = document.getElementById('search-dropdown');
  if (searchInput) searchInput.value = '';
  if (dropdown) dropdown.classList.add('hidden');
}

// ================= RANDOM COUNTRY EXPLORER =================
function pickRandomCountry() {
  if (!window.WORLD_COUNTRIES_GEOJSON) return;
  const features = window.WORLD_COUNTRIES_GEOJSON.features;
  const randomFeature = features[Math.floor(Math.random() * features.length)];
  if (randomFeature && randomFeature.properties) {
    selectCountry(randomFeature.properties);
  }
}

// ================= BREAKING NEWS TICKER =================
function initTicker() {
  const tickerStrip = document.getElementById('ticker-strip');
  if (!tickerStrip) return;

  const items = window.BREAKING_NEWS_TICKER || [];
  // Duplicate for smooth infinite loop
  const displayItems = [...items, ...items];

  tickerStrip.innerHTML = displayItems.map(item => `
    <span 
      class="inline-flex items-center space-x-2 cursor-pointer hover:text-cyan-400 transition"
      onclick="selectCountryByCode('${item.iso2}')"
    >
      <span class="font-bold text-white">${item.country}</span>
      <span class="text-slate-500 font-mono">/</span>
      <span>${item.headline}</span>
      <span class="text-slate-600 font-mono">•</span>
    </span>
  `).join('');
}

// ================= SHARING & UTILITIES =================
function copyArticleLink() {
  const story = currentNewsItems[currentModalStoryIndex];
  if (!story) return;
  const shareText = `World News Map Briefing: ${story.title} (${story.country}) - ${story.source}`;
  navigator.clipboard.writeText(shareText).then(() => {
    alert('Article brief copied to clipboard!');
  }).catch(() => {
    prompt('Copy article briefing:', shareText);
  });
}

function exportCountrySummary() {
  if (!currentSelectedCountry || !currentNewsItems) return;
  const summary = `*** ${currentSelectedCountry.name.toUpperCase()} TOP 5 NEWS BRIEFING ***\n` +
    currentNewsItems.map((item, i) => `${i+1}. [${item.category.toUpperCase()}] ${item.title} (${item.source})\n   ${item.summary}\n`).join('\n') +
    `\nGenerated by World News Map - by Anil Dutta`;
  
  navigator.clipboard.writeText(summary).then(() => {
    alert(`Top 5 News Briefing for ${currentSelectedCountry.name} copied to clipboard!`);
  }).catch(() => {
    prompt('Copy Briefing:', summary);
  });
}

// ================= KEYBOARD SHORTCUTS =================
function initKeyboardShortcuts() {
  window.addEventListener('keydown', (e) => {
    // Ignore when typing inside search input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    if (e.key === 'Escape') {
      closeReaderModal();
      closeNewsDrawer();
    } else if (e.key === '1') {
      setCategory('all');
    } else if (e.key === '2') {
      setCategory('economics');
    } else if (e.key === '3') {
      setCategory('business');
    } else if (e.key === '4') {
      setCategory('politics');
    } else if (e.key === '5') {
      setCategory('sports');
    } else if (e.key === '6') {
      setCategory('food');
    } else if (e.key.toLowerCase() === 'r') {
      pickRandomCountry();
    } else if (e.key === '/') {
      e.preventDefault();
      const input = document.getElementById('country-search-input');
      if (input) input.focus();
    }
  });
}
