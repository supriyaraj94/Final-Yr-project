#Using fast guass implementation to find nullspace

import math
from primesieve import *
from sympy import *
from trial1 import *
from fractions import gcd
from fast_guass import find_null_space

def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def get_smoothness_factor(n):
    L=math.exp(0.5*math.log(n**0.5)*math.log(math.log(n**0.5)))
    return int(math.ceil(L))

def determine_factor_base(prime_list,n):
    base_factor=[]
    for prime in prime_list:
        legendre_val=power(n,(prime-1)/2,prime)
        if (legendre_val == 1):
            base_factor.append(prime)
    return base_factor

def power(x,y,p):
    res=1;
    x=x%p;
    while (y>0):
        if (y & 1):
            res = (res*x) % p;
        y = y>>1; 
        x = (x*x) % p; 
    return  res             

def generate_sequence(a,b,n):
    seq=[]
    for i in range(a+1,b+1):
        seq.append(int(i**2-n))
    return seq
        
def filter_b_smooth(old_seq,primes):
    old_seq.sort()
    seq_copy=old_seq[:]
    factors=dict()
    for ele in seq_copy:
        factors[ele]=[0 for x in range(len(primes))]
    smooth_seq=dict()
    for p in range(len(primes)):
        prime=primes[p]
        i=0
        while i < len(old_seq):
            original_n=seq_copy[i]
            num=old_seq[i]
            while(num%prime==0):
                num=int(num/prime)
                factors[original_n][p]+=1
            if(num==1):
                smooth_seq[original_n]=factors[original_n]
                seq_copy.pop(i)
                old_seq.pop(i)
            else:
                old_seq[i]=num
                i+=1                     
    return smooth_seq            

def compute_a(seq,n):
    mask_length=int(math.ceil(math.log(len(seq.keys()),2)))
    mask=len(seq.keys())-1
    a=[]
    b=[]
    factors=[]
    fast_guass=[]
    for ele in seq.keys():
        d=dict()
        d['b']=ele
        d['a']=int(math.sqrt(ele+n))
        d['ele']=[x%2 for x in seq[ele]]
        d['w']=0
        d['u']=0
        #d['m']=[int(e) for e in format(mask,'0'+str(mask_length)+'b')]
        mask-=1
        fast_guass.append(d)
        b.append(ele)
        a.append(int(math.sqrt(ele+n)))
        factors.append([x%2 for x in seq[ele]])
    return a ,b,factors,fast_guass,mask_length     

def write_matrix_to_file(m):
  filehandle = open("null_matrix.txt", "w")
  filehandle.write(str(m));
  filehandle.close()



n=int(input("Enter n to factorize"))
'''
Get the smoothness factor
'''
b_smooth=get_smoothness_factor(n)
#b_smooth=43
#print(b_smooth)
'''
Generate all primes that are lesser than b_smooth
'''
prime_list=generate_primes(2,b_smooth)
'''
Optimization: Follow legendre function value to remove some of the factors in the generated prime list.
Factor_base is our final list of factors
'''
factor_base=determine_factor_base(prime_list,n)
#print(factor_base)
'''
Generate the sequence of x**2 - n starting from root(n) to root(2n)

'''
Xsqr_minus_N_sequence=generate_sequence(int(math.sqrt(n)),int(math.sqrt(2*n)),n)
#print(Xsqr_minus_N_sequence)
'''
Filter numbers that are not b_smooth
'''
b_smooth_sequence=filter_b_smooth(Xsqr_minus_N_sequence,factor_base)
#print(b_smooth_sequence)
print(len(factor_base))
print(len(b_smooth_sequence))
#Finding the null space

'''
Change formats for finding null_space
'''
a_base,b_base,factor_matrix,fast_guass,mask_length=compute_a(b_smooth_sequence,n)
find_null_space(fast_guass,len(a_base),len(factor_base),mask_length)
write_matrix_to_file(factor_matrix)
#print(fast_guass)







