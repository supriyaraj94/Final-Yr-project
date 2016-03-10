# This script takes input and output filename as command line arguments
# Example: python msg_cipher.py inpfile outfile
'''
import rsa, sys
from rsa.bigfile import *

inpfile = sys.argv[1]
outfile = sys.argv[2]

with open('public.pem', mode='rb') as publicfile:
	keydata = publicfile.read()
pub_key = rsa.PublicKey.load_pkcs1(keydata)

with open(inpfile, 'rb') as infile, open(outfile, 'wb') as outfile:
	encrypt_bigfile(infile, outfile, pub_key)
'''

from rsa import key, common, pkcs1, varblock
from rsa._compat import byte

# Working on this....