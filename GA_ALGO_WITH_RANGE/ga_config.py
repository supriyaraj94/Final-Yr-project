from pyevolve import Consts
from pyevolve import Initializators
from pyevolve import Selectors
from pyevolve import Crossovers
from pyevolve import Mutators
target = int( input("Enter N: ") )
square_root = int(pow(target,0.5))
genome_size = 2
population_size = 20
arangemin = 0
arangemax = 50
generation_count = 10
elitism = 1
crossover_rate = 0.90
mutation_rate = 0.02
minimax = Consts.minimaxType["maximize"]
initializator_method = Initializators.G1DListInitializatorInteger
selector_method = Selectors.GRankSelector
crossover_method = Crossovers.G1DListCrossoverSinglePoint
mutator_method = Mutators.G1DListMutatorSwap
