from pyevolve import G1DList
from pyevolve import GSimpleGA
from operator import mul

# Import Configuration Settings
from ga_config import *

def fitness_func( chromosome ):
	score = 0.0
	product = reduce(mul, chromosome, 1)

	for agene, rgene in zip( str( product )[::-1], str( target )[::-1] ):
		if agene == rgene:
			score += 1
	print(str(chromosome[0])+" "+str(chromosome[1]))		
	return score
def ConvergenceCriteria(ga_engine):
   #print(ga_engine.bestIndividual())
   print("******");
   return False	

if __name__ == '__main__':
	# Genome Instance
	genome = G1DList.G1DList( genome_size )
	genome.setParams( rangemin = arangemin, rangemax = arangemax )
	genome.evaluator.set( fitness_func )

	# Create Genetic Algorithm Engine
	ga = GSimpleGA.GSimpleGA( genome )
	ga.setPopulationSize( population_size )
	ga.setMinimax( minimax )
	ga.setElitismReplacement( elitism )
	ga.selector.set( selector_method )
	ga.setCrossoverRate( crossover_rate )
	ga.setMutationRate( mutation_rate )
	ga.terminationCriteria.set(ConvergenceCriteria)
	ga.setGenerations( generation_count )	
	ga.setMultiProcessing( flag = True, full_copy = False )	
	
	# ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
	# ga.initialize() --> Initializes the GA Engine. Create and initialize population

	ga.evolve( freq_stats = 10)
	print( ga.bestIndividual() )
