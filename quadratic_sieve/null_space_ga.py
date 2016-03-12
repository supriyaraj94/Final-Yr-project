from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import GAllele
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import Crossovers
from pyevolve import Selectors
from pyevolve import Consts
import sys, random
from math import sqrt


matrix=[]
prime_length=0
num_length=0

def cartesian_matrix(file):
   """ Read the matrix from the file """
   m=[]
   line=file.read()
   return (eval(line))


def eval_func(chromosome):
   """ The evaluation function """
   global matrix
   global num_length
   global prime_length
   s=[0 for x in range(prime_length)]
   for i in range(len(chromosome)):
      if(chromosome[i]==1):
         s=[(x + y)%2 for x, y in zip(s, matrix[i])] 
   #print(sum(s))           
   return sum(s)


def selector_method(population, **args):
  p=random.random()
  if(p>=0.5):
    population= Selectors.GTournamentSelectorAlternative(population,**args)
  else:
    population= Selectors.GRankSelector(population,**args)
  return population  

   
def main_run():
   global matrix
   global prime_length
   global num_length
   # load the tsp data file
   filehandle = open("null_matrix.txt", "rw")
   matrix = cartesian_matrix(filehandle)
   prime_length=len(matrix[0])
   num_length=len(matrix)

   
   # set the alleles
   setOfAlleles = GAllele.GAlleles()
   for i in xrange(num_length):
      a = GAllele.GAlleleRange(0, 1)
      setOfAlleles.add(a)
      
   genome = G1DList.G1DList(num_length)
   genome.setParams(allele=setOfAlleles)
   genome.setParams(bestrawscore=0, rounddecimal=2)

   genome.evaluator.set(eval_func)
   genome.mutator.set(Mutators.G1DListMutatorAllele)
   genome.initializator.set(Initializators.G1DListInitializatorAllele)
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setGenerations(100000)
   ga.selector.set( selector_method )
   ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.03)
   ga.setPopulationSize(80)

   ga.initialize()
   ga.evolve( freq_stats = 100)
   print( eval_func(ga.bestIndividual() ))

if __name__ == "__main__":
   main_run()