"""
Arnold Standin - replace with OriginGeo

Instructions:
Select all standin's to be replaced with geo and run the script.
Ensure that all of your origin mesh is placed in such a position such that it's rotation point is the origin.

"""

__author__ = "Travis.Harvey"
__version_major__ = "2"
__version_minor__ = "8"
__version__ = "{}.{}".format(__version_major__, __version_minor__)


def replace_geo():
    import os
    import maya.cmds as cmds
    import maya.mel as mel

    workspace = cmds.workspace(q=True, rd=True)
    meshSaveLocation = os.path.join(workspace, "scenes", "OriginMesh").replace("\\", "/")

    sources = cmds.ls(sl=1, l=1)

    for source in sources:
        # Get Name from .ass path
        selectedShape = cmds.listRelatives(source, s=1)
        assPath = cmds.getAttr(selectedShape[0] + ".dso")
        filename_ass = os.path.basename(assPath)

        # Translate into OriginMesh Path
        filename_mb = filename_ass.replace(".ass", ".mb")

        # location of the OriginMesh to import
        meshFilePath = os.path.join(meshSaveLocation, filename_mb).replace("\\", "/")
        if not os.path.isfile(meshFilePath):
            cmds.warning("Could not find an Origin Mesh for {}".format(assPath))
            continue

        # Import Mesh
        importedList = cmds.file(meshFilePath, f=1, op="v=0;", typ='mayaBinary', namespace="GeoReplace", mergeNamespacesOnClash=1, i=1, rnn=1)
        imported = cmds.ls(importedList, type="transform")
        importedLongName = cmds.ls(imported[0], l=1)

        # Set imported objects rotation pivot to 0 0 0
        mel.eval('xform -ws -a -rp 0 0 0 -sp 0 0 0 {};'.format(importedLongName[0]))
        # Match Geo Transforms to aiStandin
        print("Matching Geo...")
        # cmds.matchTransform(importedLongName, source, pos=1, rot=1, scl=1)

        s_x_trans = cmds.getAttr(source + ".tx")
        s_y_trans = cmds.getAttr(source + ".ty")
        s_z_trans = cmds.getAttr(source + ".tz")

        s_x_rot = cmds.getAttr(source + ".rx")
        s_y_rot = cmds.getAttr(source + ".ry")
        s_z_rot = cmds.getAttr(source + ".rz")

        s_x_scale = cmds.getAttr(source + ".sx")
        s_y_scale = cmds.getAttr(source + ".sy")
        s_z_scale = cmds.getAttr(source + ".sz")

        cmds.xform(importedLongName, relative=False,
                   translation=[s_x_trans, s_y_trans, s_z_trans],
                   rotation=[s_x_rot, s_y_rot, s_z_rot],
                   scale=[s_x_scale, s_y_scale, s_z_scale]
                   )

        # Parent StandIn beside GEO
        geo_parent = cmds.listRelatives(source, p=1)
        if geo_parent:
            cmds.parent(importedLongName, geo_parent)

        print("Deleting Source...")
        cmds.delete(source)
        print("Deleted {}".format(source))


if __name__ == "__main__":
    replace_geo()
