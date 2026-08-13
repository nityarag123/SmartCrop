"""AI crop recommendation service.

Primary: a trained RandomForest classifier (scikit-learn) fitted on the
Crop_recommendation dataset, reused from the existing repository artifact
``artifacts/crop_recommender.joblib``.

Fallback: a transparent rule-based scorer. The response always tells the caller
which engine produced the result, so the fallback is never misrepresented as a
trained ML model.
"""
import os
import threading

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Order must match the fitted artifact (artifacts/crop_recommender.joblib).
_FEATURES = ["temperature", "humidity", "rainfall", "ph", "nitrogen", "phosphorus", "potassium"]
_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATASET = os.path.join(_BASE, "crop_yield_dataset.csv")
ARTIFACT = os.path.join(_BASE, "artifacts", "crop_recommender.joblib")

_lock = threading.Lock()
_model = None


# Crop knowledge used to enrich recommendations with farmer-friendly guidance.
CROP_GUIDANCE = {
    "rice": {
        "water_requirement": "High — flooded field (1,200-1,500 mm season rainfall)",
        "growing_season": "Kharif (Jun-Nov), Rabi in irrigated areas",
        "suitable_soil": "Clay loam, holds standing water",
        "guidance": "Transplant 25-30 day old seedlings; split nitrogen; keep 3-5 cm water during tillering.",
    },
    "wheat": {
        "water_requirement": "Medium (450-650 mm)",
        "growing_season": "Rabi (Nov-Apr)",
        "suitable_soil": "Well drained loam to clay loam",
        "guidance": "Sow at proper depth; irrigate at crown root, flowering and grain filling stages.",
    },
    "maize": {
        "water_requirement": "Medium (500-800 mm)",
        "growing_season": "Kharif (Jun-Oct), Rabi, Zaid",
        "suitable_soil": "Well drained sandy loam to loam",
        "guidance": "Critical moisture at knee-high, tasseling and silking; top-dress nitrogen before tasseling.",
    },
    "sugarcane": {
        "water_requirement": "High (1,500-2,500 mm)",
        "growing_season": "Kharif / spring planting, 10-12 month crop",
        "suitable_soil": "Deep well drained loam",
        "guidance": "Plant setts with 2-3 buds; regular irrigation; earthing up at tillering.",
    },
    "cotton": {
        "water_requirement": "Medium (600-800 mm)",
        "growing_season": "Kharif (May-Oct)",
        "suitable_soil": "Deep black cotton soil / well drained loam",
        "guidance": "Avoid waterlogging; monitor bollworm and sucking pests during fruiting.",
    },
    "groundnut": {
        "water_requirement": "Low-Medium (300-500 mm)",
        "growing_season": "Kharif (Jun-Oct), Rabi",
        "suitable_soil": "Light well drained sandy loam",
        "guidance": "Apply gypsum at flowering; avoid water stress at peg formation.",
    },
    "soybean": {
        "water_requirement": "Medium (450-700 mm)",
        "growing_season": "Kharif (Jun-Sep)",
        "suitable_soil": "Well drained loam, pH 6-7.5",
        "guidance": "Use inoculated seed; avoid waterlogging at germination.",
    },
    "chickpea": {
        "water_requirement": "Low (300-400 mm)",
        "growing_season": "Rabi (Oct-Feb)",
        "suitable_soil": "Well drained sandy loam",
        "guidance": "One irrigation at establishment; manage pod borer at flowering.",
    },
    "blackgram": {
        "water_requirement": "Low-Medium (400-500 mm)",
        "growing_season": "Kharif and Rabi",
        "suitable_soil": "Well drained loam",
        "guidance": "Sow at proper spacing; harvest as pods mature to avoid shattering.",
    },
    "green gram": {
        "water_requirement": "Low (300-400 mm)",
        "growing_season": "Kharif, Rabi, Zaid",
        "suitable_soil": "Light loam to sandy loam",
        "guidance": "Short duration crop; pick pods in 2-3 rounds to prevent shattering.",
    },
    "lentil": {
        "water_requirement": "Low (300-350 mm)",
        "growing_season": "Rabi (Oct-Mar)",
        "suitable_soil": "Light loam",
        "guidance": "Good for residual moisture; low input legume.",
    },
    "pigeon peas": {
        "water_requirement": "Medium (500-700 mm)",
        "growing_season": "Kharif (Jun-Dec)",
        "suitable_soil": "Well drained loam to clay loam",
        "guidance": "Long duration crop; manage pod borer and wilt.",
    },
    "moth beans": {
        "water_requirement": "Very Low (250-350 mm)",
        "growing_season": "Kharif in arid areas",
        "suitable_soil": "Sandy to sandy loam, arid regions",
        "guidance": "Drought hardy; suited to low rainfall areas.",
    },
    "mungbean": {
        "water_requirement": "Low (300-400 mm)",
        "growing_season": "Kharif, Zaid",
        "suitable_soil": "Loam to sandy loam",
        "guidance": "Short duration; harvest pods before shattering.",
    },
    "muskmelon": {
        "water_requirement": "Medium (400-600 mm)",
        "growing_season": "Zaid (Mar-Jun)",
        "suitable_soil": "Sandy loam, well drained",
        "guidance": "Requires warm dry weather; avoid water stress at fruiting.",
    },
    "watermelon": {
        "water_requirement": "Medium (400-600 mm)",
        "growing_season": "Zaid (Feb-Jun)",
        "suitable_soil": "Well drained sandy loam",
        "guidance": "Warm season vine crop; irrigate at flowering and fruit set.",
    },
    "banana": {
        "water_requirement": "High (1,200-2,000 mm)",
        "growing_season": "Perennial (planting year-round in irrigated areas)",
        "suitable_soil": "Deep, rich loam with good drainage",
        "guidance": "Requires warmth and regular feeding; protect bunches from wind.",
    },
    "mango": {
        "water_requirement": "Low-Medium (rainfed/irrigated)",
        "growing_season": "Perennial; flowering Jan-Mar",
        "suitable_soil": "Deep well drained alluvial to laterite",
        "guidance": "Avoid water stress at flowering; control stone weevil and hoppers.",
    },
    "orange": {
        "water_requirement": "Medium (900-1,200 mm)",
        "growing_season": "Perennial",
        "suitable_soil": "Well drained sandy loam, pH 6-7",
        "guidance": "Regular irrigation; protect from citrus canker and fruit fly.",
    },
    "grape": {
        "water_requirement": "Medium (700-1,000 mm)",
        "growing_season": "Perennial (pruning-driven)",
        "suitable_soil": "Well drained sandy loam to loam",
        "guidance": "Pruning and trellising essential; manage powdery mildew.",
    },
    "papaya": {
        "water_requirement": "Medium-High (1,000-1,500 mm)",
        "growing_season": "Year-round (irrigated)",
        "suitable_soil": "Well drained sandy loam",
        "guidance": "Fast growing; needs regular feeding and virus-free plants.",
    },
    "pomegranate": {
        "water_requirement": "Low-Medium (500-800 mm)",
        "growing_season": "Perennial; flowering Feb-Mar and Jun-Jul",
        "suitable_soil": "Well drained medium black to loamy soil",
        "guidance": "Drought tolerant; manage fruit borer and bacterial blight.",
    },
    "coconut": {
        "water_requirement": "High (1,500-2,300 mm)",
        "growing_season": "Perennial (planting May-Jun)",
        "suitable_soil": "Coastal sandy to alluvial, well drained",
        "guidance": "Requires humid coastal climate; regular organic manuring.",
    },
    "coffee": {
        "water_requirement": "Medium-High (1,500-2,500 mm)",
        "growing_season": "Perennial; blossom showers Feb-Mar",
        "suitable_soil": "Rich well drained forest loam under shade",
        "guidance": "Needs shade and high altitude; manage leaf rust.",
    },
    "jute": {
        "water_requirement": "High (1,200-1,500 mm)",
        "growing_season": "Kharif (Apr-Aug)",
        "suitable_soil": "Loam to clay loam with retting water",
        "guidance": "Grows in warm humid plains; retting quality affects fibre price.",
    },
    "kidney beans": {
        "water_requirement": "Medium (450-600 mm)",
        "growing_season": "Kharif/Rabi hills, Zaid plains",
        "suitable_soil": "Well drained loam",
        "guidance": "Cool season legume; manage pod borer and anthracnose.",
    },
    "apple": {
        "water_requirement": "Medium (900-1,200 mm)",
        "growing_season": "Perennial (temperate)",
        "suitable_soil": "Deep well drained loam, pH 6-7",
        "guidance": "Needs winter chill; manage scab, powdery mildew and codling moth.",
    },
}


def load_model(force=False):
    """Load the trained model once and reuse it across requests."""
    global _model
    if _model is not None and not force:
        return _model
    with _lock:
        if _model is None or force:
            if not os.path.exists(ARTIFACT):
                _train()
            _model = joblib.load(ARTIFACT)
    return _model


def _train():
    frame = pd.read_csv(DATASET)
    frame = frame.rename(columns={"N": "nitrogen", "P": "phosphorus", "K": "potassium", "label": "crop"})
    X = frame[_FEATURES]
    y = frame["crop"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)
    os.makedirs(os.path.dirname(ARTIFACT), exist_ok=True)
    joblib.dump(model, ARTIFACT)


def validate_input(data):
    """Validate raw soil/weather inputs; returns (values, error)."""
    values = {}
    for key in _FEATURES:
        try:
            value = float(data.get(key))
        except (TypeError, ValueError):
            return None, f"'{key}' must be a number"
        if value < 0:
            return None, f"'{key}' cannot be negative"
        values[key] = value
    bounds = {"ph": (0, 14)}
    for key, (low, high) in bounds.items():
        if not (low <= values[key] <= high):
            return None, f"'{key}' must be between {low} and {high}"
    return values, None


def _rule_based_recommend(values):
    """Transparent fallback used only when the ML artifact is unavailable."""
    temp = values["temperature"]
    rain = values["rainfall"]
    ph = values["ph"]
    nitrogen = values["nitrogen"]

    if rain >= 170 and temp >= 24 and 5.5 <= ph <= 7.5:
        crop = "rice"
    elif 15 <= temp <= 28 and 100 <= rain <= 180 and 5.5 <= ph <= 7.8:
        crop = "wheat"
    elif 18 <= temp <= 35 and rain >= 80 and nitrogen >= 40:
        crop = "maize"
    elif temp >= 25 and 6.0 <= ph <= 8.5 and 50 <= rain <= 150:
        crop = "cotton"
    elif 18 <= temp <= 30 and 6.5 <= ph <= 7.5:
        crop = "chickpea"
    elif rain < 80 and temp >= 24 and 6.0 <= ph <= 8.0:
        crop = "moth beans"
    else:
        crop = "maize"
    confidence = 55.0
    reason = "Rule-based fallback (ML model not available): matched typical growing conditions from your inputs."
    return crop, confidence, reason, "rule-based"


def recommend_crop(data):
    """Return a full crop recommendation dict."""
    values, error = validate_input(data)
    if error:
        return {"error": error}, 400

    crop, confidence, reason, engine = None, None, None, None
    try:
        model = load_model()
        frame = pd.DataFrame([values], columns=_FEATURES)
        proba = model.predict_proba(frame)[0]
        order = model.classes_
        top_index = int(proba.argmax())
        crop = order[top_index]
        confidence = round(float(proba[top_index]) * 100, 1)

        probs = list(zip([str(c) for c in order], [round(float(p) * 100, 1) for p in proba]))
        probs.sort(key=lambda item: item[1], reverse=True)
        alternatives = [
            {"crop": name, "confidence": pct}
            for name, pct in probs[1:4] if pct > 5.0
        ]
        reason = (
            f"The trained model found your soil and climate conditions most similar to farms "
            f"where {crop} grows successfully."
        )
        engine = "ML"
    except Exception:
        crop, confidence, reason, engine = _rule_based_recommend(values)
        alternatives = []

    guidance = CROP_GUIDANCE.get(str(crop).strip().lower(), {})
    result = {
        "crop": str(crop).title() if str(crop).islower() else str(crop),
        "confidence": confidence,
        "reason": reason,
        "engine": engine,
        "alternatives": alternatives,
        "water_requirement": guidance.get("water_requirement", ""),
        "growing_season": guidance.get("growing_season", ""),
        "suitable_soil": guidance.get("suitable_soil", ""),
        "guidance": guidance.get("guidance", ""),
        "inputs": {k: values[k] for k in _FEATURES},
        "model_available": engine == "ML",
    }
    return result, 200
