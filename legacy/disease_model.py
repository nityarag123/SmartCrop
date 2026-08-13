"""PlantVillage disease model training and inference helpers.

The dataset must be organised as ``<data-dir>/train/<class>/*.jpg`` and
``<data-dir>/valid/<class>/*.jpg`` (or ``test`` in place of ``valid``). The class names are kept in the exported
checkpoint so browser uploads always use the same label order as training.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


MODEL_PATH = Path("models/plant_disease_model.pt")
IMAGE_SIZE = 224


def _torch_components():
    """Import the optional ML dependencies only when a model is used."""
    try:
        import torch
        from torch import nn
        from torchvision import models, transforms
    except ImportError as exc:
        raise RuntimeError(
            "PyTorch is not installed. Run `pip install -r requirements.txt`."
        ) from exc
    return torch, nn, models, transforms


def build_model(class_count: int):
    """Create a transfer-learning classifier suitable for PlantVillage images."""
    _, nn, models, _ = _torch_components()
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, class_count)
    return model


def train(data_dir: str | Path, output_path: str | Path = MODEL_PATH, epochs: int = 5):
    """Train and export a PlantVillage classifier; returns final validation accuracy."""
    torch, nn, _, transforms = _torch_components()
    from torch.utils.data import DataLoader
    from torchvision.datasets import ImageFolder

    root = Path(data_dir)
    train_dir = root / "train"
    valid_dir = root / "valid"
    if not valid_dir.is_dir():
        valid_dir = root / "test"
    if not train_dir.is_dir() or not valid_dir.is_dir():
        raise ValueError("Expected train and valid (or test) directories below the dataset folder.")

    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    training = ImageFolder(train_dir, transform=transform)
    validation = ImageFolder(valid_dir, transform=transform)
    if training.classes != validation.classes:
        raise ValueError("Train and valid folders must contain identical class names.")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_model(len(training.classes)).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()
    train_loader = DataLoader(training, batch_size=32, shuffle=True, num_workers=0)
    valid_loader = DataLoader(validation, batch_size=32, num_workers=0)

    for _ in range(epochs):
        model.train()
        for images, labels in train_loader:
            optimizer.zero_grad()
            loss = criterion(model(images.to(device)), labels.to(device))
            loss.backward()
            optimizer.step()

    model.eval()
    correct = total = 0
    with torch.no_grad():
        for images, labels in valid_loader:
            predictions = model(images.to(device)).argmax(dim=1).cpu()
            correct += (predictions == labels).sum().item()
            total += labels.numel()

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"classes": training.classes, "state_dict": model.cpu().state_dict()}, output)
    return {"classes": len(training.classes), "validation_accuracy": correct / total, "model_path": str(output)}


def predict(image_path: str | Path, model_path: str | Path = MODEL_PATH) -> dict[str, Any]:
    """Return a disease label and calibrated softmax confidence for one image."""
    torch, _, _, transforms = _torch_components()
    from PIL import Image

    checkpoint_path = Path(model_path)
    if not checkpoint_path.is_file():
        raise FileNotFoundError("Disease model is not trained yet.")
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    classes = checkpoint["classes"]
    model = build_model(len(classes))
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert("RGB")
    with torch.no_grad():
        probabilities = torch.softmax(model(transform(image).unsqueeze(0))[0], dim=0)
    index = int(probabilities.argmax())
    label = classes[index].replace("___", " — ").replace("_", " ")
    return {"label": label, "confidence": round(float(probabilities[index]), 4)}
