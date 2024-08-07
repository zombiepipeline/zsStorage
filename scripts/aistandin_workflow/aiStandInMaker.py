"""
Arnold Standin - Maker.

Instructions
Use on an asset on the origin in the Scene blocking, modeling or shading phase.
Creates the Origin Mesh version Locally and on the network.
Creates the .ass file Locally and on the network.

To Do:
Make it deselect non geo
Make it cancel if nothing is selected.


Changelog:
v4.0
Updated the set_paths script
No longer contains a duplicate of set_paths()
Better path building with os.path.join()

"""
__author__ = "Travis.Harvey"
__version_major__ = "4"
__version_minor__ = "0"
__version__ = "{}.{}".format(__version_major__, __version_minor__)

import maya.cmds as cmds
import maya.mel as mel
import shutil
import os
from mtoa.core import createOptions


def fetch_config_vars(config_file=None):  # Todo: Move this to a utils file.
    if not config_file:
        workspace = os.path.join(os.getenv('APPDATA'), 'zombieEnv')
        config_file = os.path.join(workspace, "YokaiTools_Setup.txt").replace("\\", "/")

    # Fetch info from file.
    lines = []
    with open(config_file, "r") as setupfile:
        for line in setupfile.readlines():
            lines.append(line)
    return lines


def make_standin():
    if cmds.objExists("defaultArnoldRenderOptions") == 0:
        cmds.warning("Render Settings not initialised. Initialising...")
        createOptions()

    # set_paths()
    import aistandin_workflow.aiStandIn_ArnoldSourcePath
    aistandin_workflow.aiStandIn_ArnoldSourcePath.set_paths()

    workspace = cmds.workspace(q=True, rd=True)

    # Read in Variables
    lines = fetch_config_vars()

    # Network Location
    networkLoc = lines[0].split("=")[1]
    networkLoc = networkLoc.strip()

    pluginDir = lines[1].split("=")[1]
    pluginDir = pluginDir.strip()

    networkOn = lines[2].split("=")[1]
    networkOn = networkOn.strip()

    print "The Network location is: " + networkLoc

    originName = cmds.ls(sl=1)

    # Local Directories
    meshSaveLocation = os.path.join(workspace, "scenes", "OriginMesh").replace("\\", "/")
    standInSaveLocation = os.path.join(workspace, "scenes", "standIn").replace("\\", "/")

    # Force scene save
    cmds.file(force=1, save=1, options="v=0")

    # Check if mesh is selected
    if len(originName) == 0:
        cmds.warning("No Mesh is selected.")

    # Check if the Mesh is not on Origin
    originMeshLocation = (cmds.getAttr(originName[0] + ".translateX"),
                          cmds.getAttr(originName[0] + ".translateY"),
                          cmds.getAttr(originName[0] + ".translateZ"))
    if originMeshLocation != (0.0, 0.0, 0.0):
        response = cmds.confirmDialog(
            title="Error",
            bgc=(1, 0, 0),  # Todo: Set this to a nice Hex color
            message="Mesh not on Origin",
            b="Accept",
            defaultButton="Accept",
            icon="critical")
        if response != "Accept":
            cmds.warning("The process has been canceled by the user as the mesh was not on hte origin")
            return

    # for x in range(len(originName)):
    x = 0
    # Export Mesh to local project
    output_maya_file = os.path.join(meshSaveLocation, originName[x] + ".mb").replace("\\", "/")
    cmds.file(output_maya_file, force=1, options="v=0;", typ="mayaBinary", pr=1, es=1)

    # Export aiStandIn to local project
    cmds.select(originName[x])
    # aiStandinExportCommand = ("file -force -options \"-shadowLinks 0;-mask 25;-lightLinks 0;-boundingBox;-fullPath\" -typ \"ASS Export\" -pr -es \"" + (standInSaveLocation + "/" + originName[x] + ".ass\"") + ";")
    standin_filepath = os.path.join(standInSaveLocation, originName[x] + ".ass").replace("\\", "/")
    aiStandinExportCommand = "file -force -options \"-shadowLinks 0;-mask 25;-lightLinks 0;-boundingBox;-fullPath\" -typ \"ASS Export\" -pr -es \"{}\";".format(standin_filepath)

    mel.eval(aiStandinExportCommand)

    # Network Section
    if networkOn == "1":
        # Network Directories
        networkOriginMesh = os.path.join(networkLoc, "scenes", "New_OriginMesh").replace("\\", "/")
        networkStandIn_dir = os.path.join(networkLoc, "scenes", "New_standIn").replace("\\", "/")

        # Check if the network location is available.
        if os.path.exists(networkLoc):
            # Export Mesh to Network
            network_mb_path = os.path.join(networkOriginMesh, originName[x] + ".mb").replace("\\", "/")
            cmds.file(network_mb_path, force=1, options="v=0;", typ="mayaBinary", pr=1, es=1)
            # Copy aiStandIn to Network
            standin_filepath = os.path.join(standInSaveLocation, originName[x] + ".ass").replace("\\", "/")
            shutil.copy(standin_filepath, networkStandIn_dir)
        else:
            # Summon Error Message
            cmds.confirmDialog(
                title="Network Access Error",
                bgc=(1, 0, 0),  # Todo: Set this to a nice Hex color
                message="The network location is unavailable.",
                b="Accept",
                defaultButton="Accept",
                icon="critical")

            # Export Mesh to Interim Network Folder
            interim_network_OriginMesh = os.path.join(workspace, "scenes", "interim_OriginMesh", originName[x] + ".mb").replace("\\", "/")
            cmds.file(interim_network_OriginMesh, force=1, options="v=0;", typ="mayaBinary", pr=1, es=1)
            # Copy aiStandIn to Interim Network Folder
            # Copy aiStandIn to Network
            standin_filepath = os.path.join(standInSaveLocation, originName[x] + ".ass").replace("\\", "/")
            interim_network_standin_dir = os.path.join(workspace, "scenes", "interim_standIn").replace("\\", "/")
            shutil.copy(standin_filepath, interim_network_standin_dir)

    def testStandin(originName, standInSaveLocation):
        # Create test aiStandIn
        cmds.createNode("aiStandIn", n=(originName[x] + "_shape"))
        cmds.rename("transform1", (originName[x] + "_standIn"))

        # Set the aiStandIn's import path
        interim_standin_path = os.path.join(standInSaveLocation, originName[x] + ".ass").replace("\\", "/")
        cmds.setAttr((originName[x] + '_shape.dso'), interim_standin_path, type='string')

        # Set the aiStandIn to shaded
        cmds.setAttr((originName[x] + "_shape.mode"), 6)

        # Set Original GEO Colour
        cmds.setAttr(originName[x] + ".useOutlinerColor", True)
        cmds.setAttr(originName[x] + ".outlinerColor", 0.15, 0.8, 0.9)

    # testStandin(originName, standInSaveLocation)

    cmds.confirmDialog(
        b="Confirm",
        icon="information",
        message="Standin Creation was Successful",
        title="Create aiStandin")


if __name__ == "__main__":
    make_standin()
