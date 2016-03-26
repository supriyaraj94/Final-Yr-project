# This script takes number of digits as command line argument
# Example: python semiprimes_factors.py 4 (for 4 digits prime factors)
import sys, time
from primesieve import *
import cPickle as pickle

start_time = time.time()
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

print "*" * 50
print "#Prime Factor Digits: ", sys.argv[1]
print "*" * 50
print "----- %s seconds -----" % (time.time() - start_time)
print "*" * 50