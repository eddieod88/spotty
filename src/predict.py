from pathlib import Path
import pickle
import os

import torch

from src.data.numpy_data_loader import SimpleNumpyDataset
from src.models.net import Net, NetPostClaire
from src.train import BATCH_SIZE, IMAGE_DIMENSIONS

ROOT = Path(__file__).parents[1]


def main(model_path, test_dir, results_dir):
    # Load model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = NetPostClaire(BATCH_SIZE, IMAGE_DIMENSIONS)
    model.load_state_dict(torch.load(model_path))
    model.to(device)
    # Prepare test dataset and loader
    testset = SimpleNumpyDataset(str(test_dir))
    testloader = torch.utils.data.DataLoader(testset, batch_size=20, shuffle=False)

    results = []
    print("Running predictions...")
    for data, filename in testloader:
        with torch.no_grad():
            output = model(data)
        results.append((filename[0], output.cpu().numpy()))
    print("Predictions completed.")
    # Save results

    results_path = results_dir / "predictions.pkl"
    with open(results_path, "wb"):
        pickle.dump(results, open(results_path, "wb"))
    print(f"Results saved to {results_path}")


if __name__ == "__main__":
    model = ROOT / "data_collection/spectrograms/models/NetPostClaire_2025_10_10_1.pickle"
    test_dir = ROOT / "data_collection/spectrograms/data/arrays/test_sample"
    results_dir = ROOT / "results"

    main(model, test_dir, results_dir)
