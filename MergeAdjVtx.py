import maya.cmds as cmds;
import math;

def main():
    array = cmds.ls(sl = True, fl = True);
    objArray = []
    obj1Vtx = []
    obj2Vtx = []
    objArray.append(array[0].split('.')[0])
    for a in array:
        if (objArray[0] != a.split('.')[0]):
            objArray.append(a.split('.')[0])
            obj2Vtx.append(a)
        else:
            obj1Vtx.append(a)
            
    print(obj1Vtx)
    print(obj2Vtx)
    
    
    # a to b
    checkArray = [0 for n in xrange(len(obj2Vtx))]
    count = 0
    for a in obj1Vtx:
        abArray = [a]
        minDist = -1
        i = 0
        j = 0
        for b in obj2Vtx:
            dist = disCal(a,b)
            if(minDist == -1 or minDist > dist):
                minDist = dist
                if(len(abArray) > 1):
                    abArray.pop()
                abArray.append(b)
                j = i
            i += 1
        #print abArray
        checkArray[j]  += 1
        cmds.select(cl = True)
        cmds.select(a)
        cmds.move(float(cmds.pointPosition(abArray[1])[0])-float(cmds.pointPosition(abArray[0])[0]),float(cmds.pointPosition(abArray[1])[1])-float(cmds.pointPosition(abArray[0])[1]),float(cmds.pointPosition(abArray[1])[2])-float(cmds.pointPosition(abArray[0])[2]),relative=True)
        print("moving:",count,"all",len(obj1Vtx))
        count += 1
        cmds.select(cl = True)
        
        
        
        
    #b to a
    obj3Vtx = []
    count = 0
    for i in xrange(len(checkArray)):
        if (checkArray[i] == 0):
            obj3Vtx.append(obj2Vtx[i])
    for a in obj3Vtx:
        abArray = [a]
        minDist = -1
        for b in obj1Vtx:
            dist = disCal(a,b)
            if(minDist == -1 or minDist > dist):
                minDist = dist
                if(len(abArray) > 1):
                    abArray.pop()
                abArray.append(b)
        cmds.select(cl = True)
        cmds.select(a)
        cmds.move(float(cmds.pointPosition(abArray[1])[0])-float(cmds.pointPosition(abArray[0])[0]),float(cmds.pointPosition(abArray[1])[1])-float(cmds.pointPosition(abArray[0])[1]),float(cmds.pointPosition(abArray[1])[2])-float(cmds.pointPosition(abArray[0])[2]),relative=True)
        print("check:",count,"all",len(obj3Vtx))
        count += 1
        cmds.select(cl = True)
    


def disCal(p1,p2):
    disX = float(cmds.pointPosition(p1)[0])-float(cmds.pointPosition(p2)[0])
    disY = float(cmds.pointPosition(p1)[1])-float(cmds.pointPosition(p2)[1])
    disZ = float(cmds.pointPosition(p1)[2])-float(cmds.pointPosition(p2)[2])
    return math.sqrt(disX*disX+disY*disY+disZ*disZ)
    
    
main()