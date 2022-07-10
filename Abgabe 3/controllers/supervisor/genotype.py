import numpy as np


def generate():
	matrix = np.random.rand(Genotype.rows, Genotype.columns)

	return Genotype(matrix)


def set_fitness_function(fitness_func):
	Genotype.fitness_func = fitness_func


def set_m_n(rows, columns):
	Genotype.rows = rows
	Genotype.columns = columns


class Genotype:
	# Matrixgrößen
	fitness_func = None
	rows, columns = 0, 0

	def __init__(self, weight_matrix):
		self.weight_matrix = weight_matrix
		self.fitness = Genotype.fitness_func(weight_matrix)

	def __repr__(self):
		return "Individual/genotype = " + self.weight_matrix + " Fitness = " + str(self.fitness)
