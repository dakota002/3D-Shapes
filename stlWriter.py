#python file to write .stl files
from random import randint as rInt
from random import random as rDec
from math import cos,sin,acos,pi,sqrt


#gets number of sides and shape
while True:
    try:
        sides=int(input("How many sides: "))
        break
    except (ValueError, NameError):
        print("Enter a valid integer")

while True:
    try:
        shape=str(input("Pyramid"))
        break
    except (ValueError,NameError,SyntaxError):
        print("Enter a valid shape")
    
#Reference points
origin = [0,0,0]
a=(1/sqrt(3))
unit = [a,a,a]

#function to make random vectors
def mkVect():
    global vect
    vect=[]
    for n in range(3):
        point=rDec()
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


#define Dot product of vectors
def Dot(vec1,vec2):
    return vec1[0]*vec2[0]+vec1[1]*vec2[1]+vec1[2]*vec2[2]

#define the length or norm of a vector
def Norm(vect):
    return sqrt(vect[0]**2+vect[1]**2+vect[2]**2)

#determines initial theta
def getTheta(vector_1,vector_2):
    theta = acos((Dot(vector_1,vector_2)/(Norm(vector_1)*Norm(vector_2))))
    return theta

#determines a rotation phi
def getPhi(sides):
    phi=(2*pi)/sides
    return phi

#rotation function
def rotation(phi,u,vect):
    u_x=u[0]
    u_y=u[1]
    u_z=u[2]
    R=[[cos(phi)+(u_x**2)*(1-cos(phi)),u_x*u_y*(1-cos(phi))-u_z*sin(phi),u_x*u_z*(1-cos(phi))+u_y*sin(phi)],
       [u_x*u_y*(1-cos(phi))+u_z*sin(phi),cos(phi)+(u_y**2)*(1-cos(phi)),u_y*u_z*(1-cos(phi))-u_x*sin(phi)],
       [u_x*u_z*(1-cos(phi))-u_y*sin(phi),u_y*u_z*(1-cos(phi))+u_x*sin(phi),cos(phi)+(u_z**2)*(1-cos(phi))]]
    new =[]
    for row in R:
        new.append(row[0]*vect[0]+row[1]*vect[1]+row[2]*vect[2])
    return new


#makes a pyramid and writes to stl file
def mkCone(sides):
    m=mkVect()
    vecMat=[origin,m]
    for i in range(sides-1):
        m=rotation(getPhi(sides),unit,m)
        vecMat.append(m)
    pyrMat=[]
    for i in range(2,sides+1):
        pyrMat.append([vecMat[0],vecMat[i-1],vecMat[i]])
    pyrMat.append([vecMat[0],vecMat[len(vecMat)-1],vecMat[1]])
    with open('object.stl', 'w') as file:
        file.write('\nsolid Default')
        for i in range(sides):
            file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
            for j in range(len(pyrMat[i])):
                file.write('      vertex '+str(pyrMat[i][j][0])+' '+str(pyrMat[i][j][1])+' '+str(pyrMat[i][j][2]))
                file.write('\n')
            file.write('    endloop\n  endfacet')
        file.write('\nendsolid Default')

if shape=='y':
    mkCone(sides)
