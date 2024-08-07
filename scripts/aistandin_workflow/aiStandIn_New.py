"""
AiStandin New.

Instructions:
Use in a scene to import a .ass file from your library.
Creates a standin and assigns a ".ass" from "{Project Directory}/scenes/aiStandIn"

"""

__author__ = "Travis.Harvey"
__version_major__ = "1"
__version_minor__ = "8"
__version__ = "{}.{}".format(__version_major__, __version_minor__)

import os
import maya.cmds as cmds


def new_ai_standIn(display_mode=6):
    """
    :param display_mode: {0: Bounding Box,
                          1: Per Object Bounding Box
                          2: Polywire,
                          3: Wireframe,
                          4: Point Cloud,
                          5: Shaded Polywire,
                          6: Shaded}
    """

    workspace = cmds.workspace(q=True, rd=True)
    meshSaveLocation = os.path.join(workspace + "scenes", "OriginMesh").replace("\\", "/")
    standInSaveLocation = os.path.join(workspace + "scenes", "standIn").replace("\\", "/")

    filedir = cmds.fileDialog2(
            ds=2,
            cap="Select the relevant .ass file",
            dir=standInSaveLocation,
            ff="*.ass",
            fm=1,
            okc="Accept")

    if not filedir:
        return

    standin_path = filedir[0]
    standin_filename = os.path.basename(standin_path)
    standin_shape = standin_filename.replace(".ass", "_shape")

    if not cmds.objExists(standin_shape):
        # Create aiStandIn
        newStandinShape = cmds.createNode("aiStandIn", n="newAiStandIn_shape")
        newStandin = cmds.listRelatives(newStandinShape, p=1)
        name = cmds.rename(newStandin, standin_filename.replace(".ass", "_standIn"))

        # Set the aiStandIn's import path
        cmds.setAttr(name + '.dso', standin_path, type='string')

        # Set the aiStandIn to shaded
        cmds.setAttr(newStandinShape + ".mode", display_mode)

        # Rename standIn_shape
        cmds.rename(newStandinShape, standin_shape)

    else:
        cmds.warning("The chosen standIn is already present in your scene. It will be instanced instead.")
        cmds.select(standin_filename.replace(".ass", "_standIn"))
        import aistandin_workflow.InstanceDuplicater
        aistandin_workflow.InstanceDuplicater.duplicate_as_instance(match_transforms=False)


if __name__ == "__main__":
    new_ai_standIn()
