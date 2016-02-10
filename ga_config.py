#user-defined crossover/selector


from pyevolve import Consts
from pyevolve import Initializators
from pyevolve import Selectors
from pyevolve import Crossovers
from pyevolve import Mutators
from prime_generator import *
import random
import math
from pyevolve import Util

target = int( input("Enter N: ") )
list_width=int(math.ceil(len(str(target))/2.0));
list_height=2;
population_size = 30
prime_list=list(set(primesfrom2to(math.pow(10,list_width)))-set(primesfrom2to(math.pow(10,list_width-1))))
number_of_primes=len(prime_list)


generation_count = 100
elitism = 1
crossover_rate = 0.6
mutation_rate = 0.5

minimax = Consts.minimaxType["minimize"]

selector_method = Selectors.GTournamentSelector
mutator_method = Mutators.G2DListMutatorSwap
#crossover_method=Crossovers.G2DListCrossoverUniform
last_digits=dict()
last_digits[1]=[[1,1],[3,7],[7,3]]
last_digits[3]=[[1,3],[3,1],[9,7],[7,9]]
last_digits[7]=[[1,7],[7,1],[9,3],[3,9]]
last_digits[9]=[[1,9],[9,1],[3,3]]



def initializator_method(genome, **args):
    genome.clearList()
    #while(True):
    p=prime_list[random.randint(0,int((number_of_primes-1)/2))]
    q=prime_list[random.randint(int((number_of_primes-1)/2),number_of_primes-1)]
    '''
        if ((p%10) * (q%10))!= (target%10):
            continue
        else:
            break 
    '''       
    l=[]
    l.append( [int(char) for char in str(p)])
    l.append( [int(char) for char in str(q)])
    for i in xrange(genome.getHeight()):
        for j in xrange(genome.getWidth()):
            genome.setItem(i, j, l[i][j])

def reinitializator_method(genome, **args):
    genome.sort()
    last=genome.internalPop[-1]
    initializator_method(last)
    genome.__setitem__(-1,last) 
    return last           


def crossover_method(genome, **args):
   """ The G2DList Uniform Crossover """
   sister = None
   brother = None
   gMom = args["mom"]
   gDad = args["dad"]
   sister = gMom.clone()
   brother = gDad.clone()
   sister.resetStats()
   brother.resetStats()

   h, w = gMom.getSize()

   for i in xrange(h):
      for j in xrange(w):
         if Util.randomFlipCoin(Consts.CDefG2DListCrossUniformProb):
            temp = sister.getItem(i, j)
            sister.setItem(i, j, brother.getItem(i, j))
            brother.setItem(i, j, temp)       
   return (sister, brother)            


def selector_method(population, **args):
  p=random.random()
  if(p>=0.7):
    population= Selectors.GTournamentSelectorAlternative(population,**args)
  elif(p>=0.3):
    population= Selectors.GRankSelector(population,**args)
  else:
    #print(dir(population))
    #population.clearList()   
    population=reinitializator_method(population)
  return population
      



