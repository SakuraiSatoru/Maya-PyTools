import maya.cmds as cmds
import math
import functools

'''
-------------center distance-----------------
''' 


def movePoints(x,y,z):
    vector = [x,y,z]
    array = []
    if (cmds.ls(sl = True)):
        array = cmds.ls(sl = True, fl = True)
        cPosX = 0
        cPosY = 0
        cPosZ = 0
        for a in array:
            cPosX += cmds.pointPosition(a)[0]
            cPosY += cmds.pointPosition(a)[1]
            cPosZ += cmds.pointPosition(a)[2]
        cPosX /= len(array)
        cPosY /= len(array)
        cPosZ /= len(array)
        cPos = [cPosX,cPosY,cPosZ]
        disArray = []
        for a in array:
            pDis = pDistance (cPos,cmds.pointPosition(a))
            disArray.append(pDis)
            
        maxDis = max(disArray)
        for i in range(0, len(array)-1):
            tVector = vector[:]
            tVector[0] *= 0.5*(math.cos(disArray[i]*math.pi/maxDis)+1)
            tVector[1] *= 0.5*(math.cos(disArray[i]*math.pi/maxDis)+1)
            tVector[2] *= 0.5*(math.cos(disArray[i]*math.pi/maxDis)+1)
            cmds.move(tVector[0],tVector[1],tVector[2],array[i], relative = True)
        
        
        
def pDistance (x,y):
    pDis = math.sqrt(abs((float(x[0])-float(y[0]))*(float(x[0])-float(y[0]))+(float(x[1])-float(y[1]))*(float(x[1])-float(y[1]))+(float(x[2])-float(y[2]))*(float(x[2])-float(y[2]))))
    return pDis
    
    
'''
-------------boarder level-----------------
''' 

def checkBoarder(pointCloud,minDisX,minDisY):
    xyArray = []
    boarderArray = []
    nonBoarderArray = []
    for p in pointCloud:
        px = float(cmds.pointPosition(p)[0])
        py = float(cmds.pointPosition(p)[1])
        pxy = [px,py]
        xyArray.append(pxy)
    for p in pointCloud:
        #flag = 0
        px = float(cmds.pointPosition(p)[0])
        py = float(cmds.pointPosition(p)[1])
        upP = 0
        downP = 0
        leftP = 0
        rightP = 0
        for xy in xyArray:
            if px - xy[0] > 0.8*minDisX and px - xy[0] < 1.2*minDisX and abs(py - xy[1]) < 0.2*minDisY:
                leftP = 1
            if xy[0] - px > 0.8*minDisX and xy[0] - px < 1.2*minDisX and abs(py - xy[1]) < 0.2*minDisY:
                rightP = 1
            if py - xy[1] > 0.8*minDisY and py - xy[1] < 1.2*minDisY and abs(px - xy[0]) < 0.2*minDisX:
                downP = 1
            if xy[1] - py > 0.8*minDisY and xy[1] - py < 1.2*minDisY and abs(px - xy[0]) < 0.2*minDisX:
                upP = 1
        if leftP*rightP*downP*upP == 0:
            boarderArray.append(p)
        else:
            nonBoarderArray.append(p)
    return [boarderArray,nonBoarderArray]
    
    
def moveLevels(x,y,z,level):
    vector = [x,y,z]
    if (cmds.ls(sl = True)):
            pointArray = cmds.ls(sl = True, fl = True)
            a0x = float(cmds.pointPosition(pointArray[0])[0])
            a0y = float(cmds.pointPosition(pointArray[0])[1])
            x = 0
            y = 0
            for i in range(1,len(pointArray)-1):
                ix = float(cmds.pointPosition(pointArray[i])[0])
                iy = float(cmds.pointPosition(pointArray[i])[1])
                if ((x == 0) or (x > abs(ix-a0x)) and abs(ix-a0x) != 0):
                    x = abs(ix - a0x)
                if ((y == 0) or (y > abs(iy-a0y)) and abs(iy-a0y) != 0):
                    y = abs(iy - a0y)
            arrangedArray = []
            
            remainPointsNum = len(pointArray)
            #print remainPointsNum
            while remainPointsNum > 0 and level>0:
                checkResult = checkBoarder(pointArray,x,y)
                arrangedArray.append(checkResult[0])
                remainPointsNum = len(checkResult[1])
                pointArray = checkResult[1]
                level -= 1
            if remainPointsNum > 0:
                for a in checkResult[1]:
                    arrangedArray[-1].append(a)
            n = len(arrangedArray)
            print "n = "+str(n)
            for i in range(n):
                tVector = vector[:]
                tVector[0] *= 0.5*(math.cos((n-1-i)*math.pi/n)+1)
                tVector[1] *= 0.5*(math.cos((n-1-i)*math.pi/n)+1)
                tVector[2] *= 0.5*(math.cos((n-1-i)*math.pi/n)+1)
                cmds.move(tVector[0],tVector[1],tVector[2],arrangedArray[i], relative = True)

    
    
    
'''
-------------creat UI-----------------
''' 

        
def createUI(pWindowTitle,pApplyCallback):
    windowID = 'SoftMove'
    if cmds.window(windowID,exists = True):
        cmds.deleteUI(windowID)
    
    cmds.window(windowID,title = pWindowTitle,resizeToFitChildren = True,h = 600)
    
    cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [75,120])
    cmds.text(label = 'Vector like 0,0,10: ')
    TextField = cmds.textField(text = '0,0,10')
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    cmds.text(label = 'use Level numbers (0=disable) ')
    IntField = cmds.intField()
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    cmds.button (label = 'Apply', command = functools.partial(pApplyCallback,TextField,IntField))
    def cancelCallback(*pArgs):
        if cmds.window(windowID,exists = True):
            cmds.deleteUI(windowID)
    cmds.button (label = 'Cancel', command = cancelCallback)
    cmds.showWindow()
def applyCallback(pTextField,pIntField,*pArgs):
    str = cmds.textField(pTextField,query = True,text = True)
    int = cmds.intField(pIntField,query = True,value = True)
    vector0 = str.split(",")
    if not int:
        movePoints(float(vector0[0]),float(vector0[1]),float(vector0[2]))
    else:
        moveLevels(float(vector0[0]),float(vector0[1]),float(vector0[2]),int)
createUI('Soft Move',applyCallback)