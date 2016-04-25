# This script takes number of epochs as command line argument, by default takes 500
import neurolab as nl, numpy as np, cPickle as pickle, sys, time
start_time = time.time()

if len(sys.argv) != 1:
	epochs = int(sys.argv[1])
else:
	epochs = 500

with open("m2c_rsa_generate.p", "rb") as f:
	inp, tar = pickle.load(f)

num_input_units = len(inp[0])
num_output_units = len(tar[0])
minmax = [[0, 1]] * num_input_units

size = [3 * num_input_units * 3 / 5, 2 * num_input_units, num_output_units]

inp = inp.reshape(len(inp), num_input_units)
tar = tar.reshape(len(tar), num_output_units)

trans = [nl.trans.TanSig()] * (len(size) - 1) + [nl.trans.LogSig()]
# Create network with n layers
#net = nl.net.newff(minmax, size, transf=trans)
net = nl.load(raw_input('Model name: '))

# Change traning func, by default uses train_bfgs
#net.trainf = nl.train.train_gdx  # Gradient descent with momentum backpropagation and adaptive lr

npq_net = nl.load(raw_input('NPQ Model name: '))
net.layers[0].np['w'][:] = npq_net.layers[0].np['w'][:]
net.layers[0].np['b'][:] = npq_net.layers[0].np['b'][:]

net.layers[1].np['w'][:] = npq_net.layers[1].np['w'][:]
net.layers[1].np['b'][:] = npq_net.layers[1].np['b'][:]

goal = 0.01

print "*" * 50
print "#Training Samples: ", len(inp)
print "          #Epochs: ", epochs
print "          #Layers: ", len(net.layers) + 1
print "     #Input Units: ", net.ci
print "  #Hidden Units 1: ", size[0]
print "  #Hidden Units 2: ", size[1]
print "    #Output Units: ", net.co
print "             Goal: ", goal
print "*" * 50

# Train network
#error = net.train(inp, tar, epochs=epochs, show=1, goal=goal, lr=0.01, adapt=False, lr_inc=1.05, lr_dec=0.7, max_perf_inc=1.04, mc=0.9, rr=0.0)
print "Training..."
error = net.train(inp, tar, epochs=epochs, show=1, goal=goal)
net.save('m2c-model-' + str(epochs) + '.net')
print "----- %s seconds -----" % (time.time() - start_time)
print "*" * 50
