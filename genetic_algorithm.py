from pyevolve import G2DList
from pyevolve import GSimpleGA
from operator import mul
import sys


# Import Configuration Settings
from ga_config import *
from miller import *

def fitness_func( chromosome ):

	score = 0.0
	p=int(''.join(str(x) for x in chromosome[0]))
	q=int(''.join(str(x) for x in chromosome[1]))
	product=str(p*q)
	for agene, rgene in zip( str( product )[::-1], str( target )[::-1] ):
		if agene != rgene:
			score += 1
	score+=abs(target-p*q)		
	last_p=p%10
	last_q=q%10
	if ((last_p*last_q)%10)==(target%10):
		score-=2
	'''	
	if(not isPrime(p,16) and score>0):
		score-=0.5
	if(not isPrime(q,16) and score>0):
		score-=0.5				
	'''
		
	try:		
		if(target%p==0 and p!=1):
			score=0
		if(target%q==0 and q!=1):
			score=0
	except:
		a=''
	print(str(p)+" "+str(q)+" "+str(score))					
	return score

def ConvergenceCriteria(ga_engine):
   #print(ga_engine.bestIndividual())
   print("******");
   return False

if __name__ == '__main__':
	# Genome Instance
	genome = G2DList.G2DList(list_height,list_width)
	genome.evaluator.set( fitness_func )
	genome.setParams(rangemin=0, rangemax=9)
	genome.setParams(bestrawscore=0, rounddecimal=2)
	genome.setParams(tournamentPool=2)
	genome.crossover.set(crossover_method)
	genome.initializator.set(initializator_method)
	# Create Genetic Algorithm Engine
	ga = GSimpleGA.GSimpleGA( genome )
	ga.setPopulationSize( population_size )
	ga.setMinimax( minimax )
	ga.setElitismReplacement( elitism )
	ga.selector.set( selector_method )

	ga.setCrossoverRate( crossover_rate )
	ga.setMutationRate( mutation_rate )
	#ga.terminationCriteria.set(ConvergenceCriteria)
	ga.setGenerations( generation_count )	
	ga.setMultiProcessing( flag = False, full_copy = False )	
	ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
	ga.initialize()
	ga.evolve( freq_stats = 1)
	print( ga.bestIndividual() )

