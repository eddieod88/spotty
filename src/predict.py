from pathlib import Path
import pickle
import os

import torch

from src.data.numpy_data_loader import SimpleNumpyDataset
from src.models.net import Net, NetPostClaire, AutoEncoder1D
from src.train import BATCH_SIZE, IMAGE_DIMENSIONS, INPUT_SIZE, LATENT_SIZE

ROOT = Path(__file__).parents[1]


def main(model_path, test_dir, results_dir, results_name):
    # Load model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoEncoder1D(input_size=INPUT_SIZE, latent_size=LATENT_SIZE)
    model.load_state_dict(torch.load(model_path))
    model.to(device)
    # Prepare test dataset and loader
    testset = SimpleNumpyDataset(str(test_dir))
    testloader = torch.utils.data.DataLoader(testset, batch_size=1, shuffle=False)

    results = []
    print("Running predictions...")
    for data, filename in testloader:
        with torch.no_grad():
            output = model(data)
        results.append((filename[0], output.cpu().numpy()))
    print("Predictions completed.")
    # Save results

    results_path = results_dir / results_name
    with open(results_path, "wb"):
        pickle.dump(results, open(results_path, "wb"))
    print(f"Results saved to {results_path}")


if __name__ == "__main__":
    model = ROOT / "data_collection/spectrograms/models/2025_10_30_AutoEncoder1D_1.pickle"
    test_dir = ROOT / "data_collection/spectrograms/data/arrays/test_sample_averaged"
    results_dir = ROOT / "results"
    results_name = "autoencoder1d_test_results.pkl"

    main(model, test_dir, results_dir, results_name)
