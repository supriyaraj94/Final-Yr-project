import neurolab as nl, numpy as np, rsa, cPickle as pickle

with open('public.pem', mode='rb') as publicfile:
	keydata = publicfile.read()
pubkey = rsa.PublicKey.load_pkcs1(keydata)

with open('private.pem', mode='rb') as privatefile:
	keydata = privatefile.read()
privkey = rsa.PrivateKey.load_pkcs1(keydata)

n = pubkey.n
p, q = privkey.p, privkey.q

inp = np.array(map(int, str(n)))
tar = np.array(map(int, str(p)+str(q)))

num_input_units = len(inp)
num_output_units = len(tar)
minmax = [[0, 9]] * num_input_units
# One of the thumb rule to set nh = 2/3 * (ni + no)
size = [(num_input_units + num_output_units) * 2 / 3, num_output_units]

inp = inp.reshape(1, num_input_units)
tar = tar.reshape(1, num_output_units)

with open("inp_tar.p", "wb") as inptarfile:
	pickle.dump((inp, tar), inptarfile)

# Create network with n layers and random initialized
net = nl.net.newff(minmax, size)

# Change traning func
net.trainf = nl.train.train_gd

# Change error func
net.errorf = nl.error.MSE()

# Change trans funs
#net.layers[-1].transf = nl.trans.SatLinPrm(k=1, out_min=0, out_max=9)

epochs = 500
# Train network
error = net.train(inp, tar, epochs=epochs, show=100, goal=0.01)
net.save('model-' + str(epochs) + '.net')