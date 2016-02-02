n = int(input("Enter the range"))
list_of_primes = []
for i in range(n):
    list_of_primes.append(i)
terminating_count = int(pow(n,0.5))
steps = 0
i = 2
while(steps != terminating_count):
    for j in range(i+1,len(list_of_primes)):
        if(list_of_primes[j]%i==0):
            list_of_primes[j]=0
    if(i==2):
        i = 3
    else:
        i = i+2
    steps = steps+1
for i in list_of_primes:
    if(list_of_primes[i]!=0):
        print list_of_primes[i]       
            
