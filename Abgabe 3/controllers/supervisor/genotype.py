import numpy as np


def set_fitness_function(fitness_func):
	Genotype.fitness_func = fitness_func


def generate(m, n):
	matrix = np.random.rand(m, n)

	return Genotype(matrix)


def set_m_n(m, n):
	Genotype.m = m
	Genotype.n = n


class Genotype:
	# Matrixgrößen
	fitness_func = None
	m, n = 0, 0

	def __init__(self, weight_matrix):
		self.weight_matrix = weight_matrix
		self.fitness = Genotype.fitness_func(weight_matrix)

	def __repr__(self):
		return "Individual/genotype = " + self.weight_matrix + " Fitness = " + str(self.fitness)
