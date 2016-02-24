import neurolab as nl
import numpy as np

num_input_units = <some number>
minmax = [[minx, maxx]] * num_input_units
size = [n_h1, n_h2, n_h3, ..... n_op]

# Create network with n layers and random initialized
net = nl.net.newff(minmax, size)

# Train network
error = net.train(inp, target, epochs=100, show=10, goal=0.02)
net.save('model.net')