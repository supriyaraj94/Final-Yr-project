import numpy as np
from bitstring import BitArray

def message2binary(alist, nkeybits):
	if isinstance(alist, list):
		return np.array([np.array(map(int, BitArray(bytes=msg, length=nkeybits).bin)) for msg in alist])

	return np.array([np.array(map(int, BitArray(bytes=alist, length=nkeybits).bin))])

def cipher2binary(alist, nkeybits):
	if isinstance(alist, list):
		return np.array([np.array(map(int, BitArray(uint=cipher, length=nkeybits).bin)) for cipher in alist])

	return np.array([np.array(map(int, BitArray(uint=alist, length=nkeybits).bin))])