# This script takes number of epochs as command line argument, by default takes 500
import neurolab as nl, numpy as np, rsa, cPickle as pickle, sys, time
from bitstring import BitArray
from rsa import common

start_time = time.time()
BITS = 8 # number of bits that constitute a byte

with open('public.pem', mode='rb') as publicfile:
	keydata = publicfile.read()
pubkey = rsa.PublicKey.load_pkcs1(keydata)

with open('private.pem', mode='rb') as privatefile:
	keydata = privatefile.read()
privkey = rsa.PrivateKey.load_pkcs1(keydata)

n = pubkey.n
p, q = privkey.p, privkey.q

key_bytes = common.byte_size(pubkey.n) * BITS

nb = BitArray(uint=n, length=key_bytes).bin
pb = BitArray(uint=p, length=key_bytes).bin
qb = BitArray(uint=q, length=key_bytes).bin

inp = np.array(map(int, nb))
tar = np.array(map(int, pb + qb))

num_input_units = len(inp)
num_output_units = len(tar)
minmax = [[0, 1]] * num_input_units
# One of the thumb rule to set nh = 2/3 * (ni + no)
size = [(num_input_units + num_output_units) * 3 / 5, num_output_units]

inp = inp.reshape(1, num_input_units)
tar = tar.reshape(1, num_output_units)

with open("keypair_data.p", "wb") as inptarfile:
	pickle.dump((inp, tar), inptarfile)

trans = [nl.trans.TanSig()] * (len(size) - 1) + [nl.trans.LogSig()]
# Create network with n layers
net = nl.net.newff(minmax, size, transf=trans)

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
print "     #Samples: ", 1
print " #Input Units: ", num_input_units
print "#Hidden Units: ", size[0]
print "#Output Units: ", num_output_units
print "*" * 50

# Train network
error = net.train(inp, tar, epochs=epochs, show=1, goal=0.000001)
net.save('keypair-model-' + str(epochs) + '.net')

print "----- %s seconds -----" % (time.time() - start_time)
print "*" * 50