# This script takes input and output filename as command line arguments
# Example: python msg_cipher.py inpfile outfile

import rsa, sys, cPickle as pickle, numpy as np, time
from rsa.bigfile import *

from rsa import key, common, pkcs1, varblock
from rsa._compat import byte

from bitstring import BitArray

start_time = time.time()
BITS = 8 # number of bits that constitute a byte

inpfile = sys.argv[1]
outfile = sys.argv[2]

with open('public.pem', mode='rb') as publicfile:
	keydata = publicfile.read()
pub_key = rsa.PublicKey.load_pkcs1(keydata)

with open('private.pem', mode='rb') as privatefile:
	keydata = privatefile.read()
priv_key = rsa.PrivateKey.load_pkcs1(keydata)

with open(inpfile, 'rb') as infile, open(outfile, 'wb') as oufile:
	encrypt_bigfile(infile, oufile, pub_key)

key_bytes = common.byte_size(pub_key.n) * BITS
padding_bytes = 11 * BITS

messages = []
ciphers = []
with open(outfile, 'rb') as oufile:
	for block in varblock.yield_varblocks(oufile):
		cleartext = pkcs1.decrypt(block, priv_key)

		message = BitArray(bytes=cleartext).bin
		cipher = BitArray(bytes=block).bin
		
		if len(message) == (key_bytes - padding_bytes):
			messages.append(np.array(map(int, message)))
			ciphers.append(np.array(map(int, cipher)))

messages = np.array(messages)
ciphers = np.array(ciphers)

training_dataset = (messages, ciphers)
with open("m2c_training_dataset.p", "wb") as f:
	pickle.dump(training_dataset, f)
'''
for m, c in zip(messages, ciphers):
	print "M: ", m
	print "C: ", c
	print "-" * 50
'''
print "*" * 50
print " Sample Size: ", len(messages)
print "Message Bits: ", len(messages[0])
print " Cipher Bits: ", len(ciphers[0])
print "----- %s seconds -----" % (time.time() - start_time)
print "*" * 50