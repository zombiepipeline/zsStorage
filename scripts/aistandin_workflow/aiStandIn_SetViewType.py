
"""
# AiStandin - Set View type

Instructions:
Select Geo and Choose View Type.

"""


__author__ = "Travis.Harvey"
__version_major__ = "1"
__version_minor__ = "4"
__version__ = "{}.{}".format(__version_major__, __version_minor__)

import maya.cmds as cmds


def set_view(view):
    selected = cmds.ls(sl=1, l=1)
    for x in range(len(selected)):
        cmds.setAttr(selected[x] + ".mode", view)


def run_ui():
    def determine_view(*arg):
        view_button = cmds.radioCollection(setViewCollection, query=1, sl=1)
        view_list = cmds.radioCollection(setViewCollection, query=1, collectionItemArray=1)

        for x in range(7):
            view_list[x] = view_list[x].split("|")[-1]
            if view_button == view_list[x]:
                view = x
                set_view(view)

    setViewWindow = "setViewWindow"
    if cmds.window(setViewWindow, exists=1):
        cmds.deleteUI(setViewWindow)

    setView = cmds.window(
        setViewWindow,
        title="Set aiStandin View Type",
        widthHeight=(300, 150),
        bgc=[0.15, 0.15, 0.15],
        maximizeButton=0,
    )

    columnLayout = cmds.columnLayout('columnLayout',
                                     adjustableColumn=True,
                                     columnOffset=['both', 20],
                                     rowSpacing=3,
                                     parent=setViewWindow)

    setViewCollection = cmds.radioCollection()

    background_color = [0.2, 0.2, 0.2]
    highlight_colour = [0, 0.5, 1]

    zero = cmds.radioButton(
        label="Bounding Box",
        enableKeyboardFocus=1,
        highlightColor=highlight_colour,
        backgroundColor=background_color,
        collection=setViewCollection,
        onCommand=determine_view,
        parent="columnLayout"
    )
    one = cmds.radioButton(
        label="Per-Object Bounding Box",
        enableKeyboardFocus=1,
        highlightColor=highlight_colour,
        backgroundColor=background_color,
        collection=setViewCollection,
        onCommand=determine_view,
        parent="columnLayout"
    )
    two = cmds.radioButton(
        label="Polywire",
        enableKeyboardFocus=1,
        highlightColor=highlight_colour,
        backgroundColor=background_color,
        collection=setViewCollection,
        onCommand=determine_view,
        parent="columnLayout"
    )
    three = cmds.radioButton(
        label="Wireframe",
        enableKeyboardFocus=1,
        highlightColor=highlight_colour,
        backgroundColor=background_color,
        collection=setViewCollection,
        onCommand=determine_view,
        parent="columnLayout"
    )
    four = cmds.radioButton(
        label="Point Cloud",
        enableKeyboardFocus=1,
        highlightColor=highlight_colour,
        backgroundColor=background_color,
        collection=setViewCollection,
        onCommand=determine_view,
        parent="columnLayout"
    )
    five = cmds.radioButton(
        label="Shaded Polywire",
        enableKeyboardFocus=1,
        highlightColor=highlight_colour,
        backgroundColor=background_color,
        collection=setViewCollection,
        onCommand=determine_view,
        parent="columnLayout"
    )
    six = cmds.radioButton(
        label="Shaded",
        enableKeyboardFocus=1,
        highlightColor=[0, 0.5, 1],
        backgroundColor=background_color,
        collection=setViewCollection,
        onCommand=determine_view,
        parent="columnLayout",
        enable=1
    )

    cmds.button(label="Accept", command='cmds.deleteUI(setViewWindow)', enableKeyboardFocus=1, parent="columnLayout")

    cmds.showWindow(setView)


if __name__ == "__main__":
    run_ui()
