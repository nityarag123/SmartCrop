# SMARTCROP — AI Powered Agriculture

SmartCrop is a full-stack farming assistant platform for Indian farmers. It combines
real machine-learning models, an optional knowledge-base chatbot, and a mobile-first,
multilingual (English · हिन्दी · తెలుగు · தமிழ் · ગુજરાતી) web interface in a single
Flask application. No frontend framework is used — plain HTML5 + CSS3 + vanilla JS.

## Features

| Area | What it does |
| --- | --- |
| 🌱 AI Crop Recommendation | Trained scikit-learn classifier recommends a crop from soil + climate inputs, with confidence, alternatives and growing guidance |
| 🧪 Soil Analysis | Classifies N/P/K/pH values using agronomy reference ranges; transparently states it is guidance, not a lab test |
| 🐛 Pest & Disease Detection | Upload a plant photo → real trained pest classifier (or PyTorch plant-disease model when available) |
| 🌦 Weather & Advice | Current weather, 5-day forecast and farming advice (live via keyless Open-Meteo, clearly-labelled demo otherwise) |
| 📅 Crop Calendar | Sowing → harvesting timelines from an agronomy knowledge base; save your crop+season |
| 🏛 Government Schemes | PM-KISAN, PMFBY, KCC, PMKSY, Soil Health Card, e-NAM, PKVY + state schemes |
| 🤖 AI Farm Assistant | Knowledge-base chatbot (OpenAI optional) with typing + 🎤 voice input and 🔊 text-to-speech |
| 👤 Profile & Dashboard | Farmer profile, farm details, notifications and a live dashboard aggregating all tools |

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env            # Linux/macOS: cp .env.example .env
python app.py
```

Open `http://127.0.0.1:5000`. A demo account is created for testing:
`test@smartcrop.in` / `secret123`.

### Environment variables (`.env`)

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Flask session secret |
| `MONGODB_URI` | MongoDB Atlas connection string (optional — JSON-file fallback is used when absent) |
| `MONGO_DB_NAME` | Database name on Atlas |
| `WEATHER_API_KEY` | Optional OpenWeatherMap key — used only if keyless Open-Meteo is unreachable (demo data used otherwise) |
| `LLM_API_KEY` / `LLM_MODEL` | OpenAI-style LLM for the assistant (knowledge-base fallback without it) |
| `USE_LOCAL_FALLBACK` | `true` → always use the JSON store (default when MongoDB unreachable) |
| `LOCAL_STORE_PATH` | Fallback JSON store path (default `instance/smartcrop_store.json`) |

## Architecture

```
app.py                     → entry point
config.py                  → configuration
backend/
  __init__.py              → app factory, blueprints, JSON errors, frontend serving
  models/db.py             → MongoStore + FileStore (MongoDB Atlas with JSON fallback)
  models/users.py          → user auth/profile helpers (werkzeug password hashing)
  seed.py                  → government schemes, crop calendar knowledge base
  routes/                  → auth, profile, weather, crop, soil, pest, chat,
                             calendar, schemes, dashboard (all under /api)
  ml/crop_recommendation/  → trained model + transparent rule fallback
  ml/soil_analysis/        → agronomy reference-range classifier (honest guidance)
  ml/pest_detection/       → sklearn pest classifier + optional torch disease model
  chatbot/                 → LLM client (optional), knowledge-base fallback, translation (optional)
  services/                → weather (keyless Open-Meteo) service
  utils/helpers.py         → JSON helpers, login_required, validation
frontend/                  → static site served by Flask
  index.html …             → landing, auth, dashboard, chatbot, weather, soil, crop,
                             pest, calendar, schemes, profile, 404 pages
  css/                     → style.css, forms.css, dashboard.css, chatbot.css, responsive.css
  js/                      → api.js (central fetch), i18n.js (5 languages), main.js (shared
                             shell + auth guard), geo.js (auto location detection), voice.js
                             (Speech API), page scripts
  assets/                  → logo / favicon
artifacts/                 → crop_recommender.joblib, pest_classifier.joblib
data/pest/                 → pest training images
models/                    → optional PyTorch plant-disease model (plant_disease_model.pt)
static/data/               → states/districts data
legacy/                    → original Farmspace code (unused, kept for reference)
```

## API overview (all under `/api`)

- Auth: `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`, `GET /auth/status`
- Profile: `GET/PUT /profile`
- Weather: `GET /weather?location=…`, `/weather/forecast`, `/weather/advice` (all also accept `lat`/`lon`)
- AI tools: `POST /crop/recommend`, `POST /soil/analyze`, `POST /soil/image`, `POST /pest/detect`
- Assistant: `POST /chat`, `GET /chat/history`
- Data: `GET/POST /calendar`, `GET /schemes`, `GET /schemes/<code>`, `GET /dashboard`

## Honesty & safety

- Soil analysis is explicitly labelled *soil-health-guidance*; a photo upload only validates the
  file and never claims lab-accurate NPK.
- Pest detection states which model produced each result and returns only safe, non-chemical
  guidance; serious cases point to an agriculture officer.
- Weather is LIVE by default and needs no API key: **Open-Meteo** provides the real forecast
  and geocoding (keyless). `WEATHER_API_KEY` (OpenWeatherMap) is an optional secondary source
  used only if Open-Meteo is unreachable.
- If the live weather service is unreachable, the endpoint returns seeded data clearly
  labelled `demo` (a "demo data" tag) — SmartCrop never labels demo data as real-time.
- The chatbot uses a knowledge base unless an LLM API key and package are configured.
- API errors are clean JSON; stack traces are never shown to farmers.

## Automatic location detection

- `frontend/js/geo.js` (`SmartCropGeo`) auto-detects the user's location: browser geolocation
  (with permission) → free reverse geocoding (BigDataCloud) → keyless IP fallback chain
  (`ipwho.is`, `get.geojs.io`, BigDataCloud). Results are cached in `localStorage["smartcrop.geo"]`.
- Login and register are kept minimal (name/email/password only) — no location prompt before login.
- Location detection happens after login, inside the app: the Crop Recommendation page has a
  "📍 Use my location" button that fills Temperature/Humidity/Rainfall from the detected location's
  weather; the Weather page auto-loads with the detected location (coords sent as `lat`/`lon` plus
  a 📍 re-detect button); the Profile page has a "📍 Detect" button that fills Village/City, State
  and District; the dashboard passes coords so weather guidance works even before a profile
  location is saved.

## Tests / verification

All 10 API groups were exercised end-to-end against the running server (register/login/me,
profile, weather, crop recommendation, soil analysis, pest detection, chat + history, calendar,
schemes, dashboard). The pest classifier was retrained on `data/pest`
(2,700 images, 9 classes, ~99% validation accuracy) into `artifacts/pest_classifier.joblib`.

## Notes

- MongoDB Atlas is used automatically when `MONGODB_URI` is set; otherwise the app uses
  `instance/smartcrop_store.json`. Switch back by setting the URI and restarting.
- Live weather comes from Open-Meteo (keyless). To use a different live weather source, set
  `WEATHER_API_KEY` (OpenWeatherMap). A short outage of the service drops back to
  clearly-labelled demo data.
- For the LLM assistant, install the SDK for your provider (e.g. `pip install openai`) and set
  `LLM_API_KEY`. For PyTorch disease detection, install `torch` + `torchvision` and place a
  checkpoint at `models/plant_disease_model.pt`.
