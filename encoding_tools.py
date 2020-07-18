import numpy as np
from itertools import combinations

#Shifts a vector n elements
def vectorShift(vector, n) -> list:
    shifted = vector
    if n >=0:     #shift left
        for _ in range(n):
            val = shifted[0]
            shifted = shifted[1:]
            shifted.append(val)
    else:       #shift right
        n = -n
        for _ in range(n):
            val = shifted[-1]
            shifted = shifted[:-1]
            shifted.insert(0,val)

    return shifted

#Returns binary representation of a monomial
def monomial(degree) -> list:
    polynomial = [1]
    for _ in range(0,degree):
        polynomial.append(0)
    return polynomial

#Adds leading zeros to a vector
#Example: Input: ([1,0,0,1,1], 7) Output: [0,0,1,0,0,1,1]
def fillPolynomial(polynomial, length) -> list:
    while len(polynomial) != length:
        polynomial.insert(0,0)
    return polynomial

#Removes leading zeroes from a vector
#Example: Input: [0,0,0,0,1,0,1,0] Output: [1,0,1,0]
def stripPolynomial(polynomial) -> list:
    i = 0
    for number in polynomial:
        if number != 0:
            return polynomial[i:] 
        i+=1
    
    return 0

#Creating generator matrix for a (n,k) cyclic systematic code
def createGenMatrix(n,k,polynomial) -> np.array:
    G = []
    for i in range(0,k):
        identityPart = monomial(k-1-i)  
        identityPart = fillPolynomial(identityPart,k)

        res= np.polydiv(np.poly1d(monomial(n-1-i)) , np.poly1d(polynomial)) 
        remainder = res[1] 
        remainder = [ int(x%2) for x in remainder] 
        remainder = fillPolynomial(remainder, n-k)
        
        newRow = identityPart + remainder

        G.append(newRow)
    return np.array(G)

#Creates a parity check matrix from a generator matrix
def createHTMatrix(n,k,genMatrix) -> np.array:
    HT = []
    for row in genMatrix:
        HT.append(row.tolist()[k:])
    
    HT = np.array(HT)
    HT = np.vstack([HT, np.identity(n-k, int)])

    return HT

#Calculate Hamming weight of a vector
def hammingWeight(vector) -> int:
    sum = 0
    for element in vector:
        if element == 0:
            continue
        sum += 1
    return sum

#Calculate Hamming distance between two vectors
def hammingDistance(vector1, vector2):
    sum = 0
    for i in range(0, len(vector1)):
        if vector1[i] != vector2[i]:
            sum += 1
    return sum

#Calculates minimum distance of the code by finding the minimum number of rows
#which sum is a vector of zeros
def calculateDmin(HT):
    row_count = np.size(HT,0)
    dmin = row_count
    rows = []
    combs = []

    for i in range (1, row_count+1): 
        rows.append(i)

    for i in range (1, row_count+1): #Find all combinations of rows
        comb = combinations(rows, i)
        combs = combs + list(comb)

    for combination in combs:
        if(len(combination) > dmin):
            break; 

        row_sum = [0] * np.size(HT, 1)

        for row in combination:
            row_as_list = HT[row-1].tolist()
            row_sum = [row_sum[i] + row_as_list[i] for i in range (len(row_sum))]

        row_sum = [ (x%2) for x in row_sum ]

        hamming_weight = hammingWeight(row_sum)
        if hamming_weight == 0 and len(combination) < dmin:
            dmin = len(combination)

    return dmin