import math
import struct
from tabnanny import check

magicBytes = bytearray(b'\x06\x00\x00\x00\x06\x00\x00\x00\x30\x00\x00\x00\x33\x00\x00\x00\x07\x00\x00\x00\x07\x00\x00\x00\x03\x00\x00\x00\x07\x00\x00\x00\x32\x00\x00\x00\x06\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x35\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x07\x00\x00\x00\x07\x00\x00\x00\x07\x00\x00\x00\x06\x00\x00\x00\x36\x00\x00\x00\x07\x00\x00\x00\x05\x00\x00\x00\x06\x00\x00\x00\x06\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x03\x00\x00\x00\x07\x00\x00\x00\x30\x00\x00\x00\x07\x00\x00\x00')

def isAsciiPrime(c):
    i = 2
    while i * i < c:
        if c % i == 0:
            return 0
        i = i + 1
    return 1


def checkKey(output, magicBytes, len):

    magicInts = struct.unpack('<30i', magicBytes)

    for i in range (0, len):
        if output[i] != magicInts.index(i):
            return 1
    return 0

def processInput(input):

    output = [range[30]]

    for i in range(0, 30): # 0x1e
        asciiPrime = isAsciiPrime(input[i])

        if asciiPrime == 0:
            output[i] = ord(input[i]) >> 4
        else:
            output[i] == ord(input[i]) >> 1

    isKeyValid = checkKey(output, magicBytes, 30)


maxKeys = 15
keyLen = 30

keys = [[33 for j in range(keyLen)] for i in range(maxKeys)] 

magicInts = list(struct.unpack('<' + str(keyLen) + 'i', magicBytes))

def checkChar(c, n):
    if isAsciiPrime(c) == False and c >> 4 == magicInts[n] or isAsciiPrime(c) == True and c >> 1 == magicInts[n]:
        return True
    return False

def brute(maxKeys):

    for i in range(0, maxKeys):
        for j in range(0, keyLen):
            for k in range(33, 127):
                if checkChar(k, j):
                    keys[i][j] = k







#print(magicInts)
#k = brute(0, 0, keys)
#print(k)
#brute(10)

brute(maxKeys)

for i in range(maxKeys):
    for j in range(keyLen):
            print(chr(keys[i][j]), end="")
    print()
