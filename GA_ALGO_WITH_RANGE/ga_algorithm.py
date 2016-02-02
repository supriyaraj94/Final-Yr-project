from pyevolve import G1DList
from pyevolve import GSimpleGA
import random
from operator import mul
# Import Configuration Settings
from ga_config import *
def getrange():
	no_of_digits = len(str(square_root))
	min_num = (no_of_digits-1)*10
	max_num = int('9'*no_of_digits)
	return [min_num,max_num]	
def fitness_func( chromosome ):
	score = 0.0
	product = reduce(mul, chromosome, 1)
	for agene, rgene in zip( str( product )[::-1], str( target )[::-1] ):
		if agene == rgene:
			score += 1
	return score
if __name__ == '__main__':
# Genome Instance
	range_of_numbers = getrange()
	genome = G1DList.G1DList( genome_size )
	genome.setParams( rangemin = range_of_numbers[0], rangemax = range_of_numbers[1] )
	genome.evaluator.set( fitness_func )
	# Create Genetic Algorithm Engine
	ga = GSimpleGA.GSimpleGA( genome )
	ga.setPopulationSize( population_size )
	ga.setMinimax( minimax )
	ga.setElitismReplacement( elitism )
	ga.selector.set( selector_method )
	ga.setCrossoverRate( crossover_rate )
	ga.setMutationRate( mutation_rate )
	ga.setGenerations( generation_count )
	ga.setMultiProcessing( flag = True, full_copy = False )
	# ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
	# ga.initialize() --> Initializes the GA Engine. Create and initialize population
	ga.evolve( freq_stats = 10)
	print( ga.bestIndividual() )
