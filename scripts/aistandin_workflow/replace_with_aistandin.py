"""
Convert Placed object to a chosen aiStandin.

# Instructions:
# Select an object or objects
# Run the script.
# Select the "ass" file from the list that you want to replace the selection with.
"""

__author__ = "Travis.Harvey"
__version_major__ = "3"
__version_minor__ = "5"
__version__ = "{}.{}".format(__version_major__, __version_minor__)


def run_replace(delete_source=True, view_mode=6):
    """
    :param view_mode:
    :param delete_source: Set to True to Delete the mesh that was selected after the replacement is in place.
    :return:
    """

    import os
    import maya.cmds as cmds
    import maya.mel as mel
    import aistandin_workflow.InstanceDuplicater

    selected = cmds.ls(sl=1, l=1)

    workspace = cmds.workspace(q=True, rd=True)
    standin_save_location = os.path.join(workspace, "scenes", "standIn").replace("\\", "/")

    # Center Pivot of
    mel.eval("CenterPivot;")

    filedir = cmds.fileDialog2(
        ds=2,
        cap="Select the relevant .ass file",
        dir=standin_save_location,
        ff="*.ass",
        fm=1,
        okc="Accept"
    )

    for clean_name in selected:

        # Split the directory and take the last piece.
        ass_filepath = filedir[0]
        ass_filename = os.path.basename(ass_filepath)
        duplicate_name = ass_filename.replace(".ass", "_standIn")

        if not cmds.objExists(duplicate_name):
            # Create aiStandIn
            standin_name = cmds.createNode("aiStandIn", n=clean_name + "_shape")
            standin_name = cmds.ls(sl=1)
            standin_transform = cmds.rename(cmds.listRelatives(standin_name, p=1), (clean_name + "_standIn"))

            temp = cmds.listRelatives(standin_transform, s=1, f=1)
            standin_name = temp[0]
            print("standin_name is: {}".format(standin_name))

            # Create Locator and match transforms to GEO
            locator = cmds.spaceLocator(p=(0, 0, 0), n=clean_name + "_Loc")[0]
            cmds.matchTransform(locator, clean_name, piv=1, pos=1, rot=1, scl=1)

            # Set the aiStandIn's import path
            cmds.select(standin_name)
            cmds.setAttr(standin_name + '.dso', ass_filepath, type='string')

            # Center Pivot of aiStandIn
            cmds.select(standin_name)
            mel.eval("CenterPivot;")

            # Match aiStandIn Transforms to Locator
            cmds.matchTransform(standin_name, locator, pos=1, rot=1, scl=1)

            # Set Shaded View
            cmds.setAttr(standin_name + ".mode", view_mode)

            # Delete the Locator
            cmds.delete(locator)

            # Rename standIn based on .ass file
            dso = cmds.getAttr(standin_name + ".dso")
            new_name = os.path.basename(dso).replace(".ass", "_standIn")
            final_name = cmds.rename(standin_transform, new_name)

            # Parent StandIn beside GEO
            geo_parent = cmds.listRelatives(clean_name, p=1)
            if geo_parent:
                cmds.parent(final_name, geo_parent)

        else:
            cmds.warning("The chosen standIn is already present in your scene.")
            cmds.select(duplicate_name)
            aistandin_workflow.InstanceDuplicater.duplicate_as_instance(match_transforms=False)
            cmds.select(clean_name, add=1)
            selectedList = cmds.ls(sl=1, l=1)
            cmds.matchTransform(selectedList[0], selectedList[1], piv=1, pos=1, rot=1, scl=1)

        if delete_source:
            cmds.delete(clean_name)
        else:
            # Set Outliner Colour
            cmds.setAttr(clean_name + ".useOutlinerColor", True)
            cmds.setAttr(clean_name + ".outlinerColor", 1, 0, 0)
            # Append 'Delete' to the old GEO
            cmds.rename(clean_name, clean_name.split("|")[-1] + "_DELETE")

    # Refresh outliner colour
    mel.eval('AEdagNodeCommonRefreshOutliners();')


if __name__ == "__main__":
    run_replace()
