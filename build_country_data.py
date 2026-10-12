#!/usr/bin/env python3
"""
Downloads Natural Earth 110m countries GeoJSON and enriches each feature with:
- ISO2 and ISO3 codes
- Flag emoji
- Capital city
- Capital coordinates (lat, lon)
- Primary timezone
- Currency
- Continent / Region
Saves both as:
1. data/countries.geojson
2. data/countries-geo.js (window.WORLD_COUNTRIES_GEOJSON = ...)
"""

import json
import urllib.request
import os
import sys

# Country metadata table for capitals, currencies, and centroids
COUNTRY_METADATA = {
    "GB": {"name": "United Kingdom", "capital": "London", "lat": 51.5074, "lng": -0.1278, "currency": "GBP (£)", "timezone": "Europe/London", "continent": "Europe"},
    "US": {"name": "United States", "capital": "Washington, D.C.", "lat": 38.9072, "lng": -77.0369, "currency": "USD ($)", "timezone": "America/New_York", "continent": "North America"},
    "IN": {"name": "India", "capital": "New Delhi", "lat": 28.6139, "lng": 77.2090, "currency": "INR (₹)", "timezone": "Asia/Kolkata", "continent": "Asia"},
    "CN": {"name": "China", "capital": "Beijing", "lat": 39.9042, "lng": 116.4074, "currency": "CNY (¥)", "timezone": "Asia/Shanghai", "continent": "Asia"},
    "JP": {"name": "Japan", "capital": "Tokyo", "lat": 35.6762, "lng": 139.6503, "currency": "JPY (¥)", "timezone": "Asia/Tokyo", "continent": "Asia"},
    "DE": {"name": "Germany", "capital": "Berlin", "lat": 52.5200, "lng": 13.4050, "currency": "EUR (€)", "timezone": "Europe/Berlin", "continent": "Europe"},
    "FR": {"name": "France", "capital": "Paris", "lat": 48.8566, "lng": 2.3522, "currency": "EUR (€)", "timezone": "Europe/Paris", "continent": "Europe"},
    "CA": {"name": "Canada", "capital": "Ottawa", "lat": 45.4215, "lng": -75.6972, "currency": "CAD ($)", "timezone": "America/Toronto", "continent": "North America"},
    "AU": {"name": "Australia", "capital": "Canberra", "lat": -35.2809, "lng": 149.1300, "currency": "AUD ($)", "timezone": "Australia/Sydney", "continent": "Oceania"},
    "BR": {"name": "Brazil", "capital": "Brasília", "lat": -15.7975, "lng": -47.8919, "currency": "BRL (R$)", "timezone": "America/Sao_Paulo", "continent": "South America"},
    "ZA": {"name": "South Africa", "capital": "Pretoria", "lat": -25.7479, "lng": 28.2293, "currency": "ZAR (R)", "timezone": "Africa/Johannesburg", "continent": "Africa"},
    "IT": {"name": "Italy", "capital": "Rome", "lat": 41.9028, "lng": 12.4964, "currency": "EUR (€)", "timezone": "Europe/Rome", "continent": "Europe"},
    "ES": {"name": "Spain", "capital": "Madrid", "lat": 40.4168, "lng": -3.7038, "currency": "EUR (€)", "timezone": "Europe/Madrid", "continent": "Europe"},
    "SA": {"name": "Saudi Arabia", "capital": "Riyadh", "lat": 24.7136, "lng": 46.6753, "currency": "SAR (﷼)", "timezone": "Asia/Riyadh", "continent": "Middle East"},
    "AE": {"name": "United Arab Emirates", "capital": "Abu Dhabi", "lat": 24.4539, "lng": 54.3773, "currency": "AED (د.إ)", "timezone": "Asia/Dubai", "continent": "Middle East"},
    "SG": {"name": "Singapore", "capital": "Singapore", "lat": 1.3521, "lng": 103.8198, "currency": "SGD ($)", "timezone": "Asia/Singapore", "continent": "Asia"},
    "KR": {"name": "South Korea", "capital": "Seoul", "lat": 37.5665, "lng": 126.9780, "currency": "KRW (₩)", "timezone": "Asia/Seoul", "continent": "Asia"},
    "MX": {"name": "Mexico", "capital": "Mexico City", "lat": 19.4326, "lng": -99.1332, "currency": "MXN ($)", "timezone": "America/Mexico_City", "continent": "North America"},
    "ID": {"name": "Indonesia", "capital": "Jakarta", "lat": -6.2088, "lng": 106.8456, "currency": "IDR (Rp)", "timezone": "Asia/Jakarta", "continent": "Asia"},
    "NG": {"name": "Nigeria", "capital": "Abuja", "lat": 9.0765, "lng": 7.3986, "currency": "NGN (₦)", "timezone": "Africa/Lagos", "continent": "Africa"},
    "EG": {"name": "Egypt", "capital": "Cairo", "lat": 30.0444, "lng": 31.2357, "currency": "EGP (E£)", "timezone": "Africa/Cairo", "continent": "Africa"},
    "AR": {"name": "Argentina", "capital": "Buenos Aires", "lat": -34.6037, "lng": -58.3816, "currency": "ARS ($)", "timezone": "America/Argentina/Buenos_Aires", "continent": "South America"},
    "CH": {"name": "Switzerland", "capital": "Bern", "lat": 46.9480, "lng": 7.4474, "currency": "CHF (Fr.)", "timezone": "Europe/Zurich", "continent": "Europe"},
    "SE": {"name": "Sweden", "capital": "Stockholm", "lat": 59.3293, "lng": 18.0686, "currency": "SEK (kr)", "timezone": "Europe/Stockholm", "continent": "Europe"},
    "NL": {"name": "Netherlands", "capital": "Amsterdam", "lat": 52.3676, "lng": 4.9041, "currency": "EUR (€)", "timezone": "Europe/Amsterdam", "continent": "Europe"},
    "TR": {"name": "Turkey", "capital": "Ankara", "lat": 39.9334, "lng": 32.8597, "currency": "TRY (₺)", "timezone": "Europe/Istanbul", "continent": "Europe"},
    "PL": {"name": "Poland", "capital": "Warsaw", "lat": 52.2297, "lng": 21.0122, "currency": "PLN (zł)", "timezone": "Europe/Warsaw", "continent": "Europe"},
    "NO": {"name": "Norway", "capital": "Oslo", "lat": 59.9139, "lng": 10.7522, "currency": "NOK (kr)", "timezone": "Europe/Oslo", "continent": "Europe"},
    "NZ": {"name": "New Zealand", "capital": "Wellington", "lat": -41.2865, "lng": 174.7762, "currency": "NZD ($)", "timezone": "Pacific/Auckland", "continent": "Oceania"},
    "KE": {"name": "Kenya", "capital": "Nairobi", "lat": -1.2921, "lng": 36.8219, "currency": "KES (KSh)", "timezone": "Africa/Nairobi", "continent": "Africa"},
    "IE": {"name": "Ireland", "capital": "Dublin", "lat": 53.3498, "lng": -6.2603, "currency": "EUR (€)", "timezone": "Europe/Dublin", "continent": "Europe"},
    "GR": {"name": "Greece", "capital": "Athens", "lat": 37.9838, "lng": 23.7275, "currency": "EUR (€)", "timezone": "Europe/Athens", "continent": "Europe"},
    "PT": {"name": "Portugal", "capital": "Lisbon", "lat": 38.7223, "lng": -9.1393, "currency": "EUR (€)", "timezone": "Europe/Lisbon", "continent": "Europe"},
    "TH": {"name": "Thailand", "capital": "Bangkok", "lat": 13.7563, "lng": 100.5018, "currency": "THB (฿)", "timezone": "Asia/Bangkok", "continent": "Asia"},
    "VN": {"name": "Vietnam", "capital": "Hanoi", "lat": 21.0285, "lng": 105.8542, "currency": "VND (₫)", "timezone": "Asia/Ho_Chi_Minh", "continent": "Asia"},
    "MY": {"name": "Malaysia", "capital": "Kuala Lumpur", "lat": 3.1390, "lng": 101.6869, "currency": "MYR (RM)", "timezone": "Asia/Kuala_Lumpur", "continent": "Asia"},
    "IL": {"name": "Israel", "capital": "Jerusalem", "lat": 31.7683, "lng": 35.2137, "currency": "ILS (₪)", "timezone": "Asia/Jerusalem", "continent": "Middle East"},
    "PK": {"name": "Pakistan", "capital": "Islamabad", "lat": 33.6844, "lng": 73.0479, "currency": "PKR (₨)", "timezone": "Asia/Karachi", "continent": "Asia"},
    "BD": {"name": "Bangladesh", "capital": "Dhaka", "lat": 23.8103, "lng": 90.4125, "currency": "BDT (৳)", "timezone": "Asia/Dhaka", "continent": "Asia"},
    "CO": {"name": "Colombia", "capital": "Bogotá", "lat": 4.7110, "lng": -74.0721, "currency": "COP ($)", "timezone": "America/Bogota", "continent": "South America"},
    "CL": {"name": "Chile", "capital": "Santiago", "lat": -33.4489, "lng": -70.6693, "currency": "CLP ($)", "timezone": "America/Santiago", "continent": "South America"},
    "PH": {"name": "Philippines", "capital": "Manila", "lat": 14.5995, "lng": 120.9842, "currency": "PHP (₱)", "timezone": "Asia/Manila", "continent": "Asia"},
    "AT": {"name": "Austria", "capital": "Vienna", "lat": 48.2082, "lng": 16.3738, "currency": "EUR (€)", "timezone": "Europe/Vienna", "continent": "Europe"},
    "DK": {"name": "Denmark", "capital": "Copenhagen", "lat": 55.6761, "lng": 12.5683, "currency": "DKK (kr)", "timezone": "Europe/Copenhagen", "continent": "Europe"},
    "FI": {"name": "Finland", "capital": "Helsinki", "lat": 60.1699, "lng": 24.9384, "currency": "EUR (€)", "timezone": "Europe/Helsinki", "continent": "Europe"},
    "BE": {"name": "Belgium", "capital": "Brussels", "lat": 50.8503, "lng": 4.3517, "currency": "EUR (€)", "timezone": "Europe/Brussels", "continent": "Europe"},
    "QA": {"name": "Qatar", "capital": "Doha", "lat": 25.2854, "lng": 51.5310, "currency": "QAR (﷼)", "timezone": "Asia/Qatar", "continent": "Middle East"},
    "MA": {"name": "Morocco", "capital": "Rabat", "lat": 34.0209, "lng": -6.8416, "currency": "MAD (DH)", "timezone": "Africa/Casablanca", "continent": "Africa"},
    "RU": {"name": "Russia", "capital": "Moscow", "lat": 55.7558, "lng": 37.6173, "currency": "RUB (₽)", "timezone": "Europe/Moscow", "continent": "Europe"},
    "UA": {"name": "Ukraine", "capital": "Kyiv", "lat": 50.4501, "lng": 30.5234, "currency": "UAH (₴)", "timezone": "Europe/Kyiv", "continent": "Europe"},
    "GH": {"name": "Ghana", "capital": "Accra", "lat": 5.6037, "lng": -0.1870, "currency": "GHS (GH₵)", "timezone": "Africa/Accra", "continent": "Africa"},
    "IS": {"name": "Iceland", "capital": "Reykjavik", "lat": 64.1466, "lng": -21.9426, "currency": "ISK (kr)", "timezone": "Atlantic/Reykjavik", "continent": "Europe"},
    "PE": {"name": "Peru", "capital": "Lima", "lat": -12.0464, "lng": -77.0428, "currency": "PEN (S/.)", "timezone": "America/Lima", "continent": "South America"},
}

# ISO3 to ISO2 mapping
ISO3_TO_ISO2 = {
    "AFG": "AF", "ALB": "AL", "DZA": "DZ", "AND": "AD", "AGO": "AO", "ARG": "AR", "ARM": "AM", "AUS": "AU",
    "AUT": "AT", "AZE": "AZ", "BHS": "BS", "BHR": "BH", "BGD": "BD", "ARM": "AM", "BEL": "BE", "BLZ": "BZ",
    "BEN": "BJ", "BTN": "BT", "BOL": "BO", "BIH": "BA", "BWA": "BW", "BRA": "BR", "BRN": "BN", "BGR": "BG",
    "BFA": "BF", "BDI": "BI", "KHM": "KH", "CMR": "CM", "CAN": "CA", "CAF": "CF", "TCD": "TD", "CHL": "CL",
    "CHN": "CN", "COL": "CO", "COG": "CG", "COD": "CD", "CRI": "CR", "CIV": "CI", "HRV": "HR", "CUB": "CU",
    "CYP": "CY", "CZE": "CZ", "DNK": "DK", "DJI": "DJ", "DOM": "DO", "ECU": "EC", "EGY": "EG", "SLV": "SV",
    "GNQ": "GQ", "ERI": "ER", "EST": "EE", "ETH": "ET", "FJI": "FJ", "FIN": "FI", "FRA": "FR", "GAB": "GA",
    "GMB": "GM", "GEO": "GE", "DEU": "DE", "GHA": "GH", "GRC": "GR", "GTM": "GT", "GIN": "GN", "GNB": "GW",
    "GUY": "GY", "HTI": "HT", "HND": "HN", "HUN": "HU", "ISL": "IS", "IND": "IN", "IDN": "ID", "IRN": "IR",
    "IRQ": "IQ", "IRL": "IE", "ISR": "IL", "ITA": "IT", "JAM": "JM", "JPN": "JP", "JOR": "JO", "KAZ": "KZ",
    "KEN": "KE", "PRK": "KP", "KOR": "KR", "KWT": "KW", "KGZ": "KG", "LAO": "LA", "LVA": "LV", "LBN": "LB",
    "LSO": "LS", "LBR": "LR", "LBY": "LY", "LTU": "LT", "LUX": "LU", "MDG": "MG", "MWI": "MW", "MYS": "MY",
    "MLI": "ML", "MRT": "MR", "MUS": "MU", "MEX": "MX", "MDA": "MD", "MNG": "MN", "MNE": "ME", "MAR": "MA",
    "MOZ": "MZ", "MMR": "MM", "NAM": "NA", "NPL": "NP", "NLD": "NL", "NZL": "NZ", "NIC": "NI", "NER": "NE",
    "NGA": "NG", "MKD": "MK", "NOR": "NO", "OMN": "OM", "PAK": "PK", "PAN": "PA", "PNG": "PG", "PRY": "PY",
    "PER": "PE", "PHL": "PH", "POL": "PL", "PRT": "PT", "QAT": "QA", "ROU": "RO", "RUS": "RU", "RWA": "RW",
    "SAU": "SA", "SEN": "SN", "SRB": "RS", "SLE": "SL", "SGP": "SG", "SVK": "SK", "SVN": "SI", "SOM": "SO",
    "ZAF": "ZA", "SSD": "SS", "ESP": "ES", "LKA": "LK", "SDN": "SD", "SUR": "SR", "SWE": "SE", "CHE": "CH",
    "SYR": "SY", "TWN": "TW", "TJK": "TJ", "TZA": "TZ", "THA": "TH", "TLS": "TL", "TGO": "TG", "TTO": "TT",
    "TUN": "TN", "TUR": "TR", "TKM": "TM", "UGA": "UG", "UKR": "UA", "ARE": "AE", "GBR": "GB", "USA": "US",
    "URY": "UY", "UZB": "UZ", "VEN": "VE", "VNM": "VN", "YEM": "YE", "ZMB": "ZM", "ZWE": "ZW"
}

def get_flag_emoji(iso2):
    if not iso2 or len(iso2) != 2 or iso2 == '-99':
        return '🌐'
    try:
        return chr(ord(iso2[0].upper()) + 127397) + chr(ord(iso2[1].upper()) + 127397)
    except Exception:
        return '🌐'

def compute_centroid(geometry):
    """Simple centroid calculation for Leaflet pin placement."""
    coords = []
    g_type = geometry.get("type", "")
    if g_type == "Polygon":
        for ring in geometry.get("coordinates", []):
            coords.extend(ring)
    elif g_type == "MultiPolygon":
        for poly in geometry.get("coordinates", []):
            for ring in poly:
                coords.extend(ring)
    if not coords:
        return [0.0, 0.0]
    avg_lng = sum(p[0] for p in coords) / len(coords)
    avg_lat = sum(p[1] for p in coords) / len(coords)
    return [round(avg_lat, 4), round(avg_lng, 4)]

def main():
    dest_dir = r"c:\Anil Google Projects\world-news-map\data"
    os.makedirs(dest_dir, exist_ok=True)
    
    url = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_0_countries.geojson"
    print(f"Fetching 110m GeoJSON from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    enriched_features = []
    for f in data.get("features", []):
        props = f.get("properties", {})
        iso3 = props.get("iso_a3") or props.get("adm0_a3") or ""
        iso2 = props.get("iso_a2") or ""
        name = props.get("name") or props.get("admin") or "Unknown"

        # Resolve ISO2 if missing or -99
        if (not iso2 or iso2 == "-99") and iso3 in ISO3_TO_ISO2:
            iso2 = ISO3_TO_ISO2[iso3]
        elif name == "France":
            iso2 = "FR"
            iso3 = "FRA"
        elif name == "Norway":
            iso2 = "NO"
            iso3 = "NOR"

        meta = COUNTRY_METADATA.get(iso2, {})
        centroid = compute_centroid(f.get("geometry", {}))
        
        # Override lat/lng with capital if available
        lat = meta.get("lat", centroid[0])
        lng = meta.get("lng", centroid[1])
        capital = meta.get("capital", "Capital")
        currency = meta.get("currency", "Local Currency")
        timezone = meta.get("timezone", "UTC")
        continent = meta.get("continent") or props.get("continent") or "Global"

        enriched_props = {
            "name": name,
            "iso2": iso2,
            "iso3": iso3,
            "flag": get_flag_emoji(iso2),
            "capital": capital,
            "lat": lat,
            "lng": lng,
            "centroid": centroid,
            "currency": currency,
            "timezone": timezone,
            "continent": continent,
            "subregion": props.get("subregion", ""),
            "pop_est": props.get("pop_est", 0)
        }
        f["properties"] = enriched_props
        enriched_features.append(f)

    data["features"] = enriched_features

    geojson_path = os.path.join(dest_dir, "countries.geojson")
    with open(geojson_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"Saved {geojson_path} ({os.path.getsize(geojson_path) // 1024} KB)")

    # Also save as JS file for direct script inclusion
    js_path = os.path.join(dest_dir, "countries-geo.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("/* Natural Earth 110m Countries GeoJSON with enriched metadata */\n")
        f.write("window.WORLD_COUNTRIES_GEOJSON = ")
        json.dump(data, f, ensure_ascii=False)
        f.write(";\n")
    print(f"Saved {js_path} ({os.path.getsize(js_path) // 1024} KB)")

if __name__ == "__main__":
    main()
