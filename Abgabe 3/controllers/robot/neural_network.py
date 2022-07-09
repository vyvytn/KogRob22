import torch
from torch import nn


class NeuralNetwork(nn.Module):

    def __init__(self, input_size, output_size, weights):
        super(NeuralNetwork, self).__init__()

        self.layers = nn.Sequential(
            nn.Linear(input_size, output_size),
            nn.Tanh()
        )

        with torch.no_grad():
            self.linear.weight.copy_(weights)

    def forward(self, x):
        logits = self.layers(x)
        return logits