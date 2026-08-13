"""Soil analysis service.

Important and transparent: SmartCrop does NOT claim that a photograph of soil
can produce accurate NPK/pH numbers without a trained model and a matching
dataset. This service therefore works with lab/test values entered by the
farmer and classifies them using standard agronomy reference ranges.

Image upload is accepted for a *visual* soil texture/colour classification
only, and the output clearly states that limitation.
"""
import os

import numpy as np
from PIL import Image

_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _bounded(value, default, low, high):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return default
    return max(low, min(high, value))


def classify(value, low, medium, unit=""):
    """Return (level, label, pct) for a nutrient value using reference ranges."""
    value = float(value)
    if value < low:
        return "low", "Low", _percent(value, 0, low), unit
    if value <= medium:
        return "medium", "Medium", _percent(value, low, medium), unit
    return "high", "High", 100, unit


def _percent(value, low, high):
    if high <= low:
        return 100
    return max(0, min(100, int(round((value - low) / (high - low) * 100))))


def _fertilizer_guidance(status):
    tips = []
    if status["ph"] == "low":
        tips.append("pH is acidic — apply lime/dolomite gradually to raise pH to 6.5-7.0.")
    elif status["ph"] == "high":
        tips.append("pH is alkaline — apply gypsum/organic matter and use acid-forming fertilisers like ammonium sulphate.")
    else:
        tips.append("pH is in the ideal 6.5-7.5 range for most crops.")

    if status["n"] == "low":
        tips.append("Nitrogen low — apply nitrogen-rich fertiliser (urea/DAP) as per the crop and growth stage.")
    elif status["n"] == "high":
        tips.append("Nitrogen high — avoid extra nitrogen; excess causes lodging and pest attack.")
    else:
        tips.append("Nitrogen adequate — follow the recommended dose for your crop.")

    if status["p"] == "low":
        tips.append("Phosphorus low — apply DAP/Superphosphate or bone meal; add at sowing for root growth.")
    elif status["p"] == "high":
        tips.append("Phosphorus high — withhold phosphorus fertilisers this season.")
    else:
        tips.append("Phosphorus adequate — continue a balanced dose.")

    if status["k"] == "low":
        tips.append("Potassium low — apply MOP/potash to improve fruit/seed quality and disease resistance.")
    elif status["k"] == "high":
        tips.append("Potassium high — avoid extra potash this season.")
    else:
        tips.append("Potassium adequate — maintain a balanced schedule.")
    return tips


def analyze(values):
    """Analyse soil values. values: {nitrogen, phosphorus, potassium, ph, moisture}"""
    try:
        n = _bounded(values.get("nitrogen"), 25, 0, 500)
        p = _bounded(values.get("phosphorus"), 25, 0, 500)
        k = _bounded(values.get("potassium"), 25, 0, 500)
        ph = _bounded(values.get("ph"), 7.0, 0, 14)
        moisture = _bounded(values.get("moisture", 50), 50, 0, 100)
    except Exception:
        return {"error": "Invalid soil values provided."}, 400

    n_level, n_label, n_pct, _ = classify(n, 30, 60)
    p_level, p_label, p_pct, _ = classify(p, 15, 40)
    k_level, k_label, k_pct, _ = classify(k, 30, 70)

    if ph < 6.0:
        ph_level, ph_label, ph_pct = "low", "Acidic", _percent(ph, 0, 6.0)
    elif ph <= 7.5:
        ph_level, ph_label, ph_pct = "medium", "Ideal", _percent(ph, 6.0, 7.5)
    else:
        ph_level, ph_label, ph_pct = "high", "Alkaline", _percent(14 - ph, 0, 7.5)

    if moisture < 30:
        moisture_level, moisture_label = "low", "Dry"
    elif moisture <= 70:
        moisture_level, moisture_label = "medium", "Adequate"
    else:
        moisture_level, moisture_label = "high", "Wet"

    status = {"n": n_level, "p": p_level, "k": k_level, "ph": ph_level, "moisture": moisture_level}

    low_count = sum(1 for key in ("n", "p", "k", "ph") if status[key] == "low")
    if low_count >= 3:
        overall = "Poor — needs attention before sowing"
    elif low_count == 2:
        overall = "Fair — improve before major crops"
    elif low_count == 1:
        overall = "Good — minor corrections needed"
    else:
        overall = "Very good — suitable for most crops"

    suitable = _suitable_crops(status)

    result = {
        "engine": "soil-health-guidance",
        "engine_note": "Classification from the values you entered using standard agronomy reference ranges. For lab-accurate NPK, test a sample at a soil-testing lab.",
        "overall": overall,
        "ph": {"value": round(ph, 1), "label": ph_label, "status": ph_level, "percent": ph_pct},
        "nitrogen": {"value": round(n, 1), "label": n_label, "status": n_level, "percent": n_pct},
        "phosphorus": {"value": round(p, 1), "label": p_label, "status": p_level, "percent": p_pct},
        "potassium": {"value": round(k, 1), "label": k_label, "status": k_level, "percent": k_pct},
        "moisture": {"value": round(moisture, 1), "label": moisture_label, "status": moisture_level},
        "fertilizer_guidance": _fertilizer_guidance(status),
        "suitable_crops": suitable,
    }
    return result, 200


def _suitable_crops(status):
    if status["ph"] == "low":
        base = ["Tea", "Potato", "Sweet potato", "Rubber"]
    elif status["ph"] == "high":
        base = ["Barley", "Cotton", "Chickpea", "Sugarcane"]
    else:
        base = ["Rice", "Wheat", "Maize", "Soybean", "Tomato"]
    if status["n"] == "low":
        base = base[:3]
    return base


_SOIL_PROFILES = {
    "black": {
        "color": "Very dark / black soil",
        "organic": "Likely high — dark colour usually means high organic matter.",
        "drainage": "Poor to moderate — heavy black soils hold water but drain slowly; avoid waterlogging.",
        "nutrients": {
            "n": ("high", "Likely high", "Dark soils usually hold more organic nitrogen."),
            "p": ("medium", "Likely medium", "Phosphorus is usually present but can be locked in alkaline black soils."),
            "k": ("medium", "Likely medium", "Potassium is typically adequate."),
            "ph": ("medium", "Neutral to mildly alkaline", "Slightly alkaline pH is common; lime is rarely needed."),
        },
        "crops": ["Cotton", "Sugarcane", "Soybean", "Wheat", "Chickpea"],
        "guidance": [
            "Improve drainage with raised beds / ridges in low-lying fields.",
            "Use phosphorus-rich fertiliser (DAP/Superphosphate) at sowing to overcome fixation.",
            "Add farmyard manure or green manure to keep organic matter high.",
            "For exact N, P, K and pH, confirm with a lab soil test.",
        ],
    },
    "red": {
        "color": "Reddish soil",
        "organic": "Likely low — red colour indicates iron oxides with little organic matter.",
        "drainage": "Good — well-drained; water is lost quickly, so drought-prone in summer.",
        "nutrients": {
            "n": ("low", "Likely low", "Red soils tend to be nitrogen-poor."),
            "p": ("low", "Likely low-medium", "Phosphorus is often limited."),
            "k": ("medium", "Likely medium", "Potassium is usually moderate."),
            "ph": ("low", "Likely acidic", "Red soils are often acidic (pH 5.5-6.5)."),
        },
        "crops": ["Groundnut", "Millets", "Cotton", "Pulses", "Maize"],
        "guidance": [
            "Apply lime/dolomite gradually to correct acidity toward pH 6.5.",
            "Add farmyard manure/compost to raise organic matter.",
            "Use balanced NPK fertiliser; consider split nitrogen doses.",
            "Mulch to retain moisture in dry spells.",
        ],
    },
    "brown": {
        "color": "Brown loamy soil",
        "organic": "Likely medium — good all-round fertility.",
        "drainage": "Good — loam drains well yet holds enough moisture.",
        "nutrients": {
            "n": ("medium", "Likely medium", "Balanced nitrogen level expected."),
            "p": ("medium", "Likely medium", "Phosphorus level expected to be moderate."),
            "k": ("medium", "Likely medium", "Potassium level expected to be moderate."),
            "ph": ("medium", "Neutral (6-7.5)", "pH is usually close to ideal."),
        },
        "crops": ["Rice", "Wheat", "Maize", "Tomato", "Vegetables"],
        "guidance": [
            "Maintain balanced fertiliser doses based on the crop's stage.",
            "Add organic manure annually to sustain fertility.",
            "Test soil every 2-3 years to keep NPK and pH in range.",
        ],
    },
    "yellow": {
        "color": "Yellowish soil",
        "organic": "Likely low — yellowish tint indicates hydrated iron oxides, low fertility.",
        "drainage": "Good — well-drained but nutrient-leached.",
        "nutrients": {
            "n": ("low", "Likely low", "Yellow soils are generally nitrogen-poor."),
            "p": ("low", "Likely low", "Phosphorus is often deficient."),
            "k": ("low", "Likely low-medium", "Potassium may be limited too."),
            "ph": ("low", "Likely acidic", "Usually acidic and leached."),
        },
        "crops": ["Groundnut", "Pulses", "Millets", "Castor"],
        "guidance": [
            "Correct acidity with lime before major crops.",
            "Apply farmyard manure/compost to build organic matter.",
            "Use a balanced NPK dose and split nitrogen applications.",
            "Consider green manuring (dhaincha/sunhemp) in the off-season.",
        ],
    },
    "grey": {
        "color": "Greyish soil",
        "organic": "Likely low-medium — grey tint can mean seasonal waterlogging.",
        "drainage": "Moderate — may be seasonally waterlogged; improve drainage.",
        "nutrients": {
            "n": ("low", "Likely low", "Waterlogged grey soils can lose nitrogen."),
            "p": ("medium", "Likely medium", "Phosphorus is usually moderate."),
            "k": ("medium", "Likely medium", "Potassium is usually adequate."),
            "ph": ("medium", "Neutral to slightly acidic", "pH is commonly near neutral."),
        },
        "crops": ["Paddy", "Sugarcane", "Jute", "Berseem"],
        "guidance": [
            "Provide field drainage channels to prevent standing water.",
            "Use nitrogen in split doses to avoid losses.",
            "Add organic matter to improve structure and aeration.",
        ],
    },
    "pale": {
        "color": "Pale / whitish soil",
        "organic": "Likely low — pale colour suggests sand or possible salinity.",
        "drainage": "Variable — sandy pale soils drain fast; salt-affected areas drain poorly.",
        "nutrients": {
            "n": ("low", "Likely low", "Pale soils are usually nutrient-poor."),
            "p": ("medium", "Likely medium", "Phosphorus varies."),
            "k": ("high", "Likely high", "Potassium may be high in salt-affected soils."),
            "ph": ("high", "Likely alkaline", "White crust suggests alkalinity/salinity."),
        },
        "crops": ["Barley", "Beetroot", "Date palm", "Salt-tolerant fodder"],
        "guidance": [
            "Get a lab salinity (EC) test — white crust may indicate salt accumulation.",
            "Improve drainage and leach salts with good-quality water where possible.",
            "Use salt-tolerant crops/varieties and add organic matter.",
            "Avoid over-irrigation that raises salts to the surface.",
        ],
    },
    "olive": {
        "color": "Mixed / greenish-tinted soil",
        "organic": "Likely medium — mixed hue, possibly organic-rich or moist.",
        "drainage": "Moderate — check for standing moisture.",
        "nutrients": {
            "n": ("medium", "Likely medium", "Mixed soils usually fall in the middle range."),
            "p": ("medium", "Likely medium", "Phosphorus expected moderate."),
            "k": ("medium", "Likely medium", "Potassium expected moderate."),
            "ph": ("medium", "Neutral", "pH likely near neutral."),
        },
        "crops": ["Rice", "Wheat", "Maize", "Vegetables"],
        "guidance": [
            "Confirm actual NPK/pH with a lab test before major fertiliser decisions.",
            "Maintain balanced fertilisation and add organic matter.",
        ],
    },
}


def _texture_hint(gray_std):
    if gray_std > 0.16:
        return "Coarse / grainy — suggests a sandy texture that drains and dries fast."
    if gray_std < 0.08:
        return "Fine / smooth — suggests a clayey texture that holds water but can compact."
    return "Even grain — suggests a balanced loamy texture."


def visual_classification(rgb, filename):
    """Visual soil analysis from a photo (colour + texture heuristics).

    Honest: the output is a *visual estimate* from colour and texture. It is a
    useful first hint but is NOT a lab analysis and never claims exact NPK/pH.
    """
    small = Image.fromarray(rgb.astype("uint8")).convert("RGB").resize((160, 160))
    arr = np.asarray(small, dtype=np.float32)
    hsv = np.asarray(Image.fromarray(arr.astype("uint8")).convert("HSV"), dtype=np.float32)
    h = hsv[..., 0]
    s = hsv[..., 1]
    v = hsv[..., 2]

    v_mean = float(v.mean())
    s_mean = float(s.mean())
    dark_fraction = float((v < 60).mean())
    bright_fraction = float((v > 205).mean())

    mask = (v >= 40) & (v <= 230)
    if mask.sum() > 0:
        h_mean = float(np.average(h[mask], weights=s[mask] + 1.0))
    else:
        h_mean = 128.0

    if dark_fraction > 0.45:
        family = "black"
    elif s_mean < 45 and v_mean > 190:
        family = "pale"
    elif s_mean < 45:
        family = "grey"
    elif h_mean < 12:
        family = "red"
    elif h_mean < 42:
        family = "brown"
    elif h_mean < 62:
        family = "yellow"
    else:
        family = "olive"

    gray = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    profile = _SOIL_PROFILES[family]

    nutrients = {}
    for key, (status, label, note) in profile["nutrients"].items():
        nutrients[key] = {
            "status": status,
            "label": label,
            "note": note,
            "percent": 62 if status == "medium" else 30 if status == "low" else 88,
        }

    return {
        "engine": "visual-analysis (soil colour + texture)",
        "engine_note": "This is a visual estimate from the photo's colour and texture — useful as a first hint, but NOT a lab result. For exact NPK and pH, test a soil sample at a soil-testing lab.",
        "soil_color": profile["color"],
        "texture": _texture_hint(float(gray.std()) / 255.0),
        "organic_matter": profile["organic"],
        "drainage": profile["drainage"],
        "likely_nutrients": nutrients,
        "suitable_crops": profile["crops"],
        "guidance": profile["guidance"],
        "validated": True,
        "file": filename,
    }
