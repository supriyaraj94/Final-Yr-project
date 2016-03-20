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

with open("m2c_test_dataset.p", "rb") as inptarfile:
	data, target = pickle.load(inptarfile)

net = nl.load(model)
test = net.sim(data)

print " Expected: ", target[0]
print "Generated: ", discretize(test[0])
print "----- %s seconds -----" % (time.time() - start_time)