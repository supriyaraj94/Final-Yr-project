import neurolab as nl, cPickle as pickle

with open("inp_tar.p", "rb") as inptarfile:
	data, target = pickle.load(inptarfile)

net = nl.load("model-500.net")
test = net.sim(data)

print test