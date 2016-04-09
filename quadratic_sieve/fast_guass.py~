focus_column=0
focus_row=0
pivot_ele=0
update_col_set=[]
threadLock=0
matrix=[]
go_flag=0
multiplier_optimize=dict()
import threading
import math
from fractions import gcd

def find_null_space(m,rows,cols,mask_length):
	global matrix
	global threadLock
	global focus_column
	global focus_row
	global go_flag
	global pivot_ele
	global update_col_set
	global multiplier_optimize

	#initial work
	matrix=m
	threadLock = threading.Lock()
	thread_count=int(rows/100);
	last_thread_ele_count=rows-100*thread_count
	

	for i in range(0,cols):
		focus_column=i   
		pivot_ele=rows
		go_flag=0
		#Update go_flag and find pivot
		t_list=[]
		for i in range(0,thread_count):
			thread1 = findPivot(i*100,100)
			thread1.start()
			t_list.append(thread1)	
		thread1=findPivot(100*thread_count,last_thread_ele_count)	
		thread1.start()
		t_list.append(thread1)
		for t in t_list:
			t.join()


		#if there is atleast one 1 in the column so as to find the pivot
		if(go_flag==1):
			#print(focus_column)
			#print(pivot_ele)
			#print("***")
			matrix[pivot_ele]['u']=1


			#find corr cols to be updated
			t_list=[]
			update_col_set=[]
			thread1_count=int(cols/100);
			last_thread1_ele_count=cols-100*thread1_count
			for i in range(0,thread1_count):
				thread1 = getCols(i*100,100)
				thread1.start()
				t_list.append(thread1)	
			thread1=getCols(100*thread1_count,last_thread1_ele_count)	
			thread1.start()
			t_list.append(thread1)
			for t in t_list:
				t.join()
			#print(update_col_set)	
			update_col_set.remove(focus_column)	
			


			#update those cols in each row
			t_list=[]
			for i in range(0,thread_count):
				thread1 = updateCols(i*100,100)
				thread1.start()
				t_list.append(thread1)	
			thread1=updateCols(100*thread_count,last_thread_ele_count)	
			thread1.start()
			t_list.append(thread1)
			for t in t_list:
				t.join()
	#give indices to independant/marked rows
	t_list=[]
	for i in range(0,thread_count):
		thread1 = markPivot(i*100,100)
		thread1.start()
		t_list.append(thread1)	
	thread1=markPivot(100*thread_count,last_thread_ele_count)	
	thread1.start()
	t_list.append(thread1)
	for t in t_list:
		t.join()


	print(matrix)

	for ele in matrix:
		pro_a=1
		pro_b=1
		a=1
		b=1
		n=37315319
		if(ele['u']==0):
			for i in range(0,cols):
				if(ele['ele'][i]==1):
					pro_a*=multiplier_optimize[i]['a']
					pro_b*=multiplier_optimize[i]['b']
			pro_a*=ele['a']
			pro_b*=ele['b']		
			a=isqrt(pro_b)
        	b=pro_a
        	print(gcd(a+b,n))
        	print(gcd(a-b,n))
        	print("***")

		

	


#thread to update go_flag and find pivot
class findPivot(threading.Thread):
	def __init__(self,st,num):
		threading.Thread.__init__(self)
		self.st=st
		self.num=num
	def run(self):
		global go_flag
		global pivot_ele
		fl=0
		i=self.st
		self.end=self.st+self.num
		while (i<self.end and fl==0):   		
			fl=fl or matrix[i]['ele'][focus_column]
			i+=1
		threadLock.acquire()
		go_flag=go_flag or fl
		if(fl and (i-1)<pivot_ele):
			pivot_ele=i-1
		threadLock.release()	


#thread to find columns to be updated
class getCols(threading.Thread):
	def __init__(self,st,num):
		threading.Thread.__init__(self)
		self.st=st
		self.num=num
	def run(self):
		global update_col_set
		l=[]
		for i in range(self.st,self.st+self.num):
			if(matrix[pivot_ele]['ele'][i]==1):
				l.append(i)
		threadLock.acquire()
		update_col_set.extend(l)
		threadLock.release()


#thread for elementary col operations
class updateCols(threading.Thread):
	def __init__(self,st,num):
		threading.Thread.__init__(self)
		self.st=st
		self.num=num
	def run(self):
		global update_col_set
		for i in range(self.st,self.st+self.num):
			for ele in update_col_set:
				#print(i)
				#print(ele)
				matrix[i]['ele'][ele]=(matrix[i]['ele'][ele] +matrix[i]['ele'][focus_column])%2


#threads that mark the index of the pivotal element
class markPivot(threading.Thread):
	def __init__(self,st,num):
		threading.Thread.__init__(self)
		self.st=st
		self.num=num
	def run(self):
		global multiplier_optimize
		for i in range(self.st,self.st+self.num):
			if(matrix[i]['u']==1):
				j=0
				while(matrix[i]['ele'][j]==0):
					j+=1
				matrix[i]['w']=j
				d=dict()
				d['a']=matrix[i]['a']
				d['b']=matrix[i]['b']
				threadLock.acquire()
				multiplier_optimize[j]=d
				threadLock.release()

			else:
				matrix[i]['w']=False	
				




def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


