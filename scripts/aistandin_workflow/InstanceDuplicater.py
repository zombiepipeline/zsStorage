"""
INSTRUCTIONS:
Select an object and run the script to create an instance of that object with matching transformations.

Duplicates the selected mesh as an instance.
Works on:
1. aiStandins
2. Polygon Geometry
3. Nurbs
4. Other Instances
5. Anything with a transform node
"""

__author__ = "Travis.Harvey"
__version_major__ = "2"
__version_minor__ = "1"
__version__ = "{}.{}".format(__version_major__, __version_minor__)


def duplicate_as_instance(match_transforms=False):
    import maya.cmds as cmds

    selection = cmds.ls(sl=1, l=1)

    for source_transform in selection:
        selected_shape_dir = cmds.listRelatives(source_transform, f=1)
        if selected_shape_dir:
            selected_shape_dir = selected_shape_dir[0]

        name = source_transform.split("|")[-1]
        if "_Instance" not in name:
            name += "_Instance1"

        # Create Instance
        instance_transform = cmds.instance(selected_shape_dir, n=name)[0]

        if "_Instance" not in source_transform:
            # Set Host Colour
            cmds.setAttr(source_transform + ".useOutlinerColor", True)
            cmds.setAttr(source_transform + ".outlinerColor", 0.8, 1, 0)

        # Match transforms to the instance Target
        if match_transforms:
            s_x_trans = cmds.getAttr(source_transform + ".tx")
            s_y_trans = cmds.getAttr(source_transform + ".ty")
            s_z_trans = cmds.getAttr(source_transform + ".tz")

            s_x_rot = cmds.getAttr(source_transform + ".rx")
            s_y_rot = cmds.getAttr(source_transform + ".ry")
            s_z_rot = cmds.getAttr(source_transform + ".rz")

            s_x_scale = cmds.getAttr(source_transform + ".sx")
            s_y_scale = cmds.getAttr(source_transform + ".sy")
            s_z_scale = cmds.getAttr(source_transform + ".sz")

            cmds.xform(instance_transform, relative=False,
                       translation=[s_x_trans, s_y_trans, s_z_trans],
                       rotation=[s_x_rot, s_y_rot, s_z_rot],
                       scale=[s_x_scale, s_y_scale, s_z_scale]
                       )

        # Set Instance Colour
        cmds.setAttr(instance_transform + ".useOutlinerColor", True)
        cmds.setAttr(instance_transform + ".outlinerColor", 0, 0.8, 0)

        cmds.select(instance_transform)


if __name__ == "__main__":
    duplicate_as_instance(match_transforms=True)
