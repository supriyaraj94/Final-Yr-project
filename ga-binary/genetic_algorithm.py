from pyevolve import G2DBinaryString
from pyevolve import GSimpleGA
from operator import mul

# Import Configuration Settings
from ga_config import *

def fitness_func( chromosome ):
	score = 0.0
	p=int(''.join(str(x) for x in chromosome[0]),2)
	q=int(''.join(str(x) for x in chromosome[1]),2)
	product=bin(p*q)[2:] 

	for agene, rgene in zip( str( product )[::-1], str( binary_target )[::-1] ):
		if agene == rgene:
			score += 1

	return score

if __name__ == '__main__':
	# Genome Instance
	genome = G2DBinaryString.G2DBinaryString(string_height,string_width)
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
	ga.setMultiProcessing( flag = False, full_copy = False )	
	print(binary_target)
	# ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
	# ga.initialize() --> Initializes the GA Engine. Create and initialize population
	ga.evolve( freq_stats = 20)
	print( ga.bestIndividual() )
	chromosome=ga.bestIndividual()
	p=int(''.join(str(x) for x in chromosome[0]),2)
	q=int(''.join(str(x) for x in chromosome[1]),2)
	print(p)
	print(q)
	print(p*q)
	print(bin(p*q)[2:])