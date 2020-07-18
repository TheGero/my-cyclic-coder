import encoding_tools as enc
import numpy as np 
from sys import argv

#Attempt to correct an invalid codeword
def correction(word, t):
    syndrome = np.array(word).dot(HTMatrix)
    syndrome = [ (x % 2) for x in syndrome]
    weight = enc.hammingWeight(syndrome)

    shift = 0

    corrected = []

    while weight > t and shift <= k: 
        word = enc.vectorShift(word, -1)
        shift += 1
        syndrome = np.array(word).dot(HTMatrix)
        syndrome = [ (x % 2) for x in syndrome]
        weight = enc.hammingWeight(syndrome)
        
    if weight <= t:
        syndrome = enc.fillPolynomial(syndrome,n)
        corrected = np.add(word, syndrome).tolist()
        corrected = [ (x % 2) for x in corrected]
        corrected = enc.vectorShift(corrected, shift)

    return corrected

#main

#code: (15,8) x^7+x^3+x+1 
n=15
k=8

polynomial = [0,0,0,0,0,0,0,1,0,0,0,1,0,1,1] #generator polynomial

#Creating generator and parity check matrix
genMatrix = enc.createGenMatrix(n, k, polynomial)
HTMatrix = enc.createHTMatrix(n, k, genMatrix)

dmin = enc.calculateDmin(HTMatrix) #minimum distance
detection = dmin-1 #detection ability
t = int(detection/2) #correction ability

receivedWords = []

print("Parity check matrix:")
print(HTMatrix)
print("\nDetection ability: ", detection, "\nCorrection ability: ", t, "\n")

#reading codewords from file
input = ""
try:  
    if len(argv) > 1:
        input = open(argv[1])
    else:
        input = open("coder_output.txt")
except:
    if len(argv) > 1:
        print("ERROR: Cannot open input file!")
    else:
        print("ERROR: Cannot open coder_output.txt file!")
    quit()

for row in input.readlines():
    vec = row.strip("\n")
    vec = [ int(i) for i in vec ] 
    receivedWords.append(vec)
input.close()

print("Decoding:")

output = open("decoder_output.txt", "w")
for word in receivedWords:
    syndrome = np.array(word).dot(HTMatrix)
    syndrome = [ (x % 2) for x in syndrome]

    if enc.hammingWeight(syndrome) != 0: #if received word is not a valid codeword...
        #attempt correction
        codeWord = correction(word, t)
        #if returned list is empty, the word cannot be corrected
        if len(codeWord) == 0:
            print(str(word) + " - Can't be corrected")
            output.write("Can't be corrected\n")
        else:
            #Correction successful
            infWord = codeWord[0:k]
            print(str(word)+" --Correction--> " + str(codeWord) + " -> " + str(infWord))
            output.write(str(infWord).replace(',', '').replace(" ", "").strip("[]") + "\n")
    
    #No error detected
    else:
        infWord = word[0:k]
        print(str(word)+" -> " + str(infWord))
        output.write(str(infWord).replace(',', '').replace(" ", "").strip("[]") + "\n")
    
output.close()
