import random
import numpy as np
import Genotype 

class Generation:

    def __init__(self,
                #genotype: Genotype,
                fit_func,
                generations=30,
                population_size=50,
                mut_prob=0.25,
                selection_size=4,
                elite_thresh=0.4):
        self.population_size = population_size
        self.mut_prob = mut_prob
        self.selection_size = selection_size
        #self.genotype = genotype
        self.fit_func = fit_func
        self.elite_thresh=elite_thresh,
        self.generations=generations

    def init_gen(self):
        """
        TODO: generate LIST of weight matrices with random numbers as a RETURN
        TODO: init Genotypes/Chromosomes for each individual
        list size is number og population
        """
        init_weights=[]
        genotype=Genotype(4,5)
        for i in range(self.population_size):
            init_weights.append(self.genotype.generate_weights())    
        return init_weights

    """
    -method calculates for each indiviual a fitness score
    - takes as input ONE SINGLE weight matrix
    - this matrix will be emitted to walking.py (controller) and from there will further pass to NN
    """
    def calc_fitness_indiv(self, weight):
        fitness_score=self.fit_func(weight)
        return fitness_score
    """
    -calculates list of fitness scores for WHOLE generation
    -input is a LIST of weight matrices
    -list has size of population size
    """
    def calc_fittness_gen(self, weights):
        generation_fitness=[]
        for weight in len(weights):
            generation_fitness.append(self.fit_func(weight))
        return generation_fitness

    def mutate_indiv(self, chromo):
        random_gen= random.randint(0, self.genotype.size-1)
        mutate_gen= 1 if chromo[random_gen]== 0 else 1
        chromo[random_gen]=mutate_gen
        return chromo

    def crossover (self, mother, father):
        half=self.genotype.size/2
        child_gens=[]
        for i in enumerate(half):
            mother_gens= np.random.choice(mother.shape[0], half, replace=False)  
        #change genes
        return child_gens

    # list of weights
    #TODO
    def evolution(self, weights):

        for i in range(self.generations):
            new_generation=self.survival_of_fittest(new_generation)
            generation_counter+=1
        
        list_of_elite_weights=[]

        generation_fitness=self.calc_fittness_gen(weights)
        half= weights.size/2
        elite=self.get_fittest(weights)
        for i,indiv in range(0,elite.size, 2):
            mother= elite[i]
            father=elite[i+1]
            child=self.crossover(mother, father)
            child=self.mutate_indiv(child)
            new_gen.append(child)
        #mutation
        best_chromosome=0
        return best_chromosome

    """
    method will be calles in EACH generation
    calculates fitness and calls selection function where next generation will be produced
    """
    def survival_of_fittest(self, generation):
        new_generation=[]
        generation_fitness=self.calc_fittness_gen(generation)

        #best individual with HIGHEST/ BEST fitness
        best_individual=max(generation_fitness)
        #add best indivudal to new generation WITHOUT crossover and mutation
        new_generation.append(np.array(best_individual))

        #rest of new generation will  be created through mutation and crossover
        new_generation.append(self.selection(generation, generation_fitness))
        return new_generation

    """
    TODO selectio
    """
    def selection(self, generation, generation_fitness):
        parents = []
        #select top n (selection_size) indivudals from generation for reproducing
        idx_best = np.argpartition(generation_fitness, -self.selection_size)[-self.selection_size:]
        top_n_individuals = generation[idx_best]
        
        #select also random parents for reproducing
        parents = np.random.choice(self.population_size, self.tournamentSize)
        for i in range(self.tournamentSize):
            parentList.append(bestIndex.index(parents[i]))
        parentList = np.argsort(np.array(parentList))
        parent1 = pop[parents[parentList[0]]]
        parent2 = pop[parents[parentList[1]]]

        child = self.Crossover(parent1,parent2)
        if random.random() > self.mutate_chance:
            child = self.Mutate(child)
        return childss

    """
    - starts method of Generation/ Population class
    - calls initial weights and start the evolution loop
    - evolution loop returns ONE BEST weight matrix
    - this matrix will be returned to the supervisor and later emitted to the neural network 
    """
    def reproduce(self):
        init_weights = self.init_gen()
        best_weight_matrix= self.evolution(init_weights)
        return best_weight_matrix
    