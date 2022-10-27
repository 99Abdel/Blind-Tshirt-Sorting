import math

import numpy as np

x1 = np.arange(30).reshape(10,3)
x2 = np.arange(10)

print(pow(x1[:,0],2)+x2)
print("\n\n", math.sqrt(0.241*pow(205,2)+0.691*pow(141,2)+0.068*pow(103,2)))

y1 = np.arange(20).reshape(10,2)
dim = np.shape(y1)[0]

print("\n\n", dim)


