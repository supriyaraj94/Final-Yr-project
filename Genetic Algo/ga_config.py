from pyevolve import Consts
from pyevolve import Initializators
from pyevolve import Selectors
from pyevolve import Crossovers
from pyevolve import Mutators

import math

target = raw_input( "Enter N: " )
target_len = len( target )
sqrt_target = int( math.sqrt( int( target ) ) )

genome_size = 2
population_size = 100

arangemin = 0
arangemax = 10

generation_count = 500
elitism = 1
crossover_rate = 0.90
mutation_rate = 0.02

minimax = Consts.minimaxType["minimize"]

initializator_method = Initializators.G1DListInitializatorAllele
selector_method = Selectors.GRankSelector
# The crossover mask is generated as a random bit string (binary representation of chromosomes) 
# with each bit chosen at and independent of the others. Can be considered as n-point crossover maybe 
crossover_method = Crossovers.G1DListCrossoverUniform
mutator_method = Mutators.G1DListMutatorAllele
