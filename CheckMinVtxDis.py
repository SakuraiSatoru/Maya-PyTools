import maya.cmds as cmds
import math
import functools

def disCal(p1,p2):
    disX = float(cmds.pointPosition(p1)[0])-float(cmds.pointPosition(p2)[0])
    disY = float(cmds.pointPosition(p1)[1])-float(cmds.pointPosition(p2)[1])
    disZ = float(cmds.pointPosition(p1)[2])-float(cmds.pointPosition(p2)[2])
    return math.sqrt(disX*disX+disY*disY+disZ*disZ)

def find(dis0):
    array = cmds.ls(sl = True, fl = True)
    if array[1]:
        n = len(array)
        for i in range(0,n-1):
            j = 0
            while j < i:
                dis = disCal(array[i],array[j])
                print dis
                if dis < dis0:
                    cmds.select(array[i],array[j])
                    return
                else:
                    j += 1
                    
        


 

        
def createUI(pWindowTitle,pApplyCallback):
    windowID = 'CloseVertexs'
    if cmds.window(windowID,exists = True):
        cmds.deleteUI(windowID)
    
    cmds.window(windowID,title = pWindowTitle,resizeToFitChildren = True,h = 600)
    
    cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [75,120])
    cmds.text(label = 'Threshold: ')
    TextField = cmds.textField(text = '0.01')
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    cmds.button (label = 'Find', command = functools.partial(pApplyCallback,TextField))
    def cancelCallback(*pArgs):
        if cmds.window(windowID,exists = True):
            cmds.deleteUI(windowID)
    cmds.button (label = 'Cancel', command = cancelCallback)
    cmds.showWindow()
def applyCallback(pTextField,*pArgs):
    str = cmds.textField(pTextField,query = True,text = True)
    dis0 = float(str)
    if dis0:
        find(dis0)
createUI('CloseVertexs',applyCallback)
    