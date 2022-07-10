import torch
from torch import nn
import numpy as np

class NeuralNetwork(nn.Module):

	def __init__(self, input_size, output_size, weight):
		super(NeuralNetwork, self).__init__()
		self.weight=weight
		self.linear = nn.Linear(input_size, output_size)
		self.tanh = nn.Tanh()
		with torch.no_grad(): 
			self.linear.weight.copy_(self.weight)
	def forward(self, x):
		x=x.astype(np.float32)
		y1 = self.linear(torch.tensor(x))
		y = self.tanh(y1)
		return y
