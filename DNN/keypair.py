import rsa

nbits = 16
pubkey, privkey = rsa.newkeys(nbits, accurate=True, poolsize=8)
pub_key_data = pubkey.save_pkcs1(format='PEM')
pri_key_data = privkey.save_pkcs1(format='PEM')

with open('public.pem', mode='wb') as publicfile:
	publicfile.write(pub_key_data)

with open('private.pem', mode='wb') as privatefile:
	privatefile.write(pri_key_data)