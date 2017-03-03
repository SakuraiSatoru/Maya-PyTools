import maya.cmds as cmds
import math
import maya.OpenMaya as om
import functools

def init(m,api,s,e):
    array0 = cmds.ls(sl = True, fl = True)
    for a in array0:
        if 'e[' in a:
            pt = cmds.polyListComponentConversion( a, tv=True )
            cmds.select(a,tgl = True)
            cmds.select(pt,tgl = True)
    align(m,api,s,e)

def disCal(p1,p2):
    disX = float(cmds.pointPosition(p1)[0])-float(cmds.pointPosition(p2)[0])
    disY = float(cmds.pointPosition(p1)[1])-float(cmds.pointPosition(p2)[1])
    disZ = float(cmds.pointPosition(p1)[2])-float(cmds.pointPosition(p2)[2])
    return math.sqrt(disX*disX+disY*disY+disZ*disZ)
    
    
    
def align(m,api,s,e):
    array = cmds.ls(sl = True, fl = True)
    if len(array) == 4:
        objArray = []
        for a in array:
            if not 'vtx[' in a:
                cmds.error('plz select 4 vertexs')
            obj0 = a.split('.')[0]
            objArray.append(obj0)
        obj1 = objArray[0]
        c = 0
        for a in objArray:
            if a!= obj1:
                obj2 = a
                c += 1
        if c!= 2:
            cmds.error('plz select 2 vertexs on each 2 polys')
    else:
        cmds.error('plz select 4 vertexs')

    if objArray[0] != objArray[1]:
        if objArray[1] == objArray[2]:
            d = array[1]
            array[1] = array[3]
            array[3] = d
        else:
            d = array[1]
            array[1] = array[2]
            array[2] = d
                  
    pointDis = [0,0,0,0]
    pointDis[0] = disCal(array[0],array[2])
    pointDis[1] = disCal(array[0],array[3])
    pointDis[2] = disCal(array[1],array[2])
    pointDis[3] = disCal(array[1],array[3])

    if pointDis.index(min(pointDis)) == 1:
        d = array[2]
        array[2] = array[3]
        array[3] = d
    elif pointDis.index(min(pointDis)) == 2:
        d = array[0]
        array[0] = array[1]
        array[1] = d
    elif pointDis.index(min(pointDis)) == 3:
        d = array[0]
        array[0] = array[1]
        array[1] = d
        d = array[2]
        array[2] = array[3]
        array[3] = d

    vector1 = [float(cmds.pointPosition(array[1])[0])-float(cmds.pointPosition(array[0])[0]),float(cmds.pointPosition(array[1])[1])-float(cmds.pointPosition(array[0])[1]),float(cmds.pointPosition(array[1])[2])-float(cmds.pointPosition(array[0])[2])]
    vector2 = [float(cmds.pointPosition(array[3])[0])-float(cmds.pointPosition(array[2])[0]),float(cmds.pointPosition(array[3])[1])-float(cmds.pointPosition(array[2])[1]),float(cmds.pointPosition(array[3])[2])-float(cmds.pointPosition(array[2])[2])]
    vector1 = om.MVector(vector1[0],vector1[1],vector1[2])
    vector2 = om.MVector(vector2[0],vector2[1],vector2[2])
    mQuaternion = om.MQuaternion(vector1, vector2, 1.0)
    mMatrix = mQuaternion.asMatrix()
    mTransformMtx = om.MTransformationMatrix(mMatrix)

    eulerRot = mTransformMtx.eulerRotation()

    
    angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]
    if not e:
        cmds.select(obj1)
    else:
        cmds.select(array[0],array[1])
    if api:
        sel = om.MSelectionList()
        dagPath = om.MDagPath()
        sel.add(obj1)
        sel.getDagPath(0, dagPath)
        selObj = om.MObject()
        sel.getDependNode(0,selObj)
        spc = om.MSpace.kTransform
        xformFn = om.MFnTransform(selObj)
        xformFn.rotateBy(mQuaternion,spc)
    else:
        angles0 = cmds.xform(ro = True, query = True)
        a0Pos = cmds.pointPosition(array[0])
        for i in range(3):
            angles[i] += angles0[i]
        cmds.xform(ro = (angles[0],angles[1], angles[2]), piv = cmds.pointPosition(array[0]), ws = True)
        if e:
            cmds.move(0-float(cmds.pointPosition(array[0])[0])+float(a0Pos[0]),0-float(cmds.pointPosition(array[0])[1])+float(a0Pos[1]),0-float(cmds.pointPosition(array[0])[2])+float(a0Pos[2]),relative=True)
    if m:
        cmds.move(float(cmds.pointPosition(array[2])[0])-float(cmds.pointPosition(array[0])[0]),float(cmds.pointPosition(array[2])[1])-float(cmds.pointPosition(array[0])[1]),float(cmds.pointPosition(array[2])[2])-float(cmds.pointPosition(array[0])[2]),relative=True)
    if s != 'None':
        dic = {'X':[1,0,0],'Y':[0,1,0],'Z':[0,0,1],'XY':[1,1,0],'XZ':[1,0,1],'YZ':[0,1,1],'XYZ':[1,1,1]}
        scale = disCal(array[2],array[3])/disCal(array[0],array[1])
        scaleArray = map(lambda x: scale**x,dic.get(s))
        print scaleArray
        cmds.scale(scaleArray[0],scaleArray[1],scaleArray[2],obj1,pivot = (cmds.pointPosition(array[0])[0],cmds.pointPosition(array[0])[1],cmds.pointPosition(array[0])[2]),ws = True)






'''
-------------creat UI-----------------
''' 

        
def createUI(pWindowTitle,pApplyCallback):
    windowID = 'RotateAlign2Polys'
    if cmds.window(windowID,exists = True):
        cmds.deleteUI(windowID)
    
    cmds.window(windowID,title = pWindowTitle,resizeToFitChildren = True,h = 600)
    
    cmds.rowColumnLayout(numberOfColumns = 2, columnWidth = [75,120])
    cmds.text(label = '   Move Together            ',al = 'left')
    checkBox1 = cmds.checkBox(label='')
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    cmds.text(label = '   3D Align (Can\'t Undo)   ',al = 'left')
    checkBox2 = cmds.checkBox(label='')
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    cmds.text(label = '   Only edges   ',al = 'left')
    checkBox3 = cmds.checkBox(label='')
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    cmds.text(label = '   Scale   ',al = 'left')
    optionMenu1 = cmds.optionMenu()
    cmds.menuItem( label='None' )
    cmds.menuItem( label='X' )
    cmds.menuItem( label='Y' )
    cmds.menuItem( label='Z' )
    cmds.menuItem( label='XY' )
    cmds.menuItem( label='XZ' )
    cmds.menuItem( label='YZ' )
    cmds.menuItem( label='XYZ' )
    cmds.separator(h = 10, style = 'none')
    cmds.separator(h = 10, style = 'none')
    cmds.button (label = 'Apply', command = functools.partial(pApplyCallback,checkBox1,checkBox2,checkBox3,optionMenu1))
    def cancelCallback(*pArgs):
        if cmds.window(windowID,exists = True):
            cmds.deleteUI(windowID)
    cmds.button (label = 'Cancel', command = cancelCallback)
    cmds.showWindow()
def applyCallback(pCheckBox1,pCheckBox2,pCheckBox3,pOptionMenu1,*pArgs):
    flag1 = cmds.checkBox(pCheckBox1,query = True,value = True)
    flag2 = cmds.checkBox(pCheckBox2,query = True,value = True)
    flag3 = cmds.optionMenu(pOptionMenu1,query = True,value = True)
    flag4 = cmds.checkBox(pCheckBox3,query = True,value = True)
    init(flag1,flag2,flag3,flag4)

createUI('RotateAlign2Polys',applyCallback)