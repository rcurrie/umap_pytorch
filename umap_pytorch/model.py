import torch
import torch.nn as nn
import numpy as np

# 1. Determine the best available device
device = None
if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")


class conv_encoder(nn.Module):
    def __init__(self, n_components=2):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=64,
                kernel_size=3,
                stride=2,
                padding=1,
            ),
            nn.Conv2d(
                in_channels=64,
                out_channels=128,
                kernel_size=3,
                stride=2,
                padding=1,
            ),
            nn.Flatten(),
            nn.Linear(6272, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, n_components),
        ).to(
            device
        )  # Changed .cuda() to .to(device)

    def forward(self, X):
        return self.encoder(X)


class default_encoder(nn.Module):
    def __init__(self, dims, n_components=2):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Flatten(),
            nn.Linear(np.prod(dims), 200),
            nn.ReLU(),
            nn.Linear(200, 200),
            nn.ReLU(),
            nn.Linear(200, 200),
            nn.ReLU(),
            nn.Linear(200, n_components),
        ).to(
            device
        )  # Changed .cuda() to .to(device)

    def forward(self, X):
        return self.encoder(X)


class default_decoder(nn.Module):
    def __init__(self, dims, n_components):
        super().__init__()
        self.dims = dims
        self.decoder = nn.Sequential(
            nn.Linear(n_components, 200),
            nn.ReLU(),
            nn.Linear(200, 200),
            nn.ReLU(),
            nn.Linear(200, 200),
            nn.ReLU(),
            nn.Linear(200, np.prod(dims)),
        ).to(
            device
        )  # Changed .cuda()

    def forward(self, X):
        return self.decoder(X).view(X.shape[0], *self.dims)


if __name__ == "__main__":
    model = conv_encoder(2)
    print(model.parameters)
    print(model(torch.randn((12, 1, 28, 28)).to(device)).shape)
