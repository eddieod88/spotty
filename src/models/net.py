import torch.nn as nn


class AutoEncoder1D(nn.Module):
    def __init__(self, input_size, latent_size):
        # input size will be 128
        # latent size maybe 10?  10 dimensions to do similarities within? could be decent.
        # ignore the convolution transpose in the decoder as I don't think it's needed. BUT WHAT DO I KNOW AY?
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=3, stride=2, padding=1),
            nn.Conv1d(16, 32, kernel_size=3, stride=2, padding=1),
            nn.Flatten(),
            nn.Linear(32 * (input_size // 4), 64),
            nn.ReLU(),
            nn.Linear(64, latent_size),
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_size, 64),
            nn.ReLU(),
            nn.Linear(64, input_size),
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x



class Net(nn.Module):
    def __init__(self, batch_size, image_dimensions):
        super().__init__()
        conv_stride = 5
        # maybe increase the kernel size
        conv_kernel_size = 20
        # increase number of layers and step down to as small a CNN as possible before flattening
        # DO MORE STEPS
        conv_padding = 1
        # batch norm?..............
        # tsne, RNN...

        def calc_flattened_size(image_dimensions):
            h, w = image_dimensions

            # First Conv2d + MaxPool2d
            h = (h + 2 * 3 - 7) // 3 + 1  # Conv2d
            w = (w + 2 * 3 - 7) // 3 + 1
            h = h // 2  # MaxPool2d(2)
            w = w // 2

            # Second Conv2d + MaxPool2d
            h = (h + 2 * 1 - 3) // 1 + 1
            w = (w + 2 * 1 - 3) // 1 + 1
            h = h // 2
            w = w // 2

            # Third Conv2d + MaxPool2d
            h = (h + 2 * 1 - 3) // 1 + 1
            w = (w + 2 * 1 - 3) // 1 + 1
            h = h // 2
            w = w // 2

            # Output channels after last Conv2d is 256
            return 256 * h * w

        self.flattened_size = calc_flattened_size(image_dimensions)
        self.flattened_size = 16 * 128 * 5168

        self.encoder = nn.Sequential(
            nn.Conv2d(
                1,
                8,
                stride=3,
                kernel_size=7,
                padding=3,
            ),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(
                8,
                16,
                stride=1,
                kernel_size=3,
                padding=1,
            ),
            nn.ReLU(),
            nn.MaxPool2d(2),
            # nn.Conv2d(
            #     128,
            #     256,
            #     stride=1,
            #     kernel_size=3,
            #     padding=1,
            # ),
            # nn.ReLU(),
            # nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(self.flattened_size, 1000),
            nn.BatchNorm1d(1000),
            nn.ReLU(),
            nn.Linear(1000, 2),
        )

        self.decoder = nn.Sequential(
            nn.Linear(2, 1000),
            nn.BatchNorm1d(1000),
            nn.ReLU(),
            nn.Linear(1000, self.flattened_size),
            nn.BatchNorm1d(self.flattened_size),
            nn.ReLU(),
            # nn.Upsample(scale_factor=2),
            # nn.ConvTranspose2d(
            #     256,
            #     128,
            #     stride=1,
            #     kernel_size=3,
            #     padding=1,
            # ),
            # nn.ReLU(),
            nn.Upsample(scale_factor=2),
            nn.ConvTranspose2d(
                16,
                8,
                stride=1,
                kernel_size=3,
                padding=1,
            ),
            nn.ReLU(),
            nn.Upsample(scale_factor=2),
            nn.ConvTranspose2d(
                8,
                1,
                stride=3,
                kernel_size=7,
                padding=3,
            ),
            nn.ReLU(),
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x


class NetPostClaire(nn.Module):
    def __init__(self, batch_size, image_dimensions):
        super().__init__()
        channels = [1, 8, 16]
        conv_layers = []
        h, w = image_dimensions

        kernel_size = 5
        stride = 2
        padding = 2

        # Encoder: Drop down through 5 conv layers with BatchNorm and MaxPool2d(2)
        for i in range(len(channels) - 1):
            conv_layers.append(
                nn.Conv2d(
                    channels[i],
                    channels[i + 1],
                    kernel_size=kernel_size,
                    stride=stride,
                    padding=padding,
                )
            )
            conv_layers.append(nn.BatchNorm2d(channels[i + 1]))
            conv_layers.append(nn.ReLU())
            # conv_layers.append(nn.MaxPool2d(2))

        self.encoder_conv = nn.Sequential(*conv_layers)

        def calc_out_size(size, layers):
            for _ in range(layers):
                size = (size + 2 * padding - kernel_size) // stride + 1
                # size = size // 2  # MaxPool2d(2)
            return size

        out_h = calc_out_size(h, len(channels) - 1)
        out_w = calc_out_size(w, len(channels) - 1)
        flattened_size = channels[-1] * out_h * out_w

        self.input_shape = (batch_size, channels[0], h, w)

        self.encoder_fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(flattened_size, 1000),
            nn.BatchNorm1d(1000),
            nn.ReLU(),
            nn.Linear(1000, 2),
        )

        self.decoder_fc = nn.Sequential(
            nn.Linear(2, 1000),
            nn.BatchNorm1d(1000),
            nn.ReLU(),
            nn.Linear(1000, flattened_size),
            nn.BatchNorm1d(flattened_size),
            nn.ReLU(),
        )

        decoder_channels = list(reversed(channels))
        deconv_layers = []
        for i in range(len(decoder_channels) - 1):
            deconv_layers.append(
                nn.ConvTranspose2d(
                    decoder_channels[i],
                    decoder_channels[i + 1],
                    kernel_size=kernel_size,
                    stride=stride,
                    padding=padding,
                    output_padding=1,
                )
            )
            if i < len(decoder_channels) - 2:
                deconv_layers.append(nn.BatchNorm2d(decoder_channels[i + 1]))
            deconv_layers.append(nn.ReLU())

        self.decoder_conv = nn.Sequential(*deconv_layers)

        self.out_shape = (channels[-1], out_h, out_w)

    def forward(self, x):
        x = self.encoder_conv(x)
        x = self.encoder_fc(x)
        x = self.decoder_fc(x)
        x = x.view(-1, *self.out_shape)
        x = self.decoder_conv(x)
        target_w = self.input_shape[3]
        current_w = x.shape[-1]
        if current_w > target_w:
            x = x[..., :target_w]
        elif current_w < target_w:
            pad = target_w - current_w
            x = nn.functional.pad(x, (0, pad), mode="constant", value=0)
        return x
