import torch

import torch.nn as nn
import torch.nn.functional as F

from ai.building_blocks import BNDoubleConv

class QLearningPolicy(nn.Module):

    def __init__(self, h, w, num_additional_features, outputs):
        super().__init__()

        self.conv1 = BNDoubleConv(1, 16)
        self.conv2 = BNDoubleConv(16, 16)

        #https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
        def conv2d_size_out(size, kernel_size=3, stride=1):
            return (size - (kernel_size - 1) - 1) // stride + 1

        convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(w)))
        convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(h)))
        linear_input_size = convw * convh * 16
        self.fc1 = nn.Linear(linear_input_size + num_additional_features, 256)
        self.fc2 = nn.Linear(256, outputs)

    def forward(self, image, features):
        x = self.conv1(image)
        print(x.shape)
        x = self.conv2(x)
        print(x.shape)
        x = self.conv3(x)
        print(x.shape)
        print(x.flatten().shape)

        return x


if __name__ == "__main__":
    print("making_model")
    model = QLearningPolicy(640, 640, 0, 6)

    print("making_inputs")
    inputs = torch.randn((1, 1, 640, 640))

    model(inputs, None)