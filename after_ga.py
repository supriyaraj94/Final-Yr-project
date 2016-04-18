import thread
import time
import sys
import time
import os
import timeit
from primesieve import *


def find_primes(p,q,target,time_taken):
    start = timeit.default_timer()
    len_of_p = len(str(p))
    diff = pow(10,len_of_p-1)
    # Define a function for the thread
    def find_factor1(a,b):
        it1 = Iterator()
        it1.skipto(a)
        prime1 = a
        while(prime1<b):
            prime1 = it1.next_prime()
            if(target%prime1 == 0):
                print ("The factors are : "+str(prime1)+" "+str(target/prime1))
                stop = timeit.default_timer()
                print ("Time taken : "+str(stop-start+time_taken))
                os._exit(1)
    def find_factor2(a,b):
        it2 = Iterator()
        it2.skipto(a)
        prime2 = a
        while(prime2<b):
            prime2 = it2.next_prime()
            if(target%prime2 == 0):
                print ("The factors are : "+str(prime2)+" "+str(target/prime2))
                stop = timeit.default_timer()
                print ("Time taken : "+str(stop-start+time_taken))
                os._exit(1)
    def find_factor3(a,b):
        it3 = Iterator()
        it3.skipto(b)
        prime3 = b
        while(prime3>a):
            prime3 = it3.previous_prime()
            if(target%prime3 == 0):
                print ("The factors are : "+str(prime3)+" "+str(target/prime3))
                stop = timeit.default_timer()
                print ("Time taken : "+str(stop-start+time_taken))
                os._exit(1)
    def find_factor4(a,b):
        it4 = Iterator()
        it4.skipto(b)
        prime4 = b
        while(prime4>a):
            prime4 = it4.previous_prime()
            if(target%prime4 == 0):
                print ("The factors are : "+str(prime4)+" "+str(target/prime4))
                stop = timeit.default_timer()
                print ("Time taken : "+str(stop-start+time_taken))
                os._exit(1)

    # Create two threads as follows
    try:
	if(len(str(target))<80):
        	thread.start_new_thread( find_factor3, (abs(p - 2*diff),p,) )
        	thread.start_new_thread( find_factor1, (p,p + 2*diff,) )
        	thread.start_new_thread( find_factor4, (abs(q - (2*diff)),q,) )
        	thread.start_new_thread( find_factor2, (q,q + 2*diff,) )

    except:
        print "Error: unable to start thread"

    while 1:
        pass

