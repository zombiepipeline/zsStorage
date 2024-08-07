"""
aiStandIn - Set Arnold Source Paths.
"""

__author__ = "Travis.Harvey"
__version_major__ = "1"
__version_minor__ = "6"
__version__ = "{}.{}".format(__version_major__, __version_minor__)

import os
import maya.cmds as cmds


def fetch_config_vars(config_file=None):
    if not config_file:
        workspace = cmds.workspace(q=True, rd=True)
        setupLoc = os.path.join(workspace, "scripts")
        config_file = os.path.join(setupLoc, "YokaiTools_Setup.txt").replace("\\", "/")

    # Fetch info from file.
    lines = []
    with open(config_file, "r") as setupfile:
        for line in setupfile.readlines():
            lines.append(line)
    return lines


def set_paths():
    # Version 1.6
    from mtoa.core import createOptions
    if cmds.objExists("defaultArnoldRenderOptions") == 0:
        cmds.warning("Render Settings not initialised. Initialising...")
        createOptions()

    workspace = cmds.workspace(q=True, rd=True)
    standInSaveLocation = os.path.join(workspace, "scenes", "standIn")
    sourceimages = os.path.join(workspace, "sourceimages")

    setupLoc = os.path.join(workspace, "scripts")
    config_file = os.path.join(setupLoc, "YokaiTools_Setup.txt")

    if not os.path.isfile(config_file):
        cmds.warning('No Config file found: "{}"'.format(config_file))
        return

    # Fetch info from file.
    lines = fetch_config_vars(config_file)

    # Read Variables
    networkLoc = lines[0].split("=")[1]
    pluginDir = lines[1].split("=")[1]

    # Set paths to be relative
    cmds.setAttr("defaultArnoldRenderOptions.absoluteTexturePaths", 0)
    cmds.setAttr("defaultArnoldRenderOptions.absoluteProceduralPaths", 0)

    cmds.setAttr("defaultArnoldRenderOptions.exportFullPaths", 1)

    # Proceedural Search Path: Your .ass file save location.
    cmds.setAttr("defaultArnoldRenderOptions.procedural_searchpath", standInSaveLocation, type="string")

    # Plugin Search Path: Search for .ass files made in other programs.
    cmds.setAttr("defaultArnoldRenderOptions.plugin_searchpath", pluginDir, type="string")

    # Texture Search Path: Search for referenced textures.
    cmds.setAttr("defaultArnoldRenderOptions.texture_searchpath", sourceimages, type="string")


if __name__ == "__main__":
    set_paths()
