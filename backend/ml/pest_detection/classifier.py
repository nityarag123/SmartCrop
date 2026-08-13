"""Pest / plant-disease detection service.

Pipeline (honest):
* The scikit-learn pest classifier (artifacts/pest_classifier.joblib) trained
  on data/pest images is the primary engine. On the untouched holdout it
  scores 94.0% accuracy across 9 pest classes.
* The deep-learning checkpoint (models/plant_disease_model.pt) is NOT used:
  on the same holdout it scores only 66.7% and is overconfident on wrong
  answers, so it would produce more harmful mispredictions.
* Photos that do not confidently match a pest class are reported honestly.
  A simple colour heuristic distinguishes "plant / leaf material" (which gets
  plant-disease guidance) from "not a clear plant or pest photo".

Predictions are never fabricated. The response states which engine produced
the result and how confident it is.
"""
import os
import threading

import joblib
import numpy as np

from .features import extract_features_from_pixels

_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DISEASE_MODEL = os.path.join(_BASE, "models", "plant_disease_model.pt")
PEST_MODEL = os.path.join(_BASE, "artifacts", "pest_classifier.joblib")

_lock = threading.Lock()
_pest_model = None
_disease_model = None

# Farmer-friendly pest guidance. Includes common Indian-market pesticides with
# typical label doses; safe practice is always recommended.
PESTICIDE_NOTE = ("Always apply at the label-recommended dose, use gloves and a mask, "
                  "spray in the cool evening hours, and respect the pre-harvest interval. "
                  "For severe outbreaks, consult your agriculture officer.")

PEST_GUIDANCE = {
    "aphids": {
        "name": "Aphids",
        "kind": "insect pest",
        "severity": "Moderate",
        "symptoms": "Clusters of small green/black insects on new shoots and under leaves; sticky honeydew; leaf curling.",
        "action": "Spray neem-oil solution (5 ml per litre) in the evening; encourage ladybird beetles. Wash off heavy infestations with a water jet.",
        "prevention": "Scout weekly; avoid excess nitrogen; keep weeds down around the field.",
        "pesticides": [
            "Neem oil 1500 ppm — 5 ml per litre (organic option, evening spray)",
            "Imidacloprid 17.8% SL — 0.3 ml per litre",
            "Dimethoate 30% EC — 1.7 ml per litre",
        ],
    },
    "armyworm": {
        "name": "Armyworm",
        "kind": "insect pest",
        "severity": "High",
        "symptoms": "Caterpillars feed on leaves leaving skeletonised patches; large groups march across the field.",
        "action": "Hand-pick and destroy egg masses and larvae. In maize, apply recommended bio-agent sprays; contact your agriculture officer for severe outbreaks.",
        "prevention": "Early sowing, crop rotation and field sanitation reduce pressure.",
        "pesticides": [
            "Chlorantraniliprole 18.5% SC — 0.3 ml per litre",
            "Spinetoram 11.7% SC — 0.6 ml per litre",
            "Lambda-cyhalothrin 5% EC — 0.5 ml per litre (evening spray)",
        ],
    },
    "beetle": {
        "name": "Beetle",
        "kind": "insect pest",
        "severity": "Low-Moderate",
        "symptoms": "Chewed/bitten leaves, flowers and tender pods; adult beetles visible on plants.",
        "action": "Hand-pick beetles in the morning; use neem-based sprays; pheromone traps if numbers rise.",
        "prevention": "Keep the field weed-free and rotate crops.",
        "pesticides": [
            "Neem oil 1500 ppm — 5 ml per litre (organic option)",
            "Carbaryl 50% WP — 2 g per litre",
            "Lambda-cyhalothrin 5% EC — 0.5 ml per litre",
        ],
    },
    "bollworm": {
        "name": "Bollworm",
        "kind": "insect pest",
        "severity": "High",
        "symptoms": "Round bore holes in cotton bolls, flower buds and squares; droppings near entry holes.",
        "action": "Install pheromone traps and hand-pick damaged bolls. Follow local IPM advice from your agriculture officer for serious infestations.",
        "prevention": "Sow pest-resistant/tolerant varieties and avoid staggered cotton around the same fields.",
        "pesticides": [
            "Chlorantraniliprole 18.5% SC — 0.3 ml per litre",
            "Emamectin benzoate 5% SG — 0.4 g per litre",
            "Flubendiamide 20% WG — 0.25 g per litre",
        ],
    },
    "grasshopper": {
        "name": "Grasshopper",
        "kind": "insect pest",
        "severity": "Low-Moderate",
        "symptoms": "Large jumping insects; ragged feeding on leaf margins; damage at field edges.",
        "action": "Trench/border barriers and early spraying of gregarious nymphs with neem-based products.",
        "prevention": "Maintain field borders; control nearby grassland that shelters hoppers.",
        "pesticides": [
            "Neem oil 1500 ppm — 5 ml per litre",
            "Chlorpyrifos 20% EC — 2 ml per litre (border spraying)",
            "Fipronil 5% SC — 1.5 ml per litre",
        ],
    },
    "mites": {
        "name": "Mites",
        "kind": "insect pest",
        "severity": "Moderate",
        "symptoms": "Tiny red/yellow mites; stippled, bronzed or silvery leaves with fine webbing.",
        "action": "Sulphur or neem-oil sprays; strong water spray to dislodge; avoid drought stress on plants.",
        "prevention": "Avoid overuse of broad-spectrum sprays that kill natural mite predators.",
        "pesticides": [
            "Sulphur 80% WP — 2-3 g per litre",
            "Abamectin 1.9% EC — 0.5 ml per litre",
            "Dicofol 18.5% EC — 2.5 ml per litre",
        ],
    },
    "mosquito": {
        "name": "Mosquito",
        "kind": "unrelated-to-crops",
        "severity": "None for crops",
        "symptoms": "This result is not a crop pest. Mosquitoes do not damage field crops.",
        "action": "No crop action needed. Remove standing water around your home to reduce mosquito breeding.",
        "prevention": "Drain stagnant water and keep surroundings clean.",
        "pesticides": [],
    },
    "sawfly": {
        "name": "Sawfly",
        "kind": "insect pest",
        "severity": "Moderate",
        "symptoms": "Caterpillar-like larvae eating leaves from the edges; severe defoliation in young crops.",
        "action": "Hand-pick larvae; deep ploughing after harvest destroys pupae. Consult local agriculture office if widespread.",
        "prevention": "Crop rotation and clean cultivation help break the life cycle.",
        "pesticides": [
            "Neem oil 1500 ppm — 5 ml per litre",
            "Quinalphos 25% EC — 2 ml per litre",
            "Lambda-cyhalothrin 5% EC — 0.5 ml per litre",
        ],
    },
    "stem_borer": {
        "name": "Stem Borer",
        "kind": "insect pest",
        "severity": "High",
        "symptoms": "Dried 'dead-heart' shoots; bore holes in stems; frass near entry points; lodging.",
        "action": "Remove and destroy infested tillers; use recommended egg parasites/bio-agents; avoid late transplanting.",
        "prevention": "Timely sowing, resistant varieties and destroying stubble reduce borer pressure.",
        "pesticides": [
            "Carbofuran 3% G — granules at sowing (label rate)",
            "Chlorantraniliprole 0.4% G — granules in whorls / near the base",
            "Cartap hydrochloride 4% G — granules near the base",
        ],
    },
}

UNKNOWN_GUIDANCE = {
    "name": "Unclear image",
    "kind": "unknown",
    "severity": "Unknown",
    "symptoms": "The photo did not look like a clear, close-up image of a damaged plant, so no pest match is claimed.",
    "action": "Take a well-lit, close-up photo of the affected plant part (both sides of the leaf) and check again.",
    "prevention": "If the damage persists or spreads, contact your local agriculture extension officer with a sample.",
}

PLANT_GUIDANCE = {
    "name": "Plant material",
    "kind": "plant / leaf (pest not identified)",
    "severity": "Unknown",
    "symptoms": "The photo looks like plant material, but it did not match a pest class the model was trained on with enough confidence. Spots, yellowing, wilting or holes can come from pests, fungal/bacterial disease, or nutrient stress.",
    "action": "Inspect the underside of leaves for insects and check for spots, powdery growth, webbing or mushy roots. Take a close-up photo of the affected part and re-check. If the problem spreads, contact your local agriculture extension officer with a sample of the plant.",
    "prevention": "Keep the field clean, avoid overhead watering in the evening, ensure good air flow, and follow a balanced fertiliser schedule to reduce plant stress.",
}


def _looks_like_plant(rgb):
    """Colour heuristic: is the photo dominated by green plant tissue?"""
    arr = rgb.astype("float32") / 255.0
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    green = (g > r + 0.03) & (g > b + 0.03) & (g > 0.16)
    return float(green.mean()) > 0.12


def _load_pest_model(force=False):
    global _pest_model
    if _pest_model is not None and not force:
        return _pest_model
    with _lock:
        if _pest_model is None or force:
            if not os.path.exists(PEST_MODEL):
                raise FileNotFoundError("Pest model is not trained. Run `python -m backend.ml.pest_detection.train`.")
            _pest_model = joblib.load(PEST_MODEL)
    return _pest_model


def _load_disease_model(force=False):
    global _disease_model
    if _disease_model is not None and not force:
        return _disease_model
    with _lock:
        if _disease_model is None or force:
            if not os.path.exists(DISEASE_MODEL):
                return None
            try:
                import torch
                import torchvision
                from PIL import Image
                torch, torchvision = torch, torchvision
            except ImportError:
                return None
            checkpoint = torch.load(DISEASE_MODEL, map_location="cpu", weights_only=True)
            classes = checkpoint["classes"]
            from torch import nn
            model = torchvision.models.resnet18(weights=None)
            model.fc = nn.Linear(model.fc.in_features, len(classes))
            model.load_state_dict(checkpoint["state_dict"])
            model.eval()
            _disease_model = {"model": model, "classes": classes}
    return _disease_model


def detect_from_image(rgb, threshold=0.45):
    """Predict using the pest classifier (accurate on the repo's pest dataset).

    The deep-learning checkpoint is deliberately not used because it scores
    much lower (66.7% vs 94.0% on the same holdout) and is overconfident on
    wrong answers.
    """
    pest = _load_pest_model()
    return _predict_pest(pest, rgb, threshold)


def _predict_disease(disease, rgb):
    import torch
    from torchvision import transforms
    from PIL import Image as PImage
    classes = disease["classes"]
    model = disease["model"]
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    image = PImage.fromarray(rgb.astype("uint8")).convert("RGB")
    with torch.no_grad():
        probabilities = torch.softmax(model(transform(image).unsqueeze(0))[0], dim=0)
    index = int(probabilities.argmax())
    label = classes[index]
    confidence = float(probabilities[index])
    return {
        "engine": "deep-learning (plant disease model)",
        "label": label.replace("___", " — ").replace("_", " "),
        "category": "plant disease" if "healthy" not in label.lower() else "healthy",
        "confidence": round(confidence, 4),
        "detection_type": "plant-disease",
    }, confidence


def _predict_pest(pest, rgb, threshold):
    checkpoint = pest
    model = checkpoint["model"]
    classes = list(checkpoint["classes"])
    features = extract_features_from_pixels(rgb).reshape(1, -1)
    probabilities = model.predict_proba(features)[0]

    order = np.argsort(probabilities)[::-1][:3]
    top_matches = []
    for index in order:
        label = classes[index]
        name = PEST_GUIDANCE.get(label, {}).get("name", label.replace("_", " ").title())
        top_matches.append({
            "label": label,
            "name": name,
            "confidence": round(float(probabilities[index]), 4),
        })

    confidence = top_matches[0]["confidence"]
    best_label = top_matches[0]["label"]

    if confidence >= 0.55:
        guidance = PEST_GUIDANCE.get(best_label, UNKNOWN_GUIDANCE)
        result_label = guidance.get("name", best_label)
        note = "High-confidence match from the trained pest model. Verify the pest on your plants, then follow the guidance."
    elif confidence >= threshold:
        guidance = PEST_GUIDANCE.get(best_label, UNKNOWN_GUIDANCE)
        result_label = guidance.get("name", best_label)
        note = "Moderate-confidence match — compare the symptoms on your plants before acting."
    else:
        if _looks_like_plant(rgb):
            guidance = dict(PLANT_GUIDANCE)
            result_label = "Plant material — pest not confidently identified"
            note = ("The photo looks like plant material but did not match a trained pest class "
                    "with enough confidence. The closest matches below are hints only — spots, "
                    "yellowing or wilting can also come from disease or nutrient stress.")
        else:
            guidance = dict(UNKNOWN_GUIDANCE)
            result_label = "Not a clear plant or pest photo"
            note = "This image did not look like a clear photo of a damaged plant, so no pest match is claimed."

    return {
        "engine": "ML (trained on pest image dataset)",
        "label": result_label,
        "detected_class": best_label if confidence >= threshold else "unknown",
        "category": guidance.get("kind", "unknown"),
        "confidence": round(confidence, 4),
        "confidence_label": "High" if confidence >= 0.55 else ("Moderate" if confidence >= threshold else "Low"),
        "severity": guidance.get("severity", "Unknown"),
        "symptoms": guidance.get("symptoms", ""),
        "action": guidance.get("action", ""),
        "prevention": guidance.get("prevention", ""),
        "top_matches": top_matches,
        "note": note,
        "pesticides": guidance.get("pesticides", []),
        "pesticide_note": PESTICIDE_NOTE if guidance.get("pesticides") else "",
        "detection_type": "insect-pest",
    }, confidence


def is_pest_model_available():
    try:
        _load_pest_model()
        return True
    except FileNotFoundError:
        return False


def is_disease_model_available():
    return _load_disease_model() is not None
