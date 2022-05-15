from z3 import *

divArr = list(range(6))
divArr[0] = 0x007b; # 123
divArr[1] = 0x01c8; # 456
divArr[2] = 0x0315; # 789
divArr[3] = 0x03db; # 987
divArr[4] = 0x028e; # 643
divArr[5] = 0x0141; # 321

modArr = list(range(6))
modArr[0] = 0x005c; # 92
modArr[1] = 0x001d; # 29
modArr[2] = 0x017c; # 380
modArr[3] = 0x0002; # 2
modArr[4] = 0x01f1; # 497
modArr[5] = 0x0128; # 296

maxInput = 0xc


# mod solver via congruences - first check
import chrem

congruences = []
congruences.append((modArr[0], divArr[0]))
congruences.append((modArr[1], divArr[1]))
congruences.append((modArr[2], divArr[2]))
congruences.append((modArr[3], divArr[3]))
congruences.append((modArr[4], divArr[4]))
congruences.append((modArr[5], divArr[5]))
cgrSolution = chrem.chrem_multiple(congruences)
print("magic: ", hex(cgrSolution[0]))

# mod solver via z3 and ascii sum generator - first check 

solver = Solver()
input = [BitVec('input%d'%i, 48) for i in range(maxInput)]

minAscii = 32
maxAscii = 126

# fixed value ascii sum is added up to
sumAscii = 0x7fffffff

def findTheNumber():
    global sumAscii

    # generate 
    exprSum = ""
    for i in range(1, maxInput):
        solver.add(And(input[i] >= minAscii, input[i] <= maxAscii))
        exprSum += 'input[' + str(i) + '] * ' + str(i) + ' +'

    # generate constraints 
    exprFin0 = "(" + exprSum + str(sumAscii) + ") % divArr[0] == modArr[0]"
    exprFin1 = "(" + exprSum + str(sumAscii) + ") % divArr[1] == modArr[1]"
    exprFin2 = "(" + exprSum + str(sumAscii) + ") % divArr[2] == modArr[2]"
    exprFin3 = "(" + exprSum + str(sumAscii) + ") % divArr[3] == modArr[3]"
    exprFin4 = "(" + exprSum + str(sumAscii) + ") % divArr[4] == modArr[4]"
    exprFin5 = "(" + exprSum + str(sumAscii) + ") % divArr[5] == modArr[5]"

    solver.add(eval(exprFin0))
    solver.add(eval(exprFin1))
    solver.add(eval(exprFin2))
    solver.add(eval(exprFin3))
    solver.add(eval(exprFin4))
    solver.add(eval(exprFin5))

    print(solver.check())

    while solver.check() == sat:
        #print(solver.model())
        m = solver.model()
    
        key = ""
        magicSum = 0
    
        for i in range(1, maxInput):
    
            asciiVal = m[input[i]].as_long()
            key += chr(asciiVal)
            magicSum += asciiVal * i

        sumAscii += magicSum
    
        # this will give us the same asciiSum like congruences method
        print(magicSum, hex(magicSum), hex(sumAscii), key) # we need key to pass two checks and get to the shellcode

        break # take first that satisfy rule and break since there are too many of them, we just want to pass the first two check loops, decrypt shellcode and check the key logic there


findTheNumber()


# xor and comparison bytes retrieved from the shellcode
#result = [0x94, 0x97, 0xe3, 0x8e, 0x34 ,0xa6, 0x36, 0x8a] #little endian
result = [0x8a, 0x36, 0xa6, 0x34, 0x8e, 0xe3, 0x97, 0x94,   0xa7, 0xd4, 0xd8, 0x95,   0x83, 0xb2]
#xorVars = [0xfb, 0xe0, 0xbc, 0xe1, 0x58, 0xca, 0x53 ,0xe2] #little endian
xorVals = [0xe2, 0x53, 0xca, 0x58, 0xe1, 0xbc, 0xe0, 0xfb,  0xd5, 0xb8, 0xbc, 0xca,   0xb7, 0x80]

# get to the key
pwd = list(x ^ y for x, y in zip(xorVals,result))
#print([hex(x) for x in pwd])
print("key:", "".join([chr(x) for x in pwd]))
