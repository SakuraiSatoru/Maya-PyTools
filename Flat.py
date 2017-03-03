import maya.cmds as cmds
import functools
def init(axis):
    array = cmds.ls(sl = True, fl = True)
    if axis == 'z':
        for a in array:
            cmds.move(0,0,-float(cmds.pointPosition(a)[2])+float(cmds.pointPosition(array[0])[2]),a,relative=True)
    if axis == 'y':
        for a in array:
            cmds.move(0,-float(cmds.pointPosition(a)[1])+float(cmds.pointPosition(array[0])[1]),0,a,relative=True)
    if axis == 'x':
        for a in array:
            cmds.move(-float(cmds.pointPosition(a)[0])+float(cmds.pointPosition(array[0])[0]),0,0,a,relative=True)
def createUI(pWindowTitle,pApplyCallback):
    windowID = 'FlatVet'
    if cmds.window(windowID,exists = True):
        cmds.deleteUI(windowID)
    cmds.window(windowID,title = pWindowTitle,resizeToFitChildren = True,h = 600)
    cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [75,120])
    cmds.text(label = 'Flat axis    ',al = 'left')
    optionMenu1 = cmds.optionMenu()
    cmds.menuItem( label='x' )
    cmds.menuItem( label='y' )
    cmds.menuItem( label='z' )
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    cmds.button (label = 'Apply', command = functools.partial(pApplyCallback,optionMenu1))
    def cancelCallback(*pArgs):
        if cmds.window(windowID,exists = True):
            cmds.deleteUI(windowID)
    cmds.button (label = 'Cancel', command = cancelCallback)
    cmds.showWindow()
    cmds.optionMenu(optionMenu1,edit = True,sl = 3)
def applyCallback(pOptionMenu1,*pArgs):
    sel = cmds.optionMenu(pOptionMenu1,query = True,value = True)
    init(sel)
createUI('FlatVet',applyCallback)