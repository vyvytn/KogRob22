from Generation import Generation
from Genotype import Genotype

import numpy as np
from controller import *
import json
import math

chromo_size=4

def fitness_func(self):
    pass
first_gen= Generation (genotype=Genotype(chromo_size), fit_func= fitness_func)

supervisor=Supervisor()
