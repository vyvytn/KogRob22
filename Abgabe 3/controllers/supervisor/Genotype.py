import random
import numpy as np


def generate():
	matrix = np.random.rand(Genotype.m, Genotype.n)
	fitness = 0

	return Genotype(matrix, fitness)


class Genotype:

	# Matrixgrößen
	m, n = 0

	def __init__(self, weight_matrix, fitness):
		self.weight_matrix = weight_matrix
		self.fitness = fitness

	def __repr__(self):
		return "Individual/genotype = " + self.weight_matrix + " Fitness = " + str(self.fitness)