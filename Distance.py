import maya.cmds as cmds
import math
import maya.OpenMaya as om
import functools





#################Measure Distance################
def measure():
    array0 = cmds.ls(sl = True, fl = True)
    for a in array0:
        if 'e[' in a:
            if len(array0)>1:
                cmds.error('select at most one edge!')
            pt = cmds.polyListComponentConversion( a, tv=True )
            cmds.select(a,tgl = True)
            cmds.select(pt,tgl = True)
        elif len(array0)>2:
            cmds.error('select at most two vertexs!')
    array0 = cmds.ls(sl = True, fl = True)
    currentUnit = cmds.currentUnit( query=True, linear=True )
    tmp = disCal(array0[0],array0[1])
    returnLst = [str(tmp[0])+str(currentUnit),str(tmp[1])+str(currentUnit),str(tmp[2])+str(currentUnit),str(tmp[3])+str(currentUnit)]
    return returnLst 
    
    
    
def disCal(p1,p2):
    disX = float(cmds.pointPosition(p1)[0])-float(cmds.pointPosition(p2)[0])
    disY = float(cmds.pointPosition(p1)[1])-float(cmds.pointPosition(p2)[1])
    disZ = float(cmds.pointPosition(p1)[2])-float(cmds.pointPosition(p2)[2])
    return [math.sqrt(disX*disX+disY*disY+disZ*disZ),abs(disX),abs(disY),abs(disZ)]
    
measure()



def createUI(pWindowTitle,dis):
    windowID = 'Distance'
    if cmds.window(windowID,exists = True):
        cmds.deleteUI(windowID)
    
    cmds.window(windowID,title = pWindowTitle,resizeToFitChildren = True,h = 50)
    
    cmds.rowColumnLayout(numberOfColumns = 1, columnWidth = [1,100])
    cmds.text(label = 'Distance:')
    cmds.text(label = dis[0])
    cmds.separator(h = 10, style = 'none')
    cmds.text(label = 'dx:')
    cmds.text(label = dis[1])
    cmds.separator(h = 10, style = 'none')
    cmds.text(label = 'dy:')
    cmds.text(label = dis[2])
    cmds.separator(h = 10, style = 'none')
    cmds.text(label = 'dz:')
    cmds.text(label = dis[3])
    cmds.separator(h = 10, style = 'none')
    def cancelCallback(*pArgs):
        if cmds.window(windowID,exists = True):
            cmds.deleteUI(windowID)
    cmds.button (label = 'OK', command = cancelCallback)
    cmds.showWindow()
createUI('Distance',measure())