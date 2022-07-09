import numpy as np


def generate():
	matrix = np.random.rand(Genotype.m, Genotype.n)

	return Genotype(matrix)


def crossover(mother, father):
	mother_flattened = mother.flatten()
	father_flattened = father.flatten()

	crossover_point = mother_flattened.size // 2

	offspring_a = np.append(mother_flattened[:crossover_point], father_flattened[crossover_point:]) \
		.reshape(Genotype.m, Genotype.n)
	offspring_b = np.append(mother_flattened[:crossover_point], father_flattened[crossover_point:]) \
		.reshape(Genotype.m, Genotype.n)

	return Genotype(offspring_a), Genotype(offspring_b)


def mutate(genotype):
	genotype_flattened = genotype.flattened()

	# Defining maximum mutation points in the array
	maximum_mutation_percentage = 0.2
	mutation_points = np.random.randint(low=1, high=int(maximum_mutation_percentage * Genotype.m * Genotype.n))

	# Defining the interval of numbers possible to use for mutation
	max_number_in_array = np.amax(genotype_flattened)
	min_number_in_array = np.amin(genotype_flattened)

	# Quelle: https://de.wikipedia.org/wiki/Mutation_(evolution%C3%A4rer_Algorithmus)#Mutation_ohne_Ber%C3%BCcksichtigung_von_Restriktionen
	sigma = (max_number_in_array - min_number_in_array) / 6
	intervall_min = -3 * sigma
	intervall_max = 3 * sigma

	list_of_points_to_mutate = np.random.randint(low=0, high=genotype_flattened.size - 1, size=mutation_points)

	for point in list_of_points_to_mutate:
		genotype_flattened[point] = np.random.Generator.uniform(low=intervall_min, high=intervall_max + 1, size=None)

	offspring = genotype_flattened.reshape(Genotype.m, Genotype.n)

	return Genotype(offspring)


def set_fitness_function(fitness_func):
	Genotype.fitness_func = fitness_func


class Genotype:
	# Matrixgrößen
	m, n = 0, 0  # m: Zeilen, n: Spalten
	fitness_func = None

	def __init__(self, weight_matrix):
		self.weight_matrix = weight_matrix
		self.fitness = Genotype.fitness_func(weight_matrix)

	def __repr__(self):
		return "Individual/genotype = " + self.weight_matrix + " Fitness = " + str(self.fitness)
