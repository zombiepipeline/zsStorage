"""
Based on https://github.com/renaudll/omtk/blob/master/omtk/libs/libRigging.py
"""
import os
from maya import cmds
from pymel import core as pymel

def _is_ctrl(ctrl):
    """
    Expect a transform, return True if the transform contain at least one nurbsCurve shape.
    """
    return any(shape for shape in ctrl.getShapes() if isinstance(shape, pymel.nodetypes.NurbsCurve))

def get_all_ctrls():
    ctrls = pymel.ls('*_Ctrl')
    ctrls = filter(_is_ctrl, ctrls)
    return ctrls

def get_all_ctrlsnapshots():
    snapshots = pymel.ls('*_CtrlSnapshot')
    snapshots = filter(_is_ctrl, snapshots)
    return snapshots

transferable_shape_attrs = [
    'overrideEnabled',
    'overrideColor',
    'overrideColorRGB'
]
def _duplicate_shape(old_shape):
    new_shape = pymel.createNode('nurbsCurve')

    # Transfert various attributes
    mel_dst = '{0}.create'.format(new_shape) # prevent annoying pymel warning
    pymel.connectAttr(old_shape.local, mel_dst)
    new_shape.create.evaluate() # Force maya to cache the shape before unconnecting
    pymel.disconnectAttr(old_shape.local, mel_dst)

    # Transfert various attributes
    for att_name in transferable_shape_attrs:
        att_old = old_shape.attr(att_name)
        att_new = new_shape.attr(att_name)
        att_new.set(att_old.get())

    return new_shape

def hold_ctrl_shapes(ctrl, parent=None):
    """
    Make a snapshot of all shapes of a specific ctrls.
    """
    shapes = filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), ctrl.getShapes())
    snapshot_transform = pymel.duplicate(ctrl, parentOnly=True, returnRootsOnly=True)[0]
    for shape in shapes:
        shape_snapshot = _duplicate_shape(shape)
        tmp_transform = shape_snapshot.getParent()
        shape_snapshot.setParent(snapshot_transform, s=True, r=True)
        pymel.delete(tmp_transform)
    if parent:
        snapshot_transform.setParent(parent)
    else:
        snapshot_transform.setParent(world=True)
    snapshot_transform.rename('{0}Snapshot'.format(ctrl.name()))
    return snapshot_transform


def check_ctrl_shape_vis_connection(target):
    """
    Return the visibility connections for the shapes:
    """
    for targetShape in target.getShapes():
        connected = cmds.listConnections(targetShape+".visibility", source=True, destination=False, plugs=True)
        if connected:
            return connected[0]


def fetch_ctrl_shapes(source, target):
    """
    Restore a snapshot for all shapes of a specific ctrls.
    """
    # store income connection to control shape before replace it
    connected = check_ctrl_shape_vis_connection(target)

    # Remove any previous shapes
    pymel.delete(filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), target.getShapes()))

    # Working with shape order trying to keep the shape as the first child node of the transform
    childrenGrp = None
    children = target.getChildren()
    if children:
        childrenGrp = pymel.group(children, name='dpTemp_DestChildren_Grp')
        pymel.parent(childrenGrp, world=True)
    
    for source_shape in source.getShapes():
        shape_snapshot = _duplicate_shape(source_shape)
        tmp_transform = shape_snapshot.getParent()
        shape_snapshot.setParent(target, r=True, s=True)
        shape_snapshot.rename(target.name() + 'Shape')
        pymel.delete(tmp_transform)
        # Restore visibility connections.
        if connected:
            cmds.connectAttr(connected, target.name()+'Shape.visibility', force=True)

    if children:
        pymel.parent(children, target)
        pymel.delete(childrenGrp)

    # TODO: Restore AnnotationShapes
    #pymel.delete(source)

def hold_all_ctrls_shapes(**kwargs):
    """
    Make a snapshot of all shapes of all ctrls.
    """
    ctrls = get_all_ctrls()
    return [hold_ctrl_shapes(oCtrl, **kwargs) for oCtrl in ctrls]


def fetch_all_ctrls_shapes():
    """
    Restore the snapshots of all shapes of all ctrls.
    """
    aSources = get_all_ctrlsnapshots()

    for oSource in aSources:
        sTargetName = oSource.name()[:-8]
        if len(cmds.ls(sTargetName)) == 1:
            if pymel.objExists(sTargetName):
                oTarget = pymel.PyNode(str(sTargetName))
                fetch_ctrl_shapes(oSource, oTarget)
            else:
                pymel.warning("Can't find {0}".format(sTargetName))
        else:
            pymel.warning("Skipped: more than one object named {0}".format(sTargetName))

def get_default_path_snapshot(current_path=None):
    if current_path is None:
        # Resolve current path
        current_path = cmds.file(q=True, sceneName=True)
        if not current_path:
            pymel.warning("Please save your scene!")
            return

    current_path_dirname = os.path.dirname(current_path)
    current_path_basename = os.path.basename(current_path)
    current_path_filename, current_path_fileext = os.path.splitext(current_path_basename)
    return os.path.join(current_path_dirname, '{0}_Shapes{1}'.format(current_path_filename, current_path_fileext))

def save_all_ctrls_shapes(path=None, **kwargs):
    # Resolve current path
    current_path = cmds.file(q=True, sceneName=True)
    if not current_path:
        pymel.warning("Please save your scene!")
        return

    # Resolve path
    if path is None:
        path = get_default_path_snapshot(current_path)

    cmds.undoInfo(openChunk=True)

    snapshots = hold_all_ctrls_shapes(**kwargs)
    if snapshots:
        pymel.select(snapshots)
        cmds.file(rename=path)
        cmds.file(exportSelected=True, type='mayaAscii', prompt=False, force=True)
        cmds.file(rename=current_path)
        pymel.delete(snapshots)
        print('Exported shapes to: {0}'.format(path))
        return True

    cmds.undoInfo(closeChunk=True)

    return False

def load_all_ctrls_shapes(path=None):
    # Resolve path
    if path is None:
        path = get_default_path_snapshot()

    # Ensure path exists
    if not os.path.exists(path):
        pymel.warning("File doesn't exist: {0}".format(path))
        return False

    ref = pymel.createReference(path, defaultNamespace=True)
    fetch_all_ctrls_shapes()
    ref.remove()

    return True

#
# dpAutoRig implementation
#

# global variables to this module:
CLASS_NAME = "CopyPasteShapes"
TITLE = "m137_copyPasteShapes"
DESCRIPTION = "m138_copyPasteShapesDesc"
ICON = "/Icons/dp_copyPasteShapes.png"

class CopyPasteShapes(object):
    def __init__(self, *args, **kwargs):
        if cmds.window("sqCopyPasteShapesWindow", query=True, exists=True):
            cmds.deleteUI("sqCopyPasteShapesWindow")

        win = cmds.window('sqCopyPasteShapesWindow', title='CopyPasteShapes', widthHeight=(200, 100), menuBar=False, sizeable=True, minimizeButton=True, maximizeButton=False, menuBarVisible=False, titleBar=True)
        layout = cmds.columnLayout('sqCopyPasteShapesLayout', adjustableColumn=True, parent=win)
        cmds.button('sqCopyPasteShapesBtnSave', label="Save", backgroundColor=(0.8, 0.8, 1.0), command=self.onBtnSavePressed, parent=layout)
        cmds.button('sqCopyPasteShapesBtnLoad', label="Load", backgroundColor=(1.0, 0.8, 0.8), command=self.onBtnLoadPressed, parent=layout)
        cmds.showWindow(win)

    def onBtnSavePressed(self, state):
        path = cmds.fileDialog2(fileMode=0, caption="Save Shapes")
        if not path:
            return
        path = next(iter(path), None)
        # make sure we save the file as mayaAscii
        if not path.endswith(".ma"):
            path = path.replace(".*", ".ma")
        save_all_ctrls_shapes(path)

    def onBtnLoadPressed(self, state):
        path = cmds.fileDialog2(fileMode=1, caption="Load Shapes")
        if not path:
            return
        path = next(iter(path), None)
        load_all_ctrls_shapes(path)

