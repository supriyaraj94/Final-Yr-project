# This script takes number of bits as command line argument, if not provided defaults to 16 bits.
import rsa, sys, time
start_time = time.time()

if len(sys.argv) != 1:
	nbits = int(sys.argv[1])
else:
	nbits = 16 # Default to 16 bits

pubkey, privkey = rsa.newkeys(nbits, accurate=True, poolsize=8)
pub_key_data = pubkey.save_pkcs1(format='PEM')
pri_key_data = privkey.save_pkcs1(format='PEM')

with open('public.pem', mode='wb') as publicfile:
	publicfile.write(pub_key_data)

with open('private.pem', mode='wb') as privatefile:
	privatefile.write(pri_key_data)

print "*" * 50
print "#Bits: ", nbits
print "----- %s seconds -----" % (time.time() - start_time)
print "*" * 50