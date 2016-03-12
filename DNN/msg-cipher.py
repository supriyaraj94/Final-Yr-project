# This script takes input and output filename as command line arguments
# Example: python msg_cipher.py inpfile outfile

import rsa, sys, cPickle as pickle
from rsa.bigfile import *

from rsa import key, common, pkcs1, varblock
from rsa._compat import byte

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

messages = []
ciphers = []
with open(outfile, 'rb') as oufile:
	for block in varblock.yield_varblocks(oufile):
		cleartext = pkcs1.decrypt(block, priv_key)
		messages.append(cleartext)
		ciphers.append(block)

training_dataset = (messages, ciphers)
with open("m2c_training_dataset.p", "wb") as f:
	pickle.dump(training_dataset, f)