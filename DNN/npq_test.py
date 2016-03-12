# This script takes N2PQ ANN model's filename as command line argument
import neurolab as nl, cPickle as pickle, sys

if len(sys.argv) != 1:
	model = sys.argv[1]
else:
	print "Command line argument missing! Input model's filename..."
	sys.exit()

with open("n-pq.p", "rb") as inptarfile:
	data, target = pickle.load(inptarfile)

net = nl.load(model)
test = net.sim(data)

print "Expected: ", target
print "Generated: ", test