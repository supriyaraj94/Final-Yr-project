from pyevolve import Consts
from pyevolve import Initializators
from pyevolve import Selectors
from pyevolve import Crossovers
from pyevolve import Mutators
from primesieve import *
import random
import math
import sys
from pyevolve import Util
pq = long( sys.argv[1] )
rs = long( sys.argv[2] )
target = pq*rs
list_width=int(math.ceil(len(str(target))/2.0));
list_height=2;
population_size = 80
flag = 0
found = 0
#prime_list=generate_primes(long(math.pow(10,list_width-1)),long(math.pow(10,list_width)))
#number_of_primes=len(prime_list)

num1 = ""
num2 = ""
if(len(str(target))<20):
    generation_count = 2000
else:
    generation_count = 5000
elitism = 1
crossover_rate = 0.6
mutation_rate = 0.5

minimax = Consts.minimaxType["minimize"]

#selector_method = Selectors.GTournamentSelector
#mutator_method = Mutators.G2DListMutatorSwap
#crossover_method=Crossovers.G2DListCrossoverUniform
last_digits=dict()
last_digits[1]=[[1,1],[3,7],[7,3]]
last_digits[3]=[[1,3],[3,1],[9,7],[7,9]]
last_digits[7]=[[1,7],[7,1],[9,3],[3,9]]
last_digits[9]=[[1,9],[9,1],[3,3]]
lower = math.pow(10,list_width-1)
upper = math.pow(10,list_width)

def initializator_method(genome, **args):
    genome.clearList()
    #while(True):
    '''p=prime_list[random.randint(0,int((number_of_primes-1)/2))]
    q=prime_list[random.randint(int((number_of_primes-1)/2),number_of_primes-1)]
    '''
    '''
        if ((p%10) * (q%10))!= (target%10):
            continue
        else:
            break 
    '''       
    f = long(pow(target,0.5))
    p = generate_n_primes(1,random.randint(lower,f))[0]
    q = generate_n_primes(1,random.randint(f,upper))[0]
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
   p1 = ""
   p2 = ""
   p3 = ""
   p4 = ""
   p5 = ""
   for j in range(0,w):
      p1 = p1+str(gMom.getItem(0,j)) 
   for j in range(0,w):
      p3 = p3+str(gDad.getItem(0,j))
   p1 = long(p1)    
   p3 = long(p3) 
   p2 = list(str(long(target/p1)))
   p4 = list(str(long(target/p3)))
   for i in range(0,int(w/2)):
      if(len(p2)==len(sister[0])):
         sister.setItem(1,i,int(p2[i]))
      if(len(p4)==len(sister[0])):
         brother.setItem(1,i,int(p4[i]))
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
  
def find_factors(num,n,m):
   li = []
   for i in range(1, 10):
       if num % i == 0 and (i!=n and i!=m) and num/i < 10:
          li.append([i,num/i])
   return li      

def mutator_method(population, **args):
    list_of_numbers = []
    global flag
    for row in population:
       	if(row[0]==0):
           	row[0]=random.randint(1,9)
        s = map(str, row)   
        s = ''.join(s)
        list_of_numbers.append(long(s))
    left = population[0][0] 
    right = population[1][0]
    if(flag<2):
        product = list_of_numbers[0]*list_of_numbers[1]
        diff = abs(target-product)
        length_of_diff = len(str(diff))
        ind = len(population[0])-int(math.ceil(length_of_diff/2))
        if(ind!=0):
            population[0][ind] = random.randint(0,9)
        else:
            population[0][ind] = random.randint(1,9)
        stemp = map(str,population[0])
        stemp = ''.join(stemp)
        temp_number = long(target/long(stemp))
        population[1][ind] = int(str(temp_number)[ind])
        flag = flag+1
    elif(flag<4):
        x = left
        y = right
        pr = x*y
        li = find_factors(pr,x,y)
        if(len(li)>0):
            population[0][0] = li[0][0]
            population[1][0] = li[0][1]
        flag = flag + 1
    elif(flag<6):
        if(left != 9 and right != 1):
            population[0][0] = left + 1
            population[1][0] = right - 1
        flag = flag + 1
    else:
        if(left != 1 and right != 9):
            population[0][0] = left - 1
            population[1][0] = right + 1
        flag = 0
    return 2