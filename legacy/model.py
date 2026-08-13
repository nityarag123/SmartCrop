"""Training and prediction helpers for Farmspace crop recommendations."""
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).parent
DATASET, ARTIFACT = ROOT / "crop_yield_dataset.csv", ROOT / "artifacts" / "crop_recommender.joblib"
FEATURES = ["temperature", "humidity", "rainfall", "ph", "nitrogen", "phosphorus", "potassium"]
DATASET_COLUMNS = ["temperature", "humidity", "rainfall", "ph", "N", "P", "K"]


def train_model(force=False):
    """Train the crop recommender using the supplied Crop_recommendation data."""
    if ARTIFACT.exists() and not force:
        return {"status": "existing", "artifact": str(ARTIFACT)}
    ARTIFACT.parent.mkdir(exist_ok=True)
    frame = pd.read_csv(DATASET)
    required = set(DATASET_COLUMNS + ["label"])
    if not required.issubset(frame.columns):
        raise ValueError(f"Dataset must contain: {', '.join(sorted(required))}")
    frame = frame.rename(columns={"N": "nitrogen", "P": "phosphorus", "K": "potassium", "label": "crop"})
    X_train, X_test, y_train, y_test = train_test_split(
        frame[FEATURES], frame["crop"], test_size=0.2, random_state=42, stratify=frame["crop"]
    )
    model = RandomForestClassifier(n_estimators=150, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, ARTIFACT)
    return {"status": "trained", "rows": len(frame), "crops": frame["crop"].nunique(), "test_accuracy": round(model.score(X_test, y_test), 4), "artifact": str(ARTIFACT)}


def predict_crop(values):
    train_model()
    model = joblib.load(ARTIFACT)
    crop = model.predict(pd.DataFrame([[values[key] for key in FEATURES]], columns=FEATURES))[0]
    confidence = model.predict_proba(pd.DataFrame([[values[key] for key in FEATURES]], columns=FEATURES)).max() * 100
    return {"crop": crop, "confidence": round(confidence, 1), "estimated_yield": round(2.1 + values["rainfall"] / 400 + values["nitrogen"] / 170, 2)}
