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
    len_of_q = len(str(q))
    diff = pow(10,len_of_p-1)
    # Define a function for the thread
    def find_factor(a,b):
        prime_list = generate_primes(a,b)
        for i  in prime_list:
            if(target%i==0):
                print ("Number of digits : "+str(len(str(target))))
                print ("The prime factors are : "+str(i)+" "+str(target/i))
                stop = timeit.default_timer()
                print ("Time Taken : " + str(stop-start+time_taken))
                os._exit(1)
        

    # Create two threads as follows
    try:
	if(len(str(target))<20):
        	thread.start_new_thread( find_factor, (abs(p - 2*diff),p,) )
        	thread.start_new_thread( find_factor, (p,p + 2*diff,) )
        	thread.start_new_thread( find_factor, (abs(q - (2*diff)),q,) )
        	thread.start_new_thread( find_factor, (q,q + 2*diff,) )
	else:
        	thread.start_new_thread( find_factor, (abs(p - 0.5*diff),p,) )
        	thread.start_new_thread( find_factor, (p,p + 0.5*diff,) )
        	thread.start_new_thread( find_factor, (abs(q - (0.5*diff)),q,) )
        	thread.start_new_thread( find_factor, (q,q + 0.5*diff,) )
    except:
        print "Error: unable to start thread"

    while 1:
        pass
