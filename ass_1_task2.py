import numpy as np 
from numpy.linalg import multi_dot, inv


#TODO: Spør Sondre om de tallene i getF(x)  -> De siste mindre tallene. OG hvorfor vil tar x[0]
#TODO: Spør sondre om getF(x) Hva er den?  Vi trur den er Covariansematrisen. 

def lsm_heigth(): 
    
    weight_values = np.array([0.16, 0.04, 0.25, 0.16, 0.16, 1, 0.444, 1, 1, 0.63, 0.4])

    #weight from in exel 

    #Make a MAtrix with weigths 
    weight = np.zeros(shape=(11, 11))
    for i in range(11):
        weight[i][i] = weight_values[i]
    print(weight)

    #Koken sine ligener  
    A = np.array([[0, -1], [0, -1], [0, -1], [0, -1], [1, -1], [-1, 0], [-1, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
    # Våre ligniner
    A = np.array([[1,-1], [0,-1], [0,-1], [0,-1], [0, -1], [-1,0], [-1,0],[0,0], [0,0], [0,0], [0,0]])
    f = np.array([-82.92, -82.9098, -82.917, -82.906, -1.7519, -81.1507, -81.1461, 0.0039, 0.0081, -0.0033, -0.005])
    

    #inv --> Inverse of the matrix 
    # multi_dot --> The produkt of two or more arrrays. 
    Q = inv(multi_dot([A.T, weight, A]))

    x = multi_dot([Q, A.T, weight, f])

    v = np.dot(A, x) - f 

    Sigma_0 = 1000 * np.sqrt(multi_dot([v.T, weight, v]) / (11-2))
    #Ligningen for covarianse fra Anvendt Geomatikk 
    Covariance =  np.dot(Sigma_0*Sigma_0, Q)

    sx = np.sqrt(Covariance[0, 0])
    sy = np.sqrt(Covariance[1, 1])

    # TODO: Lage print funksjoner her. 
    print("Task 2.1")
    print("A", x[0], 'B', x[1])
    print("Sigma_0 =", Sigma_0)
    print()
    print("Covariance Matrix")
    print('\n'.join([' '. join([str(round(cell, 3)) for cell in row]) for row in Covariance]))
    print("")
    print("Sx", sx, "sy", sy)
    print()
    print("Matrices used in the calculations: ")
    print("A:")
    print('\n'.join([' '.join([str(round(cell,3)) for cell in row]) for row in A]))
    print("Weigth, P:")
    print('\n'.join([' '.join([str(round(cell,3))for cell in row]) for row in weight ]))

    print('f')
    for element in f: 
        print(round, element, 3)

def getF(x): 
    # TODO: Finn ut hva X er 
    return np.array([
        #HAV - GM18A
        -x[0] + 2815018.2561,
        -x[1] + 517204.4025,
        -x[2] + 56808075.0630,
        
        #MOH - GM18A
        -x[0] + 2815018.3495,
        -x[1] + 517204.4041,
        -x[2] + 5600875.0609,

        # GM18A - GM18B
        -x[3] + x[0] - 516.0604, 
        -x[4] + x[1] - 419.5919,
        -x[5] + x[2] + 293.8671, 

        # HVA GM18B
        -x[3] + 2814502.3046, 
        -x[4] + 516784.8124, 
        -x[5] + 5681168.9450, 

        # FEST - HAV19B
        -x[3] + 2814502.2946,
        -x[4] + 516784.8141, 
        -x[5] + 5681168.9384, 

        # MOH - GM18B 
        -x[3] + 2814502.2947,
        -x[4] + 516784.8167, 
        -x[5] + 5681168.9461, 

        # ØYA - GM18B 
        -x[3] + 2814502.2952,
        -x[4] + 516784.8143,
        -x[5] + 5681168.9339, 

        0.0124,
        -0.0034, 
        0.0102, 
        0.0094, 
        -0.016,
        0.0010, 
        0.0071,
        -0.0232, 
        0.0042,
        -0.0030, 
        0.0069        
    ])

def lms_coordinate(): 
    print('')
    print('Task 2.2')
    # TODO: What is F? 
    f = np.array([
        2815018.2561,
        517204.4025,
        56808075.0630,

        2815018.3495,
        517204.4041,
        5600875.0609,

        516.0604,
        419.5919,
        293.8671,

        2814502.3046,
        516784.8124,
        5681168.9450,

         # FEST - HAV19B
        2814502.2946,
        516784.8141, 
        5681168.9384, 

        # MOH - GM18B 
        2814502.2947,
        516784.8167, 
        5681168.9461, 

        # ØYA - GM18B 
        2814502.2952,
        516784.8143,
        5681168.9339, 
        ])

    A = np.zeros(shape=(33, 6))    #Hvorfor 33 *6 
    #TODO: Hva er den A matrisen? Hvor kommer verdiene fra?   Det er vell observation equations? 
    #Fundamental equatiosn. l -> høydeforksjell,  v -> korreksjonsledd,   x = ukjent p x,  p ukjent punkt p 
    #Setter opp l + v på venstresiden 
    # Får til - fra. 
    # Få opp alle 11/33 fundamentalligningene (1d leller 3d. )
    # Sette opp observasjonsligningene. De kommer fra fundamentallignende med matte p. 
    # Korreksjonsleddet alene. 
    # A er x, y, x, u, v, w i observasjonsligningen
    #[x, y, z, u, v, w]
    #[x, y, z, u, v, w]
    #[x, y, z, u, v, w]
    A[0,0] = 1
    A[1,1] = 1
    A[2,2] = 1
    A[3,0] = 1
    A[4,1] = 1
    A[5,2] = 1
    A[6,0] =-1
    A[6,3] = 1
    A[7,1] =-1
    A[7,4] = 1
    A[8,2] =-1
    A[8,5] = 1
    A[9,3] = 1
    A[10,4]= 1
    A[11,5]= 1
    A[12,3]= 1
    A[13,4]= 1
    A[16,4]= 1
    A[17,5]= 1
    A[18,3]= 1
    A[19,4]= 1
    A[20,5]= 1

    weight = np.zeros((33,33))
    #TODO: Finne Weights. 

lsm_heigth()

lms_coordinate()

