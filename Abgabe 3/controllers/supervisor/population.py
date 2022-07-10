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
		genotype_flattened[point] = np.random.Generator.uniform(low=intervall_min, high=intervall_max + 1, size=None)

	offspring = genotype_flattened.reshape(Genotype.m, Genotype.n)

	return Genotype(offspring)


def get_change(current, previous):
	if current == previous:
		return 0
	try:
		return (abs(current - previous) / previous) * 100.0
	except ZeroDivisionError:
		return float('inf')


class Population:

	def __init__(self,
				 rows,  # Zeilen
				 columns,  # Spalten
				 fitness_function,
				 init_populations_size=50,
				 fittest_thresh=0.2,
				 elitism_thresh=0.1,
				 mut_prob=0.3,
				 max_last_best=10):
		self.fitness_function = fitness_function
		self.init_populations_size = init_populations_size
		self.mut_prob = mut_prob
		self.elitism_thresh = elitism_thresh
		self.fittest_thresh = fittest_thresh
		self.max_last_best = max_last_best

		self.last_x_best_fitness = []
		self.population = []
		self.generation = 0

		set_m_n(rows, columns)
		set_fitness_function(self.fitness_function)

	def init_gen(self):
		for i in range(self.init_populations_size):
			self.population.append(generate())

	def best_fitness(self):
		if len(self.population) == 0:
			return None

		if len(self.last_x_best_fitness) >= self.max_last_best:
			self.last_x_best_fitness.clear()

		self.last_x_best_fitness.append(
			max(self.population, key=lambda individual: individual.fitness)
		)

	def survival_of_the_fittest(self):
		new_population = []
		chosen_ones = []
		Population.population.sort(key=lambda individual: individual.fitness, reverse=True)
		chosen_ones.extend(Population.population[:int(len(Population.population) * self.fittest_thresh)])

		for genotype in chosen_ones:
			probability = np.random.uniform()

			if probability <= self.mut_prob:
				genome = mutate(genotype)
				new_population.append(genome)
			else:
				chosen_ones_without_genotype = chosen_ones
				chosen_ones_without_genotype.remove(genotype)
				offspring_one, offspring_two = crossover(genotype,
														chosen_ones_without_genotype[np.random.randint(low=0, high=len(
															chosen_ones_without_genotype) - 1)])
				new_population.extend([offspring_one, offspring_two])

		new_population.extend(self.elitist())

		Population.population = new_population
		self.generation += 1

	def elitist(self):
		elitist_candidates = self.population[:int(len(self.population) * self.elitism_thresh)]
		return elitist_candidates

	def exit_loop(self):
		if len(self.last_x_best_fitness) == self.max_last_best:
			if get_change(self.last_x_best_fitness[-1], self.last_x_best_fitness[0]) <= 0.01:
				return True

		return False

	def run(self):
		self.init_gen()
		self.best_fitness()

		while not self.exit_loop():
			self.survival_of_the_fittest()
			self.best_fitness()

		return max(self.population, key=lambda individual: individual.fitness)
