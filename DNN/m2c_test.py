# This script takes M2C ANN model's filename as command line argument
import neurolab as nl, cPickle as pickle, sys, numpy as np, time
start_time = time.time()

def discretize(alist):
	return np.array([0 if x < 0.5 else 1 for x in alist])

if len(sys.argv) != 1:
	model = sys.argv[1]
else:
	print "Command line argument missing! Input model's filename..."
	sys.exit()

with open("m2c_rsa_generate.p", "rb") as inptarfile:
	data, target = pickle.load(inptarfile)

data = data[2000:2100]
target = target[2000:2100]
net = nl.load(model)
test = net.sim(data)

# Sample wise... Bit wise
total = len(data)
nbits = len(data[0])
scount = 0.0
bcount = 0.0
for x in xrange(total):
	exp = target[x]
	gen = discretize(test[x])
	if (exp == gen).all():
		scount += 1

	for y in xrange(nbits):
		if exp[y] == gen[y]:
			bcount += 1

print "*" * 50
print "            #Samples: ", total
print "Sample Wise Accuracy: ", 100 * scount / total
print "*" * 50
print "            #Bits: ", total * nbits
print "Bit Wise Accuracy: ", 100 * bcount / (total * nbits)
print "*" * 50

print "----- %s seconds -----" % (time.time() - start_time)
print "*" * 50