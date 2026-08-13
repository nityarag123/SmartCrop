"""Train a lightweight pest classifier on the repository's pest image dataset.

Dataset layout: data/pest/pest/train/<class>/*.jpg
Output: artifacts/pest_classifier.joblib  (a scikit-learn RandomForest)

Run:  python -m backend.ml.pest_detection.train
"""
import glob
import os

import joblib
import numpy as np
from PIL import Image as _Img
from PIL import ImageEnhance
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from .features import extract_features, extract_features_from_pixels, load_rgb

_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TRAIN_DIR = os.path.join(_BASE, "data", "pest", "pest", "train")
TEST_DIR = os.path.join(_BASE, "data", "pest", "pest", "test")
ARTIFACT = os.path.join(_BASE, "artifacts", "pest_classifier.joblib")
SEED = 42


def _augmented_variants(rgb):
    """Return the base image plus realistic variations (flips, brightness,
    contrast) so the classifier generalises to real-world photos."""
    base = _Img.fromarray(rgb.astype("uint8"))
    variants = [rgb]
    variants.append(np.asarray(base.transpose(_Img.FLIP_LEFT_RIGHT), dtype=np.float32))
    variants.append(np.asarray(base.transpose(_Img.FLIP_TOP_BOTTOM), dtype=np.float32))
    variants.append(np.asarray(ImageEnhance.Brightness(base).enhance(1.35), dtype=np.float32))
    variants.append(np.asarray(ImageEnhance.Brightness(base).enhance(0.7), dtype=np.float32))
    variants.append(np.asarray(ImageEnhance.Contrast(base).enhance(1.4), dtype=np.float32))
    return variants


def _collect():
    if not os.path.isdir(TRAIN_DIR):
        raise FileNotFoundError(f"Pest training data not found at {TRAIN_DIR}")
    classes = sorted(os.listdir(TRAIN_DIR))
    X, y = [], []
    for label in classes:
        folder = os.path.join(TRAIN_DIR, label)
        if not os.path.isdir(folder):
            continue
        for path in sorted(glob.glob(os.path.join(folder, "*.jpg")) +
                           sorted(glob.glob(os.path.join(folder, "*.jpeg")))):
            try:
                rgb = load_rgb(path)
                for variant in _augmented_variants(rgb):
                    X.append(extract_features_from_pixels(variant))
                    y.append(label)
            except Exception as exc:
                print(f"Skipping {path}: {exc}")
    if not X:
        raise RuntimeError("No usable images found in the training folder")
    return np.asarray(X, dtype=np.float32), np.asarray(y)


def train(output_path=ARTIFACT, test_size=0.2):
    print("Extracting features from pest images...")
    X, y = _collect()
    print(f"Collected {X.shape[0]} images across {len(np.unique(y))} classes")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=SEED, stratify=y
    )
    model = RandomForestClassifier(n_estimators=500, random_state=SEED, n_jobs=-1, min_samples_leaf=1)
    model.fit(X_train, y_train)
    accuracy = float(model.score(X_test, y_test))
    print(f"Validation accuracy (train split): {accuracy:.3f}")
    print(classification_report(y_test, model.predict(X_test)))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump({"model": model, "classes": list(model.classes_), "accuracy": accuracy}, output_path)
    print(f"Saved to {output_path}")

    if os.path.isdir(TEST_DIR):
        print("Evaluating on untouched holdout (data/pest/pest/test)...")
        X_hold, y_hold = [], []
        for label in sorted(os.listdir(TEST_DIR)):
            folder = os.path.join(TEST_DIR, label)
            if not os.path.isdir(folder):
                continue
            for path in sorted(glob.glob(os.path.join(folder, "*.jpg")) +
                               sorted(glob.glob(os.path.join(folder, "*.jpeg")))):
                try:
                    X_hold.append(extract_features(path))
                    y_hold.append(label)
                except Exception as exc:
                    print(f"Skipping {path}: {exc}")
        if X_hold:
            X_hold = np.asarray(X_hold, dtype=np.float32)
            y_hold = np.asarray(y_hold)
            holdout_acc = float(model.score(X_hold, y_hold))
            print(f"Holdout accuracy: {holdout_acc:.3f} ({len(y_hold)} images)")
            print(classification_report(y_hold, model.predict(X_hold)))
    return accuracy


if __name__ == "__main__":
    train()
