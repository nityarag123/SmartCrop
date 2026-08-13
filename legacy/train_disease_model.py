"""Train the PlantVillage disease classifier.

Example:
    python train_disease_model.py --data-dir "C:\\data\\PlantVillage" --epochs 5
"""

import argparse

from disease_model import MODEL_PATH, train


parser = argparse.ArgumentParser(description="Train a PlantVillage disease classifier")
parser.add_argument("--data-dir", required=True, help="Folder containing train/ and valid/")
parser.add_argument("--epochs", type=int, default=5)
parser.add_argument("--output", default=str(MODEL_PATH))
args = parser.parse_args()

result = train(args.data_dir, args.output, args.epochs)
print(
    f"Saved {result['classes']}-class model to {result['model_path']} "
    f"(validation accuracy: {result['validation_accuracy']:.1%})"
)
