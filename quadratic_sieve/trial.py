import numpy as np
from null_space import rank, nullspace
A=np.array([[0 ,1, 1],
[1 ,1 ,0],
[1 ,0 ,1]],dtype=bool);
b=np.array([[0],[0],[0],[0],[0],[0]])
print(A.shape)

ns = nullspace(A)
print "nullspace:"
print ns