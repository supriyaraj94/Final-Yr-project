import math
from prime_generator import primesfrom2to

def get_smoothness_factor(n):
    L=math.exp(0.5*math.log(n)*math.log(math.log(n)))
    return int(math.ceil(L**0.5))

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



n=int(input("Enter n to factorize"))
b_smooth=get_smoothness_factor(n)
prime_list=primesfrom2to(b_smooth)
factor_base=determine_factor_base(prime_list,n)
#print(factor_base)
Xsqr_minus_N_sequence=generate_sequence(int(math.sqrt(n)),int(math.sqrt(2*n)),n)
#print(Xsqr_minus_N_sequence)
b_smooth_sequence=filter_b_smooth(Xsqr_minus_N_sequence,factor_base)
#print(b_smooth_sequence)
print(len(factor_base))
print(len(b_smooth_sequence.keys()))