from .genotype import Genotype, set_fitness_function, generate, set_m_n
import numpy as np


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
		genotype_flattened[point] = np.random.Generator.uniform(low=intervall_min, high=intervall_max + 1,
																size=None)

	offspring = genotype_flattened.reshape(Genotype.m, Genotype.n)

	return Genotype(offspring)


class Population:
	generation = 0
	population = []

	def __init__(self,
				 m,  # Zeilen
				 n,  # Spalten
				 fitness_function,
				 init_populations_size=50,
				 fittest_thresh=0.2,
				 elitism_thresh=0.1,
				 mut_prob=0.3):
		self.fitness_function = fitness_function
		self.init_populations_size = init_populations_size
		self.mut_prob = mut_prob
		self.elitism_thresh = elitism_thresh
		self.fittest_thresh = fittest_thresh

		set_m_n(m, n)
		set_fitness_function(self.fitness_function)

	def init_gen(self):
		for i in range(self.init_populations_size):
			Population.population.append(generate())

	# TODO: remove unfit chromosomes and call mutation & crossover
	def survival_of_the_fittest(self):
		new_population = []
		chosen_ones = []
		Population.population.sort(key=lambda chromosome: chromosome.fitness)
		chosen_ones.extend(Population.population[:int(len(Population.population) * self.fittest_thresh)])

		for genotype in chosen_ones:
			probability = np.random.uniform()

			if probability <= self.mut_prob:
				genome = mutate(genotype)
				new_population.append(genome)
			else:
				genome = crossover(genotype, chosen_ones[np.random.randint(low=0, high=len(chosen_ones))])
				new_population.append(genome)

		new_population.extend(self.elitist())

		Population.population = new_population
		Population.generation += 1

	def elitist(self):
		elitist_candidates = Population.population[:int(len(Population.population) * self.elitism_thresh)]
		return elitist_candidates
