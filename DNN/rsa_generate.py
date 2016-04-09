from fractions import gcd
from random import randrange
from collections import namedtuple
from math import log
from binascii import hexlify, unhexlify
import rsa

def is_prime(n, k=30):
    # http://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    if n <= 3:
        return n == 2 or n == 3
    neg_one = n - 1

    # write n-1 as 2^s*d where d is odd
    s, d = 0, neg_one
    while not d & 1:
        s, d = s+1, d>>1
    assert 2 ** s * d == neg_one and d & 1

    for i in xrange(k):
        a = randrange(2, neg_one)
        x = pow(a, d, n)
        if x in (1, neg_one):
            continue
        for r in xrange(1, s):
            x = x ** 2 % n
            if x == 1:
                return False
            if x == neg_one:
                break
        else:
            return False
    return True

def randprime(N=10**8):
    p = 1
    while not is_prime(p):
        p = randrange(N)
    return p

def multinv(modulus, value):
    '''Multiplicative inverse in a given modulus

        >>> multinv(191, 138)
        18
        >>> multinv(191, 38)
        186
        >>> multinv(120, 23)
        47

    '''
    # http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    x, lastx = 0, 1
    a, b = modulus, value
    while b:
        a, q, b = b, a // b, a % b
        x, lastx = lastx - q * x, x
    result = (1 - lastx * modulus) // value
    if result < 0:
        result += modulus
    assert 0 <= result < modulus and value * result % modulus == 1
    return result

KeyPair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'exponent modulus')

'''
def keygen(N, public=None):
    #<start> Generate public and private keys from primes up to N.

    Optionally, specify the public key exponent (65537 is popular choice).

        >>> pubkey, privkey = keygen(2**64)
        >>> msg = 123456789012345
        >>> coded = pow(msg, *pubkey)
        >>> plain = pow(coded, *privkey)
        >>> assert msg == plain

    #<end>
    # http://en.wikipedia.org/wiki/RSA
    prime1 = randprime(N)
    prime2 = randprime(N)
    composite = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    if public is None:
        while True:
            private = randrange(totient)
            if gcd(private, totient) == 1:
                break
        public = multinv(totient, private)
    else:
        private = multinv(totient, public)
    assert public * private % totient == gcd(public, totient) == gcd(private, totient) == 1
    assert pow(pow(1234567, public, composite), private, composite) == 1234567
    return KeyPair(Key(public, composite), Key(private, composite))
'''

def keygen(public=None):
    with open('public.pem', mode='rb') as publicfile:
        keydata = publicfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(keydata)

    with open('private.pem', mode='rb') as privatefile:
        keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)

    composite = pubkey.n
    prime1 = privkey.p
    prime2 = privkey.q
    totient = (prime1 - 1) * (prime2 - 1)
    if public is None:
        while True:
            private = randrange(totient)
            if gcd(private, totient) == 1:
                break
        public = multinv(totient, private)
    else:
        private = multinv(totient, public)
    return KeyPair(Key(public, composite), Key(private, composite))

def encode(msg, pubkey, verbose=False):
    chunksize = int(log(pubkey.modulus, 256))+1
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (outchunk * 2,)
    bmsg = msg.encode()
    result = []
    chunks=[]
    for start in range(0, len(bmsg), chunksize):
        chunk = bmsg[start:start+chunksize]
        chunk += b'\x00' * (chunksize - len(chunk))
        plain = int(hexlify(chunk), 16)
        coded = pow(plain, *pubkey)
        bcoded = unhexlify((outfmt % coded).encode())
        #if verbose: print('Encode:', chunksize, chunk, plain, coded, bcoded)
        result.append(coded)
        chunks.append(chunk)
    return chunksize, result, chunks

def decode(bcipher, privkey, verbose=False):
    chunksize = int(log(pubkey.modulus, 256)) + 1
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (chunksize * 2,)
    result = []
    for coded in bcipher:
        plain = pow(coded, *privkey)
        chunk = unhexlify((outfmt % plain).encode())
        result.append(chunk)
    return b''.join(result).rstrip(b'\x00').decode()

if __name__ == '__main__':
	
    import sys, cPickle as pickle, time
    from util_rsa_generate import *

    start_time = time.time()
    if len(sys.argv) != 1:
	    filename = sys.argv[1]
    else:
    	print "Command line argument: input filename missing!"
    	sys.exit()

    pubkey, privkey = keygen()
    with open(filename, "r") as inpfile:
    	data = inpfile.read()

    chunksize, ciphers, messages = encode(data, pubkey, 1)
    ciphers, messages = cipher2binary(ciphers, chunksize * 8), message2binary(messages, chunksize * 8)

    training_dataset = (messages, ciphers)
    with open("m2c_rsa_generate.p", "wb") as f:
    	pickle.dump(training_dataset, f)

    '''    
    for msg, cipher in zip(messages, ciphers):
    	print "M: ", msg
    	print "C: ", cipher
    	print "-" * 50
    '''
    print "*" * 50
    print "Message Bits: ", chunksize * 8
    print " Cipher Bits: ", chunksize * 8
    print " Sample Size: ", len(ciphers)
    print "*" * 50
    print "----- %s seconds -----" % (time.time() - start_time)
    print "*" * 50
