# This script takes number of epochs as command line argument, by default takes 500
import neurolab as nl, numpy as np, cPickle as pickle, sys, time
start_time = time.time()

with open("npq_training_dataset.p", "rb") as f:
	inp, tar = pickle.load(f)

num_input_units = len(inp[0])
num_output_units = len(tar[0])
minmax = [[0, 1]] * num_input_units
# One of the thumb rule to set nh = 2/3 * (ni + no)
size = [(num_input_units + num_output_units) * 3 / 5, num_output_units]

inp = inp.reshape(len(inp), num_input_units)
tar = tar.reshape(len(tar), num_output_units)

trans = [nl.trans.TanSig()] * (len(size) - 1) + [nl.trans.LogSig()]
# Create network with n layers
#net = nl.net.newff(minmax, size, transf=trans)
net = nl.load('npq-model-10000.net')

# Change traning func, by default uses train_bfgs
#net.trainf = nl.train.train_gd

# Change error func, by default uses SSE()
#net.errorf = nl.error.MSE()

if len(sys.argv) != 1:
	epochs = int(sys.argv[1])
else:
	epochs = 500

print "*" * 50
print "      #Epochs: ", epochs
print "     #Samples: ", len(inp)
print " #Input Units: ", num_input_units
print "#Hidden Units: ", size[0]
print "#Output Units: ", num_output_units
print "*" * 50

# Train network
error = net.train(inp, tar, epochs=epochs, show=1, goal=0.01)
net.save('npq-model-' + str(epochs) + '.net')
print "----- %s seconds -----" % (time.time() - start_time)
print "*" * 50
