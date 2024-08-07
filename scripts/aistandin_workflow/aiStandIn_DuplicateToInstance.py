"""
# Arnold Standin - Transform Duplicate into instance

Duplicates all selected objects as instances of the 1st selected object.
Works on:
1. aiStandins
2. Geometry


# Instructions:
# Select Source first
# Select all the Duplicates to be replaced Second.
# Run the script.
"""

__author__ = "Travis.Harvey"
__version_major__ = "2"
__version_minor__ = "3"
__version__ = "{}.{}".format(__version_major__, __version_minor__)

import maya.cmds as cmds


def from_duplicate_to_instance(auto_delete=True):
    """
    :param auto_delete: Automatically delete the replaced shape
    """
    selection = cmds.ls(sl=1, l=1)
    source_item = selection.pop(0)

    source_shape = cmds.listRelatives(source_item, f=1)
    # Set Host Colour
    cmds.setAttr(source_item + ".useOutlinerColor", True)
    cmds.setAttr(source_item + ".outlinerColor", 0.8, 1, 0)

    for target in selection:
        gen_name = source_item.split("|")[-1] + "_instance"
        # Create instance
        instance = cmds.instance(source_shape, n=gen_name)[0]

        # Set instance Colour
        cmds.setAttr(instance + ".useOutlinerColor", True)
        cmds.setAttr(instance + ".outlinerColor", 0, 0.8, 0)

        s_x_trans = cmds.getAttr(target + ".tx")
        s_y_trans = cmds.getAttr(target + ".ty")
        s_z_trans = cmds.getAttr(target + ".tz")

        s_x_rot = cmds.getAttr(target + ".rx")
        s_y_rot = cmds.getAttr(target + ".ry")
        s_z_rot = cmds.getAttr(target + ".rz")

        s_x_scale = cmds.getAttr(target + ".sx")
        s_y_scale = cmds.getAttr(target + ".sy")
        s_z_scale = cmds.getAttr(target + ".sz")

        cmds.xform(instance, relative=False,
                   translation=[s_x_trans, s_y_trans, s_z_trans],
                   rotation=[s_x_rot, s_y_rot, s_z_rot],
                   scale=[s_x_scale, s_y_scale, s_z_scale]
                   )

        # Re-parent
        parent = cmds.listRelatives(target, p=1)
        if parent is not None:  # If not parented to world
            if parent != cmds.listRelatives(instance, p=1):
                cmds.parent(instance, cmds.listRelatives(target, p=1, f=1))

        if auto_delete:  # Auto Delete the replaced shape
            cmds.delete(target)
        else:            # Append '_DELETE' to the replaced shape
            renamed = cmds.rename(target.split("|")[-1], target.split("|")[-1] + "_DELETE")
            cmds.setAttr(renamed + ".useOutlinerColor", True)
            cmds.setAttr(renamed + ".outlinerColor", 1, 0, 0)


if __name__ == "__main__":
    from_duplicate_to_instance()
