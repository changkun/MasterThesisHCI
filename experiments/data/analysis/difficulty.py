import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

age = [1,4,1,0,2,4,3,0,3,1,1,1]

# difficulty visualization
difficulty = np.array([
    [2, 1, 2, 2, 4, 1, 2, 3, 2],
    [2, 2, 1, 2, 3, 1, 1, 5, 1],
    [3, 2, 2, 2, 5, 3, 3, 1, 3],
    [3, 4, 2, 2, 5, 2, 3, 3, 2],
    [2, 1, 3, 3, 5, 3, 2, 1, 3],
    [2, 2, 1, 3, 4, 1, 1, 3, 2],
    [3, 4, 2, 3, 5, 3, 4, 3, 2],
    [1, 1, 1, 3, 5, 2, 2, 1, 1],
    [2, 3, 2, 2, 5, 2, 3, 1, 1],
    [1, 3, 2, 2, 3, 2, 2, 3, 3],
    [2, 2, 3, 1, 4, 5, 1, 2, 3],
    [3, 2, 1, 3, 4, 1, 3, 2, 2],
    [4, 1, 3, 5, 4, 2, 2, 2, 1],
    [2, 2, 2, 2, 3, 1, 2, 2, 1],
    [5, 1, 3, 2, 4, 1, 4, 2, 3],
    [1, 2, 1, 1, 3, 1, 1, 1, 1],
    [3, 1, 1, 3, 4, 3, 2, 2, 3],
    [2, 2, 1, 2, 3, 1, 3, 2, 2],
    [3, 2, 2, 2, 2, 1, 1, 1, 2],
    [1, 3, 2, 3, 5, 1, 2, 3, 2],
    [3, 3, 2, 3, 5, 4, 2, 3, 5]
])
Q = difficulty/difficulty.sum(axis=1)[:,None] # norm

rows = [x for x in range(0, Q.shape[0])]
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)
cax = ax.matshow(Q, cmap='RdBu_r')
fig.colorbar(cax)
plt.show()

# significant test
M1 = np.array([
    [2, 1, 2, 2, 4, 1, 2, 3, 2],
    [2, 2, 1, 2, 3, 1, 1, 5, 1],
    [3, 2, 2, 2, 5, 3, 3, 1, 3],
    [3, 4, 2, 2, 5, 2, 3, 3, 2],
    [2, 1, 3, 3, 5, 3, 2, 1, 3],
    [2, 2, 1, 3, 4, 1, 1, 3, 2],
    [3, 4, 2, 3, 5, 3, 4, 3, 2],
    [1, 1, 1, 3, 5, 2, 2, 1, 1],
    [2, 3, 2, 2, 5, 2, 3, 1, 1],
    [1, 3, 2, 2, 3, 2, 2, 3, 3],
    [2, 2, 3, 1, 4, 5, 1, 2, 3],
])
M2 = np.array([
    [3, 2, 1, 3, 4, 1, 3, 2, 2],
    [4, 1, 3, 5, 4, 2, 2, 2, 1],
    [2, 2, 2, 2, 3, 1, 2, 2, 1],
    [5, 1, 3, 2, 4, 1, 4, 2, 3],
    [1, 2, 1, 1, 3, 1, 1, 1, 1],
    [3, 1, 1, 3, 4, 3, 2, 2, 3],
    [2, 2, 1, 2, 3, 1, 3, 2, 2],
    [3, 2, 2, 2, 2, 1, 1, 1, 2],
    [1, 3, 2, 3, 5, 1, 2, 3, 2],
    [3, 3, 2, 3, 5, 4, 2, 3, 5]
])

M1Norm = M1/M1.sum(axis=0)
M2Norm = M2/M2.sum(axis=0)

for i in range(0, difficulty.shape[1]):
    p = stats.kstest(difficulty[:,i], 'norm').pvalue
    if p < 0.05:
        print(f'column difficulty[{i}], p<0.05')
    else:
        print(f'column difficulty[{i}], p = {p}')
        
for i in range(0, difficulty.shape[0]):
    p = stats.kstest(difficulty[i], 'norm').pvalue
    if p < 0.10:
        print(f'row difficulty[{i}], p<0.05')
    else:
        print(f'row difficulty[{i}], p = {p}')
        
for i in range(0, M1.shape[1]):
    p = stats.kstest(M1[:,i], 'norm').pvalue
    if p < 0.05:
        print(f'column M1[{i}], p<0.05')
    else:
        print(f'column M1[{i}], p = {p}')
        
for i in range(0, M1.shape[0]):
    p = stats.kstest(M1[i], 'norm').pvalue
    if p < 0.10:
        print(f'row M1[{i}], p<0.05')
    else:
        print(f'row M1[{i}], p = {p}')
        
for i in range(0, M2.shape[1]):
    p = stats.kstest(M2[:,i], 'norm').pvalue
    if p < 0.05:
        print(f'column M2[{i}], p<0.05')
    else:
        print(f'column M2[{i}], p = {p}')
        
for i in range(0, M2.shape[0]):
    p = stats.kstest(M2[i], 'norm').pvalue
    if p < 0.10:
        print(f'row M2[{i}], p<0.05')
    else:
        print(f'row M2[{i}], p = {p}')