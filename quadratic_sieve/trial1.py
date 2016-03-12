# coding: utf-8

"""
Automatic solver for Lights Out puzzles.
Currently only square grids are supported.

Includes a Gauss-Jordan elimination method for matrices
defined on arbitrary fields. In particular, the function
GF2inv inverts a matrix defined over the Galois Field GF(2) and
determines its null-space.
"""

from operator import add
from itertools import chain, combinations

import numpy as np
from scipy import ndimage
from sympy import *

class GF2(object):
    """Galois field GF(2)."""
    
    def __init__(self, a=0):
        self.value = int(a) & 1
    def __abs__(self):
        return self.value    
    
    def __add__(self, rhs):
        return GF2(self.value + GF2(rhs).value)
    
    def __mul__(self, rhs):
        return GF2(self.value * GF2(rhs).value)
    
    def __float__(self):
        return self    
    
    def __sub__(self, rhs):
        return GF2(self.value - GF2(rhs).value)
    
    def __div__(self, rhs):

        return GF2(self.value / GF2(rhs).value)
    
    def __repr__(self):
        return str(self.value)
    
    def __eq__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value == rhs.value
        return self.value == rhs
    
    def __le__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value <= rhs.value
        return self.value <= rhs
    
    def __lt__(self, rhs):
        if isinstance(rhs, GF2):
            return self.value <= rhs.value
        return self.value < rhs
    
    def __int__(self):
        return self.value
    
    def __long__(self):
        return self.value
    

GF2array = np.vectorize(GF2)


def gjel(A):
    """Gauss-Jordan elimination."""
    nulldim = 0
    for i in xrange(len(A)):
        pivot = A[i:,i].argmax() + i
        if A[pivot,i] == 0:
            nulldim = len(A) - i
            break
        row = A[pivot] / A[pivot,i]
        A[pivot] = A[i]
        A[i] = row
        
        for j in xrange(len(A)):
            if j == i:
                continue
            A[j] -= row*A[j,i]
    return A, nulldim

def GF2inv(A):
    """Inversion and eigenvectors of the null-space of a GF2 matrix."""
    n = len(A)
    #assert n == A.shape[1], "Matrix must be square"
    
    A = np.hstack([A, np.eye(n)])
    B, nulldim = gjel(GF2array(A))
    print(GF2array(A))
    print("Done with gjel");
    print A
    print B
    print nulldim
    print
    #print(B)
    #print(nulldim)
    E = B[:n, :n]
    null_vectors = []
    if nulldim > 0:
        null_vectors = E[:, -nulldim:]
        null_vectors[-nulldim:, :] = GF2array(np.eye(nulldim))
        null_vectors = np.int_(null_vectors.T)
    
    return null_vectors


def inv(A):
    """Inversion and eigenvectors of the null-space of a GF2 matrix."""
    n = len(A)
    #assert n == A.shape[1], "Matrix must be square"
    
    #A = np.hstack([A, np.eye(n)])
    B, nulldim = gjel(GF2array(A))
    #print(gauss_jordan(GF2array(A)))
    E = B[:n, :n]
    null_vectors = []
    if nulldim > 0:
        null_vectors = E[:, -nulldim:]
        null_vectors[-nulldim:, :] = GF2array(np.eye(nulldim))
        null_vectors = np.int_(null_vectors.T)
    
    return null_vectors
    

def main():
    """Example."""
    lo = LightsOut(4)
    b = np.array([[1,2],[3,4]]);
    bsol = GF2inv(b)
    print "The solution of"
    print b
    print "is"
    print bsol

if __name__ == '__main__':
    main()