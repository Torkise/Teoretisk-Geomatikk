import numpy as np 
from numpy.linalg import * 
np.set_printoptions(precision=4)

#Number of observations from dataset
n = 21 

#Number of unknowns {A, B, C, D, E, F}
e = 6 

#data from appendix 
data_file = open('data.txt', 'r')

data = []
#Saves the data to a List   
for line in data_file:
    data.append(line.strip('\n').split())

    
# Initializing Weights with a n*n matrix
P = np.zeros((n, n))

def getWeight(i): 
    # TODO: Get weight from dataset.  Trig is weighted 1 and Niv is levelled 4. 
    if data[i][5] == "Trig":
        return 1
    elif data[i][5] == 'Niv':
        return 4
    return 0

# Add's the weighth to the P matrix 
for i in range(n):
    P[i][i] = getWeight(i)



# List of difference beteween NN1954 and Ellipsiod height in points 
f = []
for i in range(21):
    NN1954 = float(data[i][4])
    ellipse = float(data[i][3])
    diff = abs(float((NN1954-ellipse)))
    f.append(diff)


def calculate(A):
    # Cofactor matrix  
    Q = inv(multi_dot([A.T, P, A]))
    # Solved normal equation 
    x = multi_dot([Q, A.T, P, f])
    
    #printing solution to a) 
    variables = 'ABCDEF' 
    for i in range(len(x)): 
        print(f'{variables[i]}: {x[i]}')
    

    # verbesserung, improvement 
    v = np.dot(A, x) - f

    # std of observation of unit weight 
    sigma_0 = np.sqrt(multi_dot([v.T, P, v])/(n-e))

    # variance-covariance matrix
    C = np.dot(sigma_0*sigma_0, Q)
    print(C)
    print()


    # Estimate the standard deviation 
    for i in range(e):  
        print(f'SD_{variables[i]}: {np.sqrt(C[i, i]): 3E}')
    print() 

    # computed t-values
    for i in range(e):
        t = np. abs(x[i]/np.sqrt(C[i,i]))
        print(f't_{variables[i]}: {t:.3f}')
    print('\n\n')


# Initializing the A matrix of unknonws
A = np.zeros((n, e))
for i in range(n): 
    #Bruke Thorshaug som nullpunkt
    A[i, 0] = float(data[i][1])**2                          #AX^2
    A[i, 1] = float(data[i][1]) * float(data[i][2])         #BXY 
    A[i, 2] = float(data[i][2])**2                          #CY^2
    A[i, 3] = float(data[i][1])                             #DX
    A[i, 4] = float(data[i][2])                             #EY
    A[i, 5] = float(1.0)                                    #F

print('a)')
calculate(A)


## b) 
#We change our model
# Number of unknows 
e = 3 

B = np.zeros((n, e))
for i in range(n):
    # on the form [X, Y, l]
    B[i, 0] = float(data[i][1])     # X
    B[i, 1] = float(data[i][2])     # Y 
    B[i, 2] = float(1.0)                   # constant 


print('Assignment 2. b) ')
calculate(B)
