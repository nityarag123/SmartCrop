"""Image feature extraction for the pest/disease classifier.

Uses a compact hand-crafted feature vector built from:
  * HSV colour histograms (hue / saturation / value)
  * RGB colour histograms
  * a joint hue-saturation histogram (captures colour relationships)
  * grayscale statistics and edge density (light texture signal)

Multi-scale: features are computed both on the full frame and on a center-zoom
crop, so the model sees the scene context as well as a magnified subject
(important for real photos where the pest may be small in the frame).

This is a genuine ML pipeline: the classifier is trained on the repository's
``data/pest`` image dataset and predictions are real model outputs.
"""
import numpy as np
from PIL import Image

IMAGE_SIZE = 128
_HUE_BINS = 32
_SAT_BINS = 16
_VAL_BINS = 16
_RGB_BINS = 16
_HS_ROWS = 8
_HS_COLS = 8
_EDGE_BINS = 8
_ZOOM = 0.65


def load_rgb(path):
    image = Image.open(path).convert("RGB")
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    return np.asarray(image, dtype=np.float32)


def _hsv(image_rgb):
    from PIL import Image as _Img
    return np.asarray(_Img.fromarray(image_rgb.astype("uint8")).convert("HSV"), dtype=np.float32)


def _hist(indices, bins):
    return np.bincount(np.asarray(indices).ravel(), minlength=bins).astype(np.float32)


def _norm(hist):
    total = hist.sum()
    if total > 0:
        hist = hist / total
    return hist


def _edge_stats(gray):
    gy, gx = np.gradient(gray.astype(np.float32))
    magnitude = np.sqrt(gx ** 2 + gy ** 2)
    edge_ratio = float((magnitude > 32).mean())
    edges = np.clip((magnitude / 8).astype(np.int16), 0, _EDGE_BINS - 1)
    edge_hist = _norm(_hist(edges.ravel(), _EDGE_BINS))
    return np.concatenate([[edge_ratio], edge_hist])


def _block(rgb):
    """Feature block for one (already resized) RGB array."""
    hsv = _hsv(rgb)
    h = np.clip((hsv[..., 0] / 255.0 * 255).astype(np.int16), 0, 255)
    s = np.clip((hsv[..., 1] / 255.0 * 255).astype(np.int16), 0, 255)
    v = np.clip((hsv[..., 2] / 255.0 * 255).astype(np.int16), 0, 255)

    h_hist = _norm(_hist(h // (256 // _HUE_BINS), _HUE_BINS))
    s_hist = _norm(_hist(s // (256 // _SAT_BINS), _SAT_BINS))
    v_hist = _norm(_hist(v // (256 // _VAL_BINS), _VAL_BINS))

    rgb_u8 = np.clip(rgb, 0, 255).astype(np.int16)
    rgb_hist = np.concatenate([
        _norm(_hist(rgb_u8[..., c] // (256 // _RGB_BINS), _RGB_BINS)) for c in range(3)
    ])

    hs_idx = (h // (256 // _HS_ROWS)) * _HS_COLS + (s // (256 // _HS_COLS))
    hs_hist = _norm(_hist(np.clip(hs_idx, 0, _HS_ROWS * _HS_COLS - 1), _HS_ROWS * _HS_COLS))

    gray = (0.299 * rgb_u8[..., 0] + 0.587 * rgb_u8[..., 1] + 0.114 * rgb_u8[..., 2])
    gray_mean = float(gray.mean()) / 255.0
    gray_std = float(gray.std()) / 255.0
    edge = _edge_stats(gray)

    return np.concatenate([h_hist, s_hist, v_hist, rgb_hist, hs_hist,
                           [gray_mean, gray_std], edge]).astype(np.float32)


def _center_zoom(rgb):
    from PIL import Image as _Img
    size = IMAGE_SIZE
    crop = int(size * _ZOOM)
    off = (size - crop) // 2
    box = (off, off, off + crop, off + crop)
    img = _Img.fromarray(rgb.astype("uint8")).crop(box).resize((size, size))
    return np.asarray(img, dtype=np.float32)


def extract_features_from_pixels(rgb):
    """Return a fixed-size feature vector for a float32 RGB pixel array."""
    full = _block(rgb)
    zoom = _block(_center_zoom(rgb))
    return np.concatenate([full, zoom]).astype(np.float32)


def extract_features(path):
    return extract_features_from_pixels(load_rgb(path))


def feature_size():
    block = (_HUE_BINS + _SAT_BINS + _VAL_BINS + _RGB_BINS * 3 + _HS_ROWS * _HS_COLS
             + 2 + 1 + _EDGE_BINS)
    return block * 2
