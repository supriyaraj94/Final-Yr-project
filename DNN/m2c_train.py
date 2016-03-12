import neurolab as nl, numpy as np, cPickle as pickle

with open("m2c_training_dataset.p", "rb") as f:
	inp, tar = pickle.load(f)

num_input_units = len(inp[0])
num_output_units = len(tar[0])
minmax = [[0, 1]] * num_input_units
# One of the thumb rule to set nh = 2/3 * (ni + no)
size = [(num_input_units + num_output_units) * 2 / 3, num_output_units]

#<----- Need some conversion of input to numpy arrays ----->
# Create network with n layers
net = nl.net.newff(minmax, size)

# Change traning func
net.trainf = nl.train.train_gd

# Change error func, by default uses SSE()
#net.errorf = nl.error.MSE()

# Change trans funs
#net.layers[-1].transf = nl.trans.SatLinPrm(k=1, out_min=0, out_max=9)

if len(sys.argv) != 1:
	epochs = int(sys.argv[1])
else:
	epochs = 500

# Train network
error = net.train(inp, tar, epochs=epochs, show=100, goal=0.01)
net.save('m2c-model-' + str(epochs) + '.net')