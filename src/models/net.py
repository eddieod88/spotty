import torch.nn as nn

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

        self.encoder = nn.Sequential(
            nn.Conv2d(
                1,
                8,
                stride=conv_stride,
                kernel_size=conv_kernel_size,
                padding=conv_padding,
            ),
            nn.ReLU(),
            nn.Conv2d(
                8,
                16,
                stride=conv_stride,
                kernel_size=conv_kernel_size,
                padding=conv_padding,
            ),
            
            nn.Flatten(),
            nn.Linear(batch_size * 10584064, 2),
        )
        self.decoder = nn.Sequential(
            nn.Linear(2, 10584064 * batch_size),
            nn.Unflatten(1, (16, *image_dimensions)),
            nn.ConvTranspose2d(
                16,
                8,
                kernel_size=conv_kernel_size,
                stride=conv_stride,
                padding=conv_padding,
            ),
            nn.ReLU(),
            nn.ConvTranspose2d(
                8,
                1,
                kernel_size=conv_kernel_size,
                stride=conv_stride,
                padding=conv_padding,
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
        channels = [1, 8, 16, 32, 64, 128]
        conv_layers = []
        h, w = image_dimensions

        kernel_size = 5
        stride = 2
        padding = 2

        # Encoder: Drop down through 5 conv layers with BatchNorm
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

        self.encoder_conv = nn.Sequential(*conv_layers)

        def calc_out_size(size, layers):
            for _ in range(layers):
                size = (size + 2 * padding - kernel_size) // stride + 1
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
