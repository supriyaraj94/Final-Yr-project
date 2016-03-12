# This script takes input and output filename as command line arguments
# Example: python msg_cipher.py inpfile outfile

import rsa, sys
from rsa.bigfile import *

from rsa import key, common, pkcs1, varblock
from rsa._compat import byte

inpfile = sys.argv[1]
outfile = sys.argv[2]

with open('public.pem', mode='rb') as publicfile:
	keydata = publicfile.read()
pub_key = rsa.PublicKey.load_pkcs1(keydata)

with open(inpfile, 'rb') as infile, open(outfile, 'wb') as oufile:
	encrypt_bigfile(infile, oufile, pub_key)

key_bytes = common.bit_size(pub_key.n)
blocksize = key_bytes - 11 # keep space for PKCS#1 padding

messages = []
ciphers = []
with open(inpfile, 'rb') as infile, open(outfile, 'rb') as oufile:
	for block in varblock.yield_fixedblocks(infile, blocksize):
		messages.append(block)

	for block in varblock.yield_varblocks(oufile):
		ciphers.append(block)

print len(messages), len(ciphers)

training_data = zip(messages, ciphers)
print training_data