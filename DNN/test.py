import neurolab as nl

net = nl.load("model.net")

data = <test data>
test = net.sim(data)