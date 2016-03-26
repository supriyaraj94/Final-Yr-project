# This script takes Keypair ANN model's filename as command line argument
import neurolab as nl, cPickle as pickle, sys, numpy as np, time
start_time = time.time()

def discretize(alist):
	return np.array([0 if x < 0.5 else 1 for x in alist])

if len(sys.argv) != 1:
	model = sys.argv[1]
else:
	print "Command line argument missing! Input model's filename..."
	sys.exit()

with open("keypair_data.p", "rb") as inptarfile:
	data, target = pickle.load(inptarfile)

net = nl.load(model)
test = net.sim(data)

exp = target[0]
gen = discretize(test[0])

print "*" * 50
print " Expected: ", exp
print "Generated: ", gen

if (exp == gen).all():
	print "\nSame!!!"
else:
	print "\nNot same!!!"

print "*" * 50
print "----- %s seconds -----" % (time.time() - start_time)
print "*" * 50