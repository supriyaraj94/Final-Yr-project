#Using fast guass implementation to find nullspace and also use mt 

import math
from primesieve import *
from sympy import *
from trial1 import *
from fractions import gcd
from fast_guass import find_null_space
import threading


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



#thread for generating and cleaning primes
class determine_factor_base(threading.Thread):
    def __init__(self,st,num):
        threading.Thread.__init__(self)
        self.st=st
        self.num=num
    def run(self):
        global factor_base
        global b_smooth
        global threadLock
        global n
        primes=generate_primes(self.st,self.st+self.num)
        base_factor=[]
        for prime in primes:
            legendre_val=power(n,(prime-1)/2,prime)
            if (legendre_val == 1):
                base_factor.append(prime)
        threadLock.acquire()
        factor_base.extend(base_factor)
        threadLock.release()          

class generate_sequence(threading.Thread):
    def __init__(self,st,num):
        threading.Thread.__init__(self)
        self.st=st
        self.num=num
    def run(self):
        global factor_base
        global b_smooth
        global threadLock
        global n
        global b_smooth_sequence
        global fast_guass
        smooth_seq=dict()
        l=[]
        for i in range(self.st,self.num+self.st):
            b=int(i**2-n)
            num=b
            factors=[0 for x in range(len(factor_base))]
            for p in range(len(factor_base)):
                prime=factor_base[p]
                while(num%prime==0):
                    num=int(num/prime)
                    factors[p]+=1
                if(num==1):
                    smooth_seq[b]=factors
                    d=dict()
                    d['b']=b
                    d['a']=int(math.sqrt(b+n))
                    d['ele']=[x%2 for x in factors]
                    d['w']=0
                    d['u']=0
                    l.append(d)
                    break                         
        threadLock.acquire()
        b_smooth_sequence.update(smooth_seq)
        fast_guass.extend(l)
        threadLock.release()  


def power(x,y,p):
    res=1;
    x=x%p;
    while (y>0):
        if (y & 1):
            res = (res*x) % p;
        y = y>>1; 
        x = (x*x) % p; 
    return  res             


        
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


threadLock = threading.Lock()
n=long(input("Enter n to factorize"))
'''
Get the smoothness factor
'''
b_smooth=get_smoothness_factor(n)



t_list=[]
factor_base=[]
thread_length=10000
thread_count=int((b_smooth-1)/thread_length);
last_thread_ele_count=b_smooth-1-thread_length*thread_count
#print(thread_count)
for i in range(0,thread_count):
    thread1 = determine_factor_base(i*thread_length,thread_length-1)
    thread1.start()
    t_list.append(thread1)  
thread1=determine_factor_base(thread_length*thread_count,last_thread_ele_count)   
thread1.start()
t_list.append(thread1)
for t in t_list:
    t.join()




#print(len(factor_base))

t_list=[]
fast_guass=[]
b_smooth_sequence=dict()
thread_count=int((int(math.sqrt(2*n))-int(math.sqrt(n)))/thread_length);
last_thread_ele_count=(int(math.sqrt(2*n))-int(math.sqrt(n)))-thread_length*thread_count
for i in range(0,thread_count):
    thread1 = generate_sequence(i*thread_length+int(math.sqrt(n))+1,thread_length)
    thread1.start()
    t_list.append(thread1)  
thread1=generate_sequence(thread_length*thread_count+int(math.sqrt(n))+1,last_thread_ele_count)   
thread1.start()
t_list.append(thread1)
for t in t_list:
    t.join()












#print(b_smooth_sequence)

#print(len(b_smooth_sequence))
#Finding the null space
find_null_space(fast_guass,len(b_smooth_sequence),len(factor_base),n)
#write_matrix_to_file(factor_matrix)
#print(fast_guass)







