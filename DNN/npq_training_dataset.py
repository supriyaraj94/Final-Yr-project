# This script takes number of bits and number of samples as command line arguments, 
# if not provided, defaults to 16 bits and 1000 samples.
import rsa, sys, time, numpy as np, cPickle as pickle
from bitstring import BitArray

start_time = time.time()

if len(sys.argv) != 1:
	nbits = int(sys.argv[1])
	nsamples = int(sys.argv[2])
else:
	nbits = 16 # Default to 16 bits
	nsamples = 1000 # Default to 1000 samples

inp, tar = [], []
for x in xrange(nsamples):
	pubkey, privkey = rsa.newkeys(nbits, accurate=True, poolsize=8)
	n, p, q = pubkey.n, privkey.p, privkey.q
	nb = BitArray(uint=n, length=nbits).bin
	pb = BitArray(uint=p, length=nbits).bin
	qb = BitArray(uint=q, length=nbits).bin

	tinp = np.array(map(int, nb))
	ttar = np.array(map(int, pb + qb))

	inp.append(tinp)
	tar.append(ttar)

inp, tar = np.array(inp), np.array(tar)
training_dataset = (inp, tar)

with open("npq_training_dataset.p", "wb") as f:
	pickle.dump(training_dataset, f)

print "*" * 50
print "   #Bits: ", nbits
print "#Samples: ", nsamples
print "*" * 50
print "----- %s seconds -----" % (time.time() - start_time)
print "*" * 50
