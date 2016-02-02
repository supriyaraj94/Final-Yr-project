from pyevolve import Consts
from pyevolve import Initializators
from pyevolve import Selectors
from pyevolve import Crossovers
from pyevolve import Mutators
import math

target = int( input("Enter N: ") )
binary_target=bin(target)[2:] 
string_width=int(math.ceil(len(binary_target)/2.0));
string_height=2;
population_size = 20

#arangemin = 1
#arangemax = 10

generation_count = 200
elitism = 1
crossover_rate = 0.80
mutation_rate = 0.02

minimax = Consts.minimaxType["maximize"]

#initializator_method = Initializators.G1DListInitializatorInteger
selector_method = Selectors.GRankSelector
crossover_method = Crossovers.G2DBinaryStringXSingleHPoint
mutator_method = Mutators.G2DBinaryStringMutatorSwap