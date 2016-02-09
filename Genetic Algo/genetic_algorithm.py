from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import GAllele
from operator import mul

# Fast prime number generator python library
from primesieve import *

# Import configuration settings
from ga_config import *

# Fitness function: compares number of matching digits
def fitness_func_similar_digits( chromosome ):
	score = 0.0
	product = str( reduce(mul, chromosome, 1) )
	
	if len( product ) != target_len:
		return target_len - score  

	for rgene, agene in zip( target[::-1], product[::-1] ):
		if agene == rgene:
			score += 1

	return target_len - score

# Fitness function: returns absolute difference
def fitness_func_difference( chromosome ):
	product = reduce(mul, chromosome, 1)
	return abs(int( target ) - product)

# To set initial population to only primes!
def initial_range( sqrt_target ):
	# To produce almost equal sized primes for initialization
	p_range = generate_primes(10 ** (len( str( sqrt_target ) ) - 1), sqrt_target)
	q_range = generate_primes(sqrt_target, (10 ** len( str( sqrt_target ) ) - 1))

	return (p_range, q_range)

if __name__ == '__main__':
	# Allele choices
	alleles = GAllele.GAlleles()
	p_range, q_range = initial_range( sqrt_target )
	p_choice = GAllele.GAlleleList( p_range )
	q_choice = GAllele.GAlleleList( q_range )
	alleles.add( p_choice )
	alleles.add( q_choice )


	# Genome Instance
	genome = G1DList.G1DList( genome_size )
	genome.setParams( allele = alleles )
	# One or more fitness function
	genome.evaluator.set( fitness_func_similar_digits )
	genome.evaluator.add( fitness_func_difference )

	genome.initializator.set( initializator_method )
	genome.crossover.set( crossover_method )
	genome.mutator.set( mutator_method )
	

	# Create Genetic Algorithm Engine
	ga = GSimpleGA.GSimpleGA( genome )
	ga.selector.set( selector_method )
	ga.setPopulationSize( population_size )
	ga.setMinimax( minimax )
	ga.setElitismReplacement( elitism )
	ga.setCrossoverRate( crossover_rate )
	ga.setMutationRate( mutation_rate )
	
	ga.setGenerations( generation_count )	
	#ga.setMultiProcessing(flag = True, full_copy = False)	
	
	# ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)
	# ga.initialize() --> Initializes the GA Engine. Create and initialize population

	ga.evolve( freq_stats = 10)
	print( ga.bestIndividual() )