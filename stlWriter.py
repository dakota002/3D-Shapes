#python file to write .stl files
from random import randint as rInt
from random import random as rDec
from math import cos,sin,acos,pi,sqrt

#gets shape, reflection, etc
while True:
    try:
        shape=str(input("Cone, Cube: "))
        break
    except (ValueError,NameError,SyntaxError):
        print("Enter a valid shape")

if shape.lower()=='cone':
    while True:
        try:
            mirror=str(input("Mirror object: "))
            break
        except(ValueError,NameError,SyntaxError):
            print("Choose a valid option")

    if mirror.lower()=='y':
        while True:
            try:
                mAxis=str(input("x, y, or z"))
                break
            except(ValueError,NameError,SyntaxError):
                print("Choose valid axis")

#Reference points
origin = [0,0,0]
a=(1/sqrt(3))
unit = [a,a,a]

#function to make random vectors
def mkVect():
    global vect
    vect=[]
    for n in range(3):
        point=rDec()*10
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


#define Dot product of [x,y,z] vectors
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


#makes a closed cone centered at the origin and writes to stl file
def mkCone():
    while True:
        try:
            sides=int(input("How many sides: "))
            break
        except (ValueError, NameError):
            print("Enter a valid integer")
    m=mkVect()
    vecMat=[origin,m]
    for i in range(sides-1):
        m=rotation(getPhi(sides),unit,m)
        vecMat.append(m)
    pyrMat=[]
    for i in range(2,sides+1):
        pyrMat.append([vecMat[0],vecMat[i-1],vecMat[i]])
    pyrMat.append([vecMat[0],vecMat[len(vecMat)-1],vecMat[1]])
    while True:
        try:
            update=str(input("Update or overwrite: "))
            break
        except (NameError,SyntaxError):
            print("Try again: ")
    if (update.lower() in ('u','update'))==True:
        fType='a+'
    elif (update.lower() in ('o','overwrite'))==True:
        fType='w+'
    with open('object.stl', fType) as file:
        file.write('\nsolid Default')
        for i in range(sides):
            file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
            for j in range(len(pyrMat[i])):
                file.write('      vertex '+str(pyrMat[i][j][0])+' '+str(pyrMat[i][j][1])+' '+str(pyrMat[i][j][2]))
                file.write('\n')
            file.write('    endloop\n  endfacet')
        for i in range(len(pyrMat)-2):
            file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
            file.write('      vertex '+str(vecMat[1][0])+' '+str(vecMat[1][1])+' '+str(vecMat[1][2]))
            file.write('\n')
            for j in range(1,3):
                file.write('      vertex '+str(vecMat[i+j+1][0])+' '+str(vecMat[i+j+1][1])+' '+str(vecMat[i+j+1][2]))
                file.write('\n')
            file.write('    endloop\n  endfacet')
        file.write('\nendsolid Default')



#reflects the shape about an axis
def reflect(mAxis):
    refList=[]
    with open('object.stl','r') as file:
        for line in file:
            if ('vertex' in line)== True:
                refList.append([float(line[13:line.find(' ',13)]),
                               float(line[line.find(' ',13)+1:line.find(' ',line.find(' ',line.find(' ',13)+1))]),
                               float(line[line.find(' ',line.find(' ',line.find(' ',13)+1)):len(line)-1])])
    refMat=[]
    for i in range(len(refList)/3):
        refMat.append([refList.pop(0),refList.pop(0),refList.pop(0)])
    
    if ('x' in mAxis)==True:
        with open('object.stl','a') as file:
            file.write('\nsolid Default')
            for subls in refMat:
                file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
                for points in subls:
                    file.write('      vertex '+str(-points[0])+' '+str(points[1])+' '+str(points[2]))
                    file.write('\n')
                file.write('    endloop\n  endfacet')
            file.write('\nendsolid Default')
    if ('y' in mAxis)==True:
        with open('object.stl','a') as file:
            file.write('\nsolid Default')
            for subls in refMat:
                file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
                for points in subls:
                    file.write('      vertex '+str(points[0])+' '+str(-points[1])+' '+str(points[2]))
                    file.write('\n')
                file.write('    endloop\n  endfacet')
            file.write('\nendsolid Default')
    if ('z' in mAxis)==True:
        with open('object.stl','a') as file:
            file.write('\nsolid Default')
            for subls in refMat:
                file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
                for points in subls:
                    file.write('      vertex '+str(points[0])+' '+str(points[1])+' '+str(-points[2]))
                    file.write('\n')
                file.write('    endloop\n  endfacet')
            file.write('\nendsolid Default')
    if (('x' in mAxis) and ('y' in mAxis))==True:
        with open('object.stl','a') as file:
            file.write('\nsolid Default')
            for subls in refMat:
                file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
                for points in subls:
                    file.write('      vertex '+str(-points[0])+' '+str(-points[1])+' '+str(points[2]))
                    file.write('\n')
                file.write('    endloop\n  endfacet')
            file.write('\nendsolid Default')
    if (('x' in mAxis) and ('z' in mAxis))==True:
        with open('object.stl','a') as file:
            file.write('\nsolid Default')
            for subls in refMat:
                file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
                for points in subls:
                    file.write('      vertex '+str(-points[0])+' '+str(points[1])+' '+str(-points[2]))
                    file.write('\n')
                file.write('    endloop\n  endfacet')
            file.write('\nendsolid Default')
    if (('y' in mAxis) and ('z' in mAxis))==True:
        with open('object.stl','a') as file:
            file.write('\nsolid Default')
            for subls in refMat:
                file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
                for points in subls:
                    file.write('      vertex '+str(points[0])+' '+str(-points[1])+' '+str(-points[2]))
                    file.write('\n')
                file.write('    endloop\n  endfacet')
            file.write('\nendsolid Default')
    if (('x' in mAxis) and ('y' in mAxis) and ('z' in mAxis))==True:
        with open('object.stl','a') as file:
            file.write('\nsolid Default')
            for subls in refMat:
                file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
                for points in subls:
                    file.write('      vertex '+str(-points[0])+' '+str(-points[1])+' '+str(-points[2]))
                    file.write('\n')
                file.write('    endloop\n  endfacet')
            file.write('\nendsolid Default')

#makes cubes centered at the origin
def mkCube():
    while True:
        try:
            size=int(input("Length of a side: "))
            break
        except (ValueError, NameError):
            print("Enter a valid integer")
    while True:
        try:
            update=str(input("Update or overwrite: "))
            break
        except (NameError,SyntaxError):
            print("Try again: ")
    if (update.lower() in ('u','update'))==True:
        fType='a+'
    elif (update.lower() in ('o','overwrite'))==True:
        fType='w+'
    E=float(size/2)
    corners=[[E,E,E],
             [-E,E,E],
             [-E,-E,E],
             [E,-E,E],
             [E,-E,-E],
             [E,E,-E],
             [-E,E,-E],
             [-E,-E,-E]]
    eTryMat=[]
    for i in range(5):
        eTryMat.append([corners[0],corners[i+1],corners[i+2]])
    eTryMat.append([corners[0],corners[6],corners[1]])
    for i in range(5):
        eTryMat.append([corners[7],corners[i+1],corners[i+2]])
    eTryMat.append([corners[7],corners[6],corners[1]])
    with open('object.stl',fType) as file:
        file.write('\nsolid Default')
        for i in range(12):
            file.write('\n  facet normal 0.000000e+00 0.000000e+00 -1.000000e+00 \n    outer loop \n')
            for j in range(len(eTryMat[i])):
                file.write('      vertex '+str(eTryMat[i][j][0])+' '+str(eTryMat[i][j][1])+' '+str(eTryMat[i][j][2]))
                file.write('\n')
            file.write('    endloop\n  endfacet')
        file.write('\nendsolid Default')

if shape.lower()=='cone':
    mkCone()
    if mirror=='y':
        reflect(mAxis)
elif shape.lower()=='cube':
    mkCube()
