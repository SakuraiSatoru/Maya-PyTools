import maya.cmds as cmds
import functools


def creatCurve(a,b):
    c = cmds.curve( d = 1, p=[cmds.pointPosition(a),cmds.pointPosition(b)] )
    return c


def init(flag1,flag2):
    array0 = cmds.ls(sl = True, fl = True)
    cmds.select(cl = True)
    for a in array0:
        if 'e[' in a:
            #cmds.error('Vertex Only')
            
            cmds.select(cmds.polyListComponentConversion(a, tv = True),add = True)
            array0 = cmds.ls(sl = True, fl = True)
    if len(array0) != 3 and len(array0) != 4:
        cmds.error('3 or 4 Vertex')
    main(array0,flag1,flag2)


def main(array,flag1,flag2):
    if flag2 == 'None':
        c1 = creatCurve(array[0],array[1])
        c2 = creatCurve(array[-1],array[-2])
    elif flag2 == '1':
        c1 = creatCurve(array[0],array[-2])
        c2 = creatCurve(array[1],array[-1])
    else:
        c1 = creatCurve(array[0],array[-1])
        c2 = creatCurve(array[1],array[-2])
    cmds.loft( c1, c2, ch=True, rn=True, ar=True, po = True )
    cmds.delete(c1,c2)
    if flag1:
        obj0 = array[0].split('.')[0]
        obj1 = cmds.ls(sl = True, fl = True)[0]
        cmds.polyUnite(obj0,obj1)
        obj2 = cmds.ls(sl = True, fl = True)[0]
        array1 = []
        for a in array:
            a = obj2 + '.' + a.split('.')[1]
            array1.append(a)
        cmds.select(cmds.polyListComponentConversion(obj2, tv = True))
        n0 = cmds.ls(sl = True, fl = True)
        if len(array) == 4:
            cmds.select(n0[-4:])
        else:
            cmds.select(n0[-3:])
        cmds.select(array1,add = True)
        cmds.polyMergeVertex(d = 0.001)
        cmds.select(obj2)



def createUI(pWindowTitle,pApplyCallback):
    windowID = 'CreateSurface'
    if cmds.window(windowID,exists = True):
        cmds.deleteUI(windowID)
    
    cmds.window(windowID,title = pWindowTitle,resizeToFitChildren = True,h = 600)
    
    cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [75,120])
    cmds.text(label = '   Filp            ',al = 'left')
    optionMenu1 = cmds.optionMenu()
    cmds.menuItem( label='None' )
    cmds.menuItem( label='1' )
    cmds.menuItem( label='2' )
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    cmds.text(label = '   Merge   ',al = 'left')
    checkBox1 = cmds.checkBox(label='')
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    cmds.button (label = 'Apply', command = functools.partial(pApplyCallback,checkBox1,optionMenu1))
    def cancelCallback(*pArgs):
        if cmds.window(windowID,exists = True):
            cmds.deleteUI(windowID)
    cmds.button (label = 'Cancel', command = cancelCallback)
    cmds.showWindow()
def applyCallback(pCheckBox1,pOptionMenu1,*pArgs):
    flag1 = cmds.checkBox(pCheckBox1,query = True,value = True)
    flag2 = cmds.optionMenu(pOptionMenu1,query = True,value = True)
    init(flag1,flag2)

createUI('CreateSurface',applyCallback)