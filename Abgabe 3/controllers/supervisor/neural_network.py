import torch
from torch import nn


class NeuralNetwork(nn.Module):

	def __init__(self, input_size, output_size):
		super(NeuralNetwork, self).__init__()

		self.linear = nn.Linear(input_size, output_size)
		self.tanh = nn.Tanh()

	def forward(self, x):
		y1 = self.linear(torch.tensor(x))
		y = self.tanh(y1)
		return y

	def set_weights(self, weights):
		self.linear.weight.copy_(torch.tensor(weights))
