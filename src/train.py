from datetime import date
from pathlib import Path

import torch
import torch.nn as nn
import torchvision
import torch.optim as optim
import torchvision.transforms as transforms
import torch.nn.functional as F
import numpy as np

from src.data.numpy_data_loader import SimpleNumpyDataset
from src.models.net import Net, NetPostClaire

BATCH_SIZE = 20
IMAGE_DIMENSIONS = (128, 5168)

ROOT = Path(__file__).parents[1]


def save_model(model: nn.Module):
    today = date.today().strftime("%Y_%m_%d")
    model_dir = ROOT / "data_collection/spectrograms/models"
    count_today = len(
        [p for p in Path(model_dir).glob("*") if p.stem.startswith(today)]
    )

    model_path = (
        model_dir / f"{today}_{model.__class__.__name__}_{count_today + 1}"
    ).with_suffix(".pickle")
    print(f"Saving model {model_path}")
    torch.save(model.state_dict(), model_path)


if __name__ == "__main__":
    data_dir = ROOT / "data_collection/spectrograms/data/arrays"
    print(data_dir)

    trainset = SimpleNumpyDataset(str(data_dir / "train_sample"))
    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=BATCH_SIZE, shuffle=True, num_workers=1
    )

    net = NetPostClaire(batch_size=BATCH_SIZE, image_dimensions=IMAGE_DIMENSIONS)
    criterion = nn.MSELoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    print_number = 10
    try:
        print("training...")
        for epoch in range(5):  # loop over the dataset multiple times
            print(f"Epoch {epoch+1}")
            running_loss = 0.0
            for i, data in enumerate(trainloader, 0):
                inputs, labels = data
                labels = inputs  # Autoencoder...
                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                outputs = net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                running_loss += loss.item()
                if i % print_number == 0:
                    print(
                        f"[{epoch + 1}, {i + 1:5d}] loss: {running_loss / print_number:.3f}"
                    )
                    running_loss = 0.0
    except KeyboardInterrupt:
        save_model(net)
    else:
        print("Finished Training")
        save_model(net)
