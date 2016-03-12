import math
from primesieve import *
from sympy import *
from trial1 import *
from fractions import gcd

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
    a=[]
    b=[]
    factors=[]
    for ele in seq.keys():
        b.append(ele)
        a.append(int(math.sqrt(ele+n)))
        factors.append([x%2 for x in seq[ele]])
    return a ,b,factors     

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
#print(len(factor_base))
#print(len(b_smooth_sequence))
#Finding the null space

'''
Change formats for finding null_space
'''
a_base,b_base,factor_matrix=compute_a(b_smooth_sequence,n)
#print(())
write_matrix_to_file(factor_matrix)

#print((factor_matrix))

'''
Find row reduced echelon form
'''
sympy_mat=Matrix(factor_matrix).T
echelon=sympy_mat.rref();
#print(echelon)
#print(b_base)
pivotal_numbers=echelon[1]
#print(pivotal_numbers)
#print("Pivots:"+str(len(pivotal_numbers)))
'''Remove non-pivotal columns'''

new_a_base=[a_base[x] for x in pivotal_numbers]
new_b_base=[b_base[x] for x in pivotal_numbers]
new_factor_matrix=[factor_matrix[x] for x in pivotal_numbers]
write_matrix_to_file(new_factor_matrix)
#print(new_a_base)
'''
Padding zeroes to obt square matrix
'''
padding=len(factor_base)-len(new_factor_matrix)
for i in range(padding):
    l=[0 for x in range(len(factor_base))]
    new_factor_matrix.append(l)


b = np.array(new_factor_matrix).transpose()
bsol = GF2inv(b)
print(len(bsol[1]))
#print(new_b_base)


soln_vectors=[]
for vector in bsol[1]:
    vector=vector[0:len(factor_base)-padding]
    if(sum(vector)==0):
        continue
    check=[0 for x in factor_base]
    pro_b=1
    pro_a=1
    for i in range(len(vector)):
        if(vector[i]==1):
            pro_b*=new_b_base[i]
            pro_a*=new_a_base[i]
            for j in range(len(factor_base)):
                check[j]=(check[j] + new_factor_matrix[i][j])%2
    if(sum(check)==0):
        print("******")
        print(check)
        print(vector)
        print(pro_b)
        print(pro_a)            
        a=isqrt(pro_b)
        b=pro_a
        print(gcd(a+b,n))
        print(gcd(a-b,n))








