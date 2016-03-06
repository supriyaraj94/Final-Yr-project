#Command line arguments
import sys
from primesieve import *
import cPickle as pickle

size = eval(sys.argv[1])
lower_limit = 10 ** (size - 1)
upper_limit = (10 ** size) - 1

primes = generate_primes(lower_limit, upper_limit)
p_count = len(primes)

factors = []
semiprimes = []
for x in xrange(p_count):
	for y in xrange(x+1, p_count):
		product = primes[x] * primes[y]
		if product % 2 != 0:
			t = (primes[x], primes[y])
			factors.append(t)
			semiprimes.append(product)

pickle.dump( (semiprimes, factors), open( "semiprimes_factors.p", "wb" ) )