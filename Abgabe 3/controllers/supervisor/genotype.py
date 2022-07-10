import numpy as np

"""
Generates a weight matrix
"""
def generate():
	matrix = np.random.rand(Genotype.rows, Genotype.columns)

	return Genotype(matrix)


"""
Sets the fitness function to be used to calculate fitness
"""
def set_fitness_function(fitness_func):
	Genotype.fitness_func = fitness_func


"""
Sets the class variables m, n (width and height of weight matrix) 
"""
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
		print(self.__repr__(self))

	def __repr__(self):
		return "Individual/genotype = " + self.weight_matrix + " Fitness = " + str(self.fitness)
