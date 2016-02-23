#python file to write .stl files
import math
import random as rng

#gets number of sides. Will round down
while True:
    try:
        sides=int(input("How many sides: "))
        break
    except (ValueError, NameError):
        print("Enter a valid integer")

#Reference point
origin = [0,0,0]

#function to make random vectors
def mkVect():
    global vect
    vect=[]
    for n in range(3):
        point=rng.randint(0,9)
        vect.append(point)
    return vect

#creates a matrix of each set of 3 points which make a triangle

def mkPmat():
    global pMat
    pMat=[origin]
    for m in range(2):
        mkVect()
        pMat.append(vect)
    return pMat

#creates a matrix of sides

def mkSmat(sides):
    global sMat
    sMat=[]
    sMat.append(mkPmat())
    for l in range(1,sides-1):
        tempVect1=sMat[l-1][1]
        tempVect2=sMat[l-1][2]
        sMat.append([tempVect1,tempVect2,mkVect()])
    sMat.append([sMat[len(sMat)-1][1], sMat[len(sMat)-1][2],sMat[0][0]])
    return sMat

#create random 3D object and write it to stl file
def makeSide(sides):
    with open('object.stl', 'w') as file:
        file.write('solid Default')
        mkSmat(sides)
        for i in range(sides):
            file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
            for j in range(3):
                file.write('      vertex '+str(sMat[i][j][0])+' '+str(sMat[i][j][1])+' '+str(sMat[i][j][2]))
                file.write('\n')
            file.write('    endloop\n  endfacet')
        file.write('\nendsolid Default')


#makes a triangular pyramid if sides = 4 and writes to stl file
def triPyr():
    temp=[]
    for i in range(3):
        temp.append(mkVect())
    pyrMat=[[origin,temp[0],temp[1]],
            [origin,temp[0],temp[2]],
            [origin,temp[1],temp[2]],
            temp]
    with open('object.stl', 'w') as file:
        file.write('\nsolid Default')
        for i in range(sides):
            file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
            for j in range(3):
                file.write('      vertex '+str(pyrMat[i][j][0])+' '+str(pyrMat[i][j][1])+' '+str(pyrMat[i][j][2]))
                file.write('\n')
            file.write('    endloop\n  endfacet')
        file.write('\nendsolid Default')
if sides==4:
    triPyr()

else:
    makeSide(sides)
