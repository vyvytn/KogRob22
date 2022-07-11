from turtle import update
from genotype import Genotype, set_fitness_function, generate, set_m_n
import numpy as np
import numpy as np
import time
import matplotlib.pyplot as plt

ax = plt.axes()
hl = plt.plot([], [])[0]

"""
Crossover algorithm for two individuals
"""


def crossover(mother, father):
	mother_flattened = mother.weight_matrix.flatten()
	father_flattened = father.weight_matrix.flatten()

	crossover_point = mother_flattened.size // 2

	offspring_a = np.append(mother_flattened[:crossover_point], father_flattened[crossover_point:]) \
		.reshape(Genotype.rows, Genotype.columns)
	offspring_b = np.append(mother_flattened[:crossover_point], father_flattened[crossover_point:]) \
		.reshape(Genotype.rows, Genotype.columns)

	return Genotype(offspring_a), Genotype(offspring_b)


"""
Mutation algorithm for a genotype
"""


def mutate(genotype):
	genotype_flattened = genotype.weight_matrix.flatten()

	# Defining maximum mutation points in the array
	maximum_mutation_percentage = 0.2
	mutation_points = np.random.randint(low=1, high=int(maximum_mutation_percentage * Genotype.rows * Genotype.columns))

	# Defining the interval of numbers possible to use for mutation
	max_number_in_array = np.amax(genotype_flattened)
	min_number_in_array = np.amin(genotype_flattened)

	# Quelle: https://de.wikipedia.org/wiki/Mutation_(evolution%C3%A4rer_Algorithmus)#Mutation_ohne_Ber%C3%BCcksichtigung_von_Restriktionen
	sigma = (max_number_in_array - min_number_in_array) / 6
	intervall_min = -3 * sigma
	intervall_max = 3 * sigma

	list_of_points_to_mutate = np.random.randint(low=0, high=genotype_flattened.size - 1, size=mutation_points)

	for point in list_of_points_to_mutate:
		genotype_flattened[point] = np.random.uniform(low=intervall_min, high=intervall_max + 1, size=None)
	offspring = genotype_flattened.reshape(Genotype.rows, Genotype.columns)
	print('finished for loop')
	return Genotype(offspring)


"""
Calculates percentage change between two fitness scores
"""


def get_change(current, previous):
	if current.fitness == previous.fitness:
		return 0
	try:
		return (abs(current.fitness - previous.fitness) / previous.fitness) * 100.0
	except ZeroDivisionError:
		return float('inf')


class Population:

	def __init__(self,
				 rows,  # Zeilen
				 columns,  # Spalten
				 fitness_function,
				 init_populations_size=30,
				 fittest_thresh=0.4,
				 elitism_thresh=0.6,
				 mut_prob=0.8,
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

	def update_diagramm(self, hl, fit_val):
		hl.set_xdata(np.append(hl.get_xdata(), self.generation))
		hl.set_ydata(np.append(hl.get_ydata(), fit_val))

		ax.relim()
		ax.autoscale_view()

		plt.draw()
		plt.savefig('foo.png')

	"""
	Checks if <last_x_best_fitness> fitness scores are already saved.
	If yes, clears array and appends maximum of this generation
	"""

	def best_fitness(self):
		if len(self.population) == 0:
			return None

		if len(self.last_x_best_fitness) >= self.max_last_best:
			self.last_x_best_fitness.clear()

		self.last_x_best_fitness.append(
			max(self.population, key=lambda individual: individual.fitness)
		)
		self.update_diagramm(hl, self.last_x_best_fitness[-1].fitness)
		print('best fitness')

	"""
	Chooses the best <fittest_thresh> % of the population of current generation.
	Those 'chosen ones' are then mutated or crossovered with some probability defined in <mut_prob>.
	Also the best <elitism_thresh> are also added to the next generation without any alteration of the genomes.
	"""

	def survival_of_the_fittest(self):
		new_population = []
		chosen_ones = []
		self.population.sort(key=lambda individual: individual.fitness, reverse=True)
		if len(self.population) < 20:
			chosen_ones = self.population
		else:
			chosen_ones.extend(self.population[:int(len(self.population) * self.fittest_thresh)])
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
															 chosen_ones_without_genotype))])
				new_population.extend([offspring_one, offspring_two])

		new_population.extend(self.elitist())

		self.population = new_population
		self.generation += 1
		print('current generation: ', self.generation)

	"""
	Chooses the best <elitism_thresh> % of the population and returns them to be added to the new population.
	"""

	def elitist(self):
		elitist_candidates = self.population[:int(len(self.population) * self.elitism_thresh)]
		return elitist_candidates

	"""
	Exit condition of loop in run()
	If first documented fitness score and 10th documented fitness score are less than 1% different,
	the loop should be exited.
	The last ten fitness scores are documented in the array named last_x_best_fitness.
	"""

	def exit_loop(self):
		if len(self.last_x_best_fitness) == self.max_last_best:
			if get_change(self.last_x_best_fitness[-1], self.last_x_best_fitness[0]) <= 0.1:
				return True
		elif self.generation >= 40:
			return True

		return False

	"""
	Run loop for generations
	"""

	def run(self):
		self.init_gen()
		self.best_fitness()

		# while not self.exit_loop():
		for i in range(2):
			self.survival_of_the_fittest()
			self.best_fitness()
		print('FINISHED')
		return max(self.population, key=lambda individual: individual.fitness)
