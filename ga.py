from pyevolve import G2DList
from pyevolve import GSimpleGA
from operator import mul
from pyevolve import DBAdapters
import sys
import timeit
from after_ga import *

# Import Configuration Settings
from ga_config import *
from miller import *

def fitness_func( chromosome ):

	score = 0.0
	p=int(''.join(str(x) for x in chromosome[0]))
	q=int(''.join(str(x) for x in chromosome[1]))
	product=str(p*q)
    	co = len(product)
	if(co != len(str(target))):
		score += co*10
	for agene, rgene in zip( str( product )[::-1], str( target )[::-1] ):
		if agene != rgene:
			score += co*co
            		co = co - 1
	#score+=abs(target-p*q)		
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
		global found		
		if(target%p == 0 and p != 1):
			score=0
            		found = 1
		if(target%q==0 and q!=1):
			score=0
            		found = 1
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
    	start = timeit.default_timer()
	genome = G2DList.G2DList(list_height,list_width)
	genome.evaluator.set( fitness_func )
	genome.setParams(rangemin=0, rangemax=9)
	genome.setParams(bestrawscore=0, rounddecimal=2)
	genome.setParams(tournamentPool=5)
	genome.crossover.set(crossover_method)
	genome.mutator.set(mutator_method)
	genome.initializator.set(initializator_method)
	# Create Genetic Algorithm Engine
	ga = GSimpleGA.GSimpleGA( genome )
    	ga.setMultiProcessing()
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
    	sqlite_adapter = DBAdapters.DBSQLite(identify="ex1",resetDB=True)
    	ga.setDBAdapter(sqlite_adapter)
	ga.initialize()
	try:
		ga.evolve( freq_stats = 1)
	except:
		pass
    	final_genome = ga.bestIndividual()
    	h,w = final_genome.getSize()
    	for j in range(0,w):
       		num1 = num1+str(final_genome.getItem(0,j))
        	num2 = num2+str(final_genome.getItem(1,j))
	if(target%long(num1)==0):
		num2 = str(target/long(num1))
	else:
		num1 = str(target/long(num2))
	print( final_genome )
	stop = timeit.default_timer()
	if(found != 1):
		find_primes(long(num1),long(num2),target,stop-start)
	print ("Number of digits : "+str(len(str(target))))
	print ("The prime factors are : "+num1+" "+num2)
	print ("Time Taken : "+str(stop-start))
