"""Offline farm-assistant fallback.

A transparent rule/knowledge-based assistant used when no LLM key is
configured. It answers common questions about crops, soil, pests, weather,
schemes and farming practice using built-in agricultural knowledge. It is NOT
described as an LLM. It clearly states uncertainty and never fabricates
weather, schemes, or dangerous pesticide instructions.
"""
import re
from datetime import date

CROP_KEYWORDS = {
    "rice": ["rice", "paddy", "chawal"],
    "wheat": ["wheat", "gehu", "aata"],
    "maize": ["maize", "corn", "makkai", "bhutta"],
    "sugarcane": ["sugarcane", "ganna", "cane"],
    "cotton": ["cotton", "kapas"],
    "groundnut": ["groundnut", "peanut", "mungfali"],
    "potato": ["potato", "aloo", "aalu"],
    "tomato": ["tomato", "tamatar"],
    "onion": ["onion", "pyaaz", "kanda"],
}

CROP_ANSWERS = {
    "rice": "Rice grows best in warm, humid conditions (25-35 C) in soil that holds water. It needs lots of water — transplant seedlings into a flooded field and split nitrogen in three doses (transplanting, tillering, panicle initiation). Harvest about 120-140 days after sowing.",
    "wheat": "Wheat suits cool weather (15-25 C) and well-drained loam soil. Irrigate at crown-root, flowering and grain-filling stages. Top-dress nitrogen at crown root and tillering. Harvest when the straw turns yellow, around 110-130 days after sowing.",
    "maize": "Maize likes warm weather (20-35 C) and needs moisture at knee-high, tasseling and silking. Give basal phosphorus and split nitrogen before tasseling. Watch for stem borer and fall armyworm. Harvest 100-120 days after sowing.",
    "sugarcane": "Sugarcane needs deep well-drained soil, warmth and lots of water over 10-12 months. Plant healthy setts with 2-3 buds. Irrigate regularly and keep an eye on shoot borer and red rot.",
    "cotton": "Cotton suits warm weather (25-35 C) and deep black or well-drained loam soil. Avoid waterlogging. Monitor bollworm, jassids and whitefly from flowering onwards. Pick bolls as they open.",
    "groundnut": "Groundnut grows in light, well-drained sandy loam. Apply gypsum at flowering. Irrigate lightly but keep moisture at peg and pod-filling stages. Harvest when haulms yellow and pods mature.",
    "potato": "Potato needs loose, well-drained sandy loam and cool weather (15-22 C). Use disease-free seed tubers. Do light, frequent irrigation; watch for late blight. Harvest after haulms dry and skins set.",
    "tomato": "Tomato prefers well-drained loam with pH 6-7. Transplant 25-30 day seedlings, stake the plants, and give regular light water. Watch for fruit borer and blight. Pick fruits at the pink/breaker stage.",
    "onion": "Onion grows in loose, well-drained soil in cool-dry weather. Regular but light irrigation; stop watering near maturity. Watch for thrips and purple blotch.",
}


def _normalize(text):
    return re.sub(r"[^a-z0-9 ]", " ", text.lower()).strip()


def _find_crop(text):
    text = _normalize(text)
    for crop, keywords in CROP_KEYWORDS.items():
        if any(k in text for k in keywords):
            return crop
    return None


def _classify(message):
    text = _normalize(message)
    if any(k in text for k in ["hello", "hi ", "namaste", "namaskar", "hey", "salaam"]):
        return "greeting"
    if any(k in text for k in ["soil", "khad", "fertilizer", "fertiliser", "nutrient", "n-p-k", "npk", "ph level"]):
        return "soil"
    if any(k in text for k in ["pest", "insect", "disease", "leaf spot", "fungus", "rot", "borer", "kita", "rugna"]):
        return "pest"
    if any(k in text for k in ["weather", "rain", "rainfall", "temperature", "forecast", "mausam", "barish"]):
        return "weather"
    if any(k in text for k in ["scheme", "subsidy", "yojana", "sarkari", "grant", "kisan"]):
        return "scheme"
    if any(k in text for k in ["which crop", "recommend", "suitable", "grow", "plant", "crop"]):
        return "crop"
    if any(k in text for k in ["water", "irrigation", "drip", "sinchai"]):
        return "water"
    if any(k in text for k in ["help", "what can you", "options", "menu", "kya kar"]):
        return "help"
    return "unknown"


def _context_block(user):
    if not user:
        return ""
    parts = []
    if user.get("location"):
        parts.append(f"The farmer is located in {user.get('location')}.")
    if user.get("current_crop"):
        parts.append(f"They are currently growing {user.get('current_crop')}.")
    if user.get("farm_size"):
        parts.append(f"Farm size is {user.get('farm_size')}.")
    return " ".join(parts)


def answer(message, user=None):
    category = _classify(message)
    context = _context_block(user)

    if category == "greeting":
        reply = "Hello! I am the SmartCrop farm assistant. Ask me about crops, soil, pests, weather or government schemes. For example: 'Which crop suits my soil?'"
        return reply, category

    if category == "help":
        reply = ("You can ask me things like:\n"
                 "- Which crop should I grow?\n"
                 "- How do I grow wheat?\n"
                 "- My soil has low nitrogen, what should I do?\n"
                 "- What are the symptoms of stem borer?\n"
                 "- Will it rain tomorrow?\n"
                 "- What is PM-KISAN?")
        return reply, category

    if category == "soil":
        reply = ("Good soil care starts with a test. Ideal values: pH 6.5-7.5, nitrogen 30-60 kg/ha, "
                 "phosphorus 15-40 kg/ha, potassium 30-70 kg/ha. If nitrogen is low, add urea/DAP at the "
                 "recommended stage; if pH is acidic, apply lime; if alkaline, add organic matter and gypsum. "
                 "Use the Soil Analysis page in SmartCrop to check your levels.")
        return reply, category

    if category == "pest":
        crop = _find_crop(message)
        crop_note = f" For {crop}," if crop else ""
        reply = (f"Most crop problems can be managed by early detection{crop_note}: inspect your plants weekly, "
                 "remove badly affected parts, and start with safe options like neem-oil spray (5 ml per litre) "
                 "in the evening. For serious or spreading damage, contact your local agriculture extension "
                 "officer — they will recommend the correct, registered treatment. Upload a clear photo in the "
                 "Pest Detection page for an AI check.")
        return reply, category

    if category == "weather":
        reply = ("I can't predict the weather on my own. Open the Weather page in SmartCrop and choose your "
                 "state and district to see current conditions and the forecast. Use that to plan irrigation "
                 "and harvesting.")
        return reply, category

    if category == "scheme":
        reply = ("Popular central schemes: PM-KISAN (Rs 6,000/year income support), PMFBY (crop insurance), "
                 "Kisan Credit Card (cheap crop loans), PMKSY (irrigation support), Soil Health Card (free soil "
                 "testing). See the Schemes page in SmartCrop for full details and the official websites to apply. "
                 "State schemes differ by state — ask your district agriculture office.")
        return reply, category

    if category == "crop":
        crop = _find_crop(message)
        if crop and crop in CROP_ANSWERS:
            return CROP_ANSWERS[crop], category
        reply = ("The best crop depends on your soil nutrients, pH, temperature and rainfall. Enter these in the "
                 "Crop Recommendation page and SmartCrop's AI model will suggest the best crop for your conditions.")
        return reply, category

    if category == "water":
        reply = ("Smart irrigation: water at the crop's critical stages (germination, flowering, grain filling) "
                 "rather than every day. Drip/sprinkler systems save 30-50% water. Match irrigation to rainfall — "
                 "check the Weather page first.")
        return reply, category

    reply = (
        "I'm not sure about that one. I'm a farming assistant — I can help with crops, soil, pests, "
        "weather planning and government schemes. For example, try 'How do I grow rice?' "
        "or 'Which crop suits my soil?'. For serious crop problems, contact your local agriculture officer. "
        f"{context}".strip()
    )
    return reply, category
