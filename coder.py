import encoding_tools as enc
import numpy as np
from sys import argv

#code: (15,8) x^7+x^3+x+1 
n=15 #block length
k=8 #message length
polynomial = [0,0,0,0,0,0,0,1,0,0,0,1,0,1,1]

print("n: " + str(n) + " k: " + str(k) + " Generator polynomial: ")
print(np.poly1d(polynomial))

#Create generator matrix...
genMatrix = enc.createGenMatrix(n, k, polynomial)

print("\nGenerator matrix: ")
print(genMatrix)

infWords = [] #messages
codeWords = [] 

#Reading messages from file
input = ""
try:
    if len(argv) > 1:
        input = open(argv[1])
    else:
        input = open("coder_input.txt")
except:
    if len(argv) > 1:
        print("ERROR: Cannot open input file!")
    else:
        print("ERROR: Cannot open coder_input.txt file!")
    quit()

lines = input.readlines()
for line in lines:
    lst = list(line.strip("\n"))
    lst = [int(i) for i in lst ]
    infWords.append(lst)
input.close()

print("\nEncoding: ")

output = open("coder_output.txt", 'w')
for word in infWords:
    codeWord = np.array(word).dot(genMatrix) # Multiplying message by generator matrix
    codeWord = codeWord.tolist()             
    codeWord = [ (i % 2) for i in codeWord]  # mod 2 each element
    output.write(str(codeWord).replace(',', '').replace(" ", "").strip("[]") + "\n")
    print(str(word) + " -> " + str(codeWord)) 
output.close()