##--------------------------------------------------------------------------
##
## ScriptName : AssetIt
## Author     : Wizix
## URL        :
## LastUpdate : 2022/07/08
##
## Version    : 0.3.0
#
###
##--------------------------------------------------------------------------


from PySide2 import QtWidgets, QtCore, QtGui
from maya import cmds as mc
import maya.mel as mel
import json
from .Qt import QtWidgets, QtCore, QtCompat
import os
import maya.cmds as cmds
from maya import OpenMayaUI as omui
import mtoa.core as core
from functools import partial

# Special cases for different Maya versions
from shiboken2 import wrapInstance
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget

from . import AssetIt_Global
import importlib
importlib.reload(AssetIt_Global)

from . import AssetIt_CSS
importlib.reload(AssetIt_CSS)

from . import AssetIt_Widgets
import importlib
importlib.reload(AssetIt_Widgets)

from . import AssetIt_Setting
importlib.reload(AssetIt_Setting)

from . import AssetIt_AddAsset
importlib.reload(AssetIt_AddAsset)

from . import AssetIt_NewTab
importlib.reload(AssetIt_NewTab)

from . import AssetIt_NewSecondTab
importlib.reload(AssetIt_NewSecondTab)

##______________________GLOBAL VAR

##PATH_SET
IconPath = AssetIt_Global.IconsPathThemeClassic
PreferencePath = AssetIt_Global.PreferencePath
ToolsPath = AssetIt_Global.ToolPath

##FIRST LAUNCH
FirstLaunchpref_path=open(PreferencePath + 'FirstLaunch.json',"r")
FirstLaunchdata_pref = json.load(FirstLaunchpref_path)
FirstLaunchPath=(FirstLaunchdata_pref['FIRST_LAUNCH'])
FIRSTLAUNCH = FirstLaunchPath

##TAB OPEN
TabOpenpref_path=open(PreferencePath + 'TabOpen.json',"r")
TabOpendata_pref = json.load(TabOpenpref_path)
TabOpenPath=(TabOpendata_pref['TAB_OPEN'])
TAB_OPEN = TabOpenPath

TabOpenSecondpref_path=open(PreferencePath + 'TabOpenSecond.json',"r")
TabOpenSeconddata_pref = json.load(TabOpenSecondpref_path)
TabOpenSecondPath=(TabOpenSeconddata_pref['TAB_OPEN'])
TAB_OPEN_SECOND = TabOpenSecondPath


ASSET_LIBRARY_PATH = AssetIt_Global.ASSET_LIBRARY_PATH
ASSET_FAVOURITES_PATH = AssetIt_Global.ASSET_FAVOURITES_PATH

ACTIVESUBTAB = 0
ACTIVESUBTAB_NAME = ""



##______________________BUILD UI
class AssetIt_UI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AssetIt_UI, self).__init__()
        self.allListWidets = [] #contains all the list widgets to process actions to all of them

        self.setMinimumSize(450, 400)
        #self.setGeometry(100, 300, 600, 500)
        self.buildUI()

        self.firstTab.setCurrentIndex(TAB_OPEN)
        self.secondTab.setCurrentIndex(TAB_OPEN_SECOND)


    def buildUI(self):
        "ajoute tous les widgets a la fenêtre principale"
        ##__________________________________________________________________________________UI - Import CSS
        self.setStyleSheet(AssetIt_Global.Theme)

        # ******************************************
        #           BUTTON BARS
        # ******************************************
        iconButtonSize = AssetIt_Global.IconButtonSize

        ###________________________________________________________________________________>>> TOOLBAR
        separatorWidth = 2

        ## TOOLBAR LAYOUT
        self.ToolBarLyt = QtWidgets.QHBoxLayout()
        #self.ToolBarLyt.addWidget(Color('red'))
        #self.ToolBarLyt.addSpacing(15)


        ## BTN SETTING
        self.SettingBTN = QtWidgets.QPushButton()
        self.SettingBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.SettingBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.SettingBTN.setIcon(QtGui.QIcon(IconPath + "BatchProcess.png"))
        self.SettingBTN.clicked.connect(self.Setting_Window)
        self.SettingBTN.setToolTip("  Setting Window  ")
        self.ToolBarLyt.addWidget(self.SettingBTN)




        ## SEPARATOR
        self.Separator = QtWidgets.QPushButton()
        self.Separator.setFixedSize(separatorWidth,iconButtonSize)
        self.Separator.setObjectName("Separator")
        self.Separator.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.Separator.setIcon(QtGui.QIcon(IconPath + "SeparatorBtn.png"))
        self.Separator.setEnabled(0)
        self.ToolBarLyt.addWidget(self.Separator)

        ## BTN LIBRARY FOLDER
        self.LibFolderBTN = QtWidgets.QPushButton()
        self.LibFolderBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.LibFolderBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.LibFolderBTN.setIcon(QtGui.QIcon(IconPath + "Folder2.png"))
        self.LibFolderBTN.clicked.connect(self.OpenLibFolder)
        self.LibFolderBTN.setToolTip("  Open Library Folder  ")
        self.ToolBarLyt.addWidget(self.LibFolderBTN)

        ## BTN REFRESH
        self.RefreshBTN = QtWidgets.QPushButton()
        self.RefreshBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.RefreshBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.RefreshBTN.setIcon(QtGui.QIcon(IconPath + "Reload.png"))
        self.RefreshBTN.clicked.connect(self.Refresh)
        self.RefreshBTN.setToolTip("  Refresh UI  ")
        self.ToolBarLyt.addWidget(self.RefreshBTN)

        ## SEPARATOR
        self.Separator = QtWidgets.QPushButton()
        self.Separator.setFixedSize(separatorWidth,iconButtonSize)
        self.Separator.setObjectName("Separator")
        self.Separator.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.Separator.setIcon(QtGui.QIcon(IconPath + "SeparatorBtn.png"))
        self.Separator.setEnabled(0)
        self.ToolBarLyt.addWidget(self.Separator)



        ## BTN SELECT GROUP
        activeSelMode = mc.selectMode(q=True, root=True)
        self.SelGroupBTN = QtWidgets.QPushButton()
        self.SelGroupBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.SelGroupBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        if activeSelMode == True:
            self.SelGroupBTN.setIcon(QtGui.QIcon(IconPath + "Sel_Group.png"))
        else:
            self.SelGroupBTN.setIcon(QtGui.QIcon(IconPath + "Sel_Group_OFF.png"))
        self.SelGroupBTN.clicked.connect(self.SelGroup)
        self.SelGroupBTN.setToolTip("  Direct Group Selection  ")
        self.ToolBarLyt.addWidget(self.SelGroupBTN)




        ## SEPARATOR
        self.Separator = QtWidgets.QPushButton()
        self.Separator.setFixedSize(separatorWidth,iconButtonSize)
        self.Separator.setObjectName("Separator")
        self.Separator.setIconSize(QtCore.QSize(26, iconButtonSize))
        self.Separator.setIcon(QtGui.QIcon(IconPath + "SeparatorBtn.png"))
        self.Separator.setEnabled(0)
        self.ToolBarLyt.addWidget(self.Separator)


        ## BTN PIVOT ORIGIN GRID
        self.PivotOriginGridBTN = QtWidgets.QPushButton()
        self.PivotOriginGridBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.PivotOriginGridBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.PivotOriginGridBTN.setIcon(QtGui.QIcon(IconPath + "AlignGridBase.png"))
        self.PivotOriginGridBTN.clicked.connect(self.PivotGrid)
        self.PivotOriginGridBTN.setToolTip("  Pivot at Bottom and Grid Origin  ")
        self.ToolBarLyt.addWidget(self.PivotOriginGridBTN)

        ## BTN PIVOT BASE GRID
        self.GridCenterBTN = QtWidgets.QPushButton()
        self.GridCenterBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.GridCenterBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.GridCenterBTN.setIcon(QtGui.QIcon(IconPath + "AlignGrid.png"))
        self.GridCenterBTN.clicked.connect(self.GridCenter)
        self.GridCenterBTN.setToolTip("  Object at Grid Center  ")
        self.ToolBarLyt.addWidget(self.GridCenterBTN)

        ## BTN PIVOT BOTTOM
        self.PivotBottomBTN = QtWidgets.QPushButton()
        self.PivotBottomBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.PivotBottomBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.PivotBottomBTN.setIcon(QtGui.QIcon(IconPath + "AlignPivotBase.png"))
        self.PivotBottomBTN.clicked.connect(self.PivotBottom)
        self.PivotBottomBTN.setToolTip("  Pivot at Object Bottom  ")
        self.ToolBarLyt.addWidget(self.PivotBottomBTN)

        ## SEPARATOR
        self.Separator = QtWidgets.QPushButton()
        self.Separator.setFixedSize(separatorWidth,iconButtonSize)
        self.Separator.setObjectName("Separator")
        self.Separator.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.Separator.setIcon(QtGui.QIcon(IconPath + "SeparatorBtn.png"))
        self.Separator.setEnabled(0)
        self.ToolBarLyt.addWidget(self.Separator)

        PlacementMode_pref = json.load(open(PreferencePath + 'PlacementMode.json', "r"))
        PLACEMENTMODE = (PlacementMode_pref['PLACEMENT_MODE'])

        ## BTN PLACEMENT ORIGIN
        self.PlacementOriginGridBTN = QtWidgets.QPushButton()
        self.PlacementOriginGridBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.PlacementOriginGridBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        if PLACEMENTMODE == 0:
            self.PlacementOriginGridBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Orign.png"))
        else:
            self.PlacementOriginGridBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Orign_OFF.png"))
        self.PlacementOriginGridBTN.clicked.connect(self.PlacementOrigin)
        self.PlacementOriginGridBTN.setToolTip("  Import Asset at Grid Origin  ")
        self.ToolBarLyt.addWidget(self.PlacementOriginGridBTN)



        ## BTN PLACEMENT REPLACE
        self.PlacementReplaceBTN = QtWidgets.QPushButton()
        self.PlacementReplaceBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.PlacementReplaceBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        if PLACEMENTMODE == 4:
            self.PlacementReplaceBTN.setIcon(QtGui.QIcon(IconPath + "Replace.png"))
        else:
            self.PlacementReplaceBTN.setIcon(QtGui.QIcon(IconPath + "Replace_OFF.png"))
        self.PlacementReplaceBTN.clicked.connect(self.PlacementReplace)
        self.PlacementReplaceBTN.setToolTip("  Replace Selection  ")
        self.ToolBarLyt.addWidget(self.PlacementReplaceBTN)







        ## BTN PLACEMENT SELECTION
        self.PlacementSelectionBTN = QtWidgets.QPushButton()
        self.PlacementSelectionBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.PlacementSelectionBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        if PLACEMENTMODE == 1:
            self.PlacementSelectionBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Selection.png"))
        else:
            self.PlacementSelectionBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Selection_OFF.png"))
        self.PlacementSelectionBTN.clicked.connect(self.PlacementSelection)
        self.PlacementSelectionBTN.setToolTip("  Import Asset at selection average point  ")
        self.ToolBarLyt.addWidget(self.PlacementSelectionBTN)


        ## BTN PLACEMENT TOP OF
        self.PlacementTopOfBTN = QtWidgets.QPushButton()
        self.PlacementTopOfBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.PlacementTopOfBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        if PLACEMENTMODE == 2:
            self.PlacementTopOfBTN.setIcon(QtGui.QIcon(IconPath + "PlaceOnTopOf.png"))
        else:
            self.PlacementTopOfBTN.setIcon(QtGui.QIcon(IconPath + "PlaceOnTopOf_OFF.png"))
        self.PlacementTopOfBTN.clicked.connect(self.PlacementTopOf)
        self.PlacementTopOfBTN.setToolTip("  Import Asset and place it on top of the selection  ")
        self.ToolBarLyt.addWidget(self.PlacementTopOfBTN)



        ## BTN PLACEMENT DRAG
        self.PlacementDragBTN = QtWidgets.QPushButton()
        self.PlacementDragBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.PlacementDragBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        if PLACEMENTMODE == 3:
            self.PlacementDragBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Drag.png"))
        else:
            self.PlacementDragBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Drag_OFF.png"))



        self.PlacementDragBTN.clicked.connect(self.PlacementDrag)
        self.PlacementDragBTN.setToolTip("  Interactive drag and move Asset on scene geometries  ")
        self.ToolBarLyt.addWidget(self.PlacementDragBTN)






        ## SEPARATOR
        self.Separator = QtWidgets.QPushButton()
        self.Separator.setFixedSize(separatorWidth,iconButtonSize)
        self.Separator.setObjectName("Separator")
        self.Separator.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.Separator.setIcon(QtGui.QIcon(IconPath + "SeparatorBtn.png"))
        self.Separator.setEnabled(0)
        self.ToolBarLyt.addWidget(self.Separator)




        ## IMPORT MULTI FILES
        self.ImportFromFilesBTN = QtWidgets.QPushButton()
        self.ImportFromFilesBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.ImportFromFilesBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.ImportFromFilesBTN.setIcon(QtGui.QIcon(IconPath + "MultiFile.png"))
        self.ImportFromFilesBTN.clicked.connect(self.BatchProcess)
        self.ImportFromFilesBTN.setToolTip("  Add Multiple Asset from external files  ")
        self.ToolBarLyt.addWidget(self.ImportFromFilesBTN)


        ## CREATE MULTI FROM SCENE
        self.CreateAssetsfromSceneBTN = QtWidgets.QPushButton()
        self.CreateAssetsfromSceneBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.CreateAssetsfromSceneBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.CreateAssetsfromSceneBTN.setIcon(QtGui.QIcon(IconPath + "AddMultipleAsset.png"))
        self.CreateAssetsfromSceneBTN.clicked.connect(self.CreateMultiFromScene)
        self.CreateAssetsfromSceneBTN.setToolTip("  Create Multiple Asset from Scene  ")
        self.ToolBarLyt.addWidget(self.CreateAssetsfromSceneBTN)







        ## BTN ADD ASSET
        self.AddAssetBTN = QtWidgets.QPushButton()
        self.AddAssetBTN.setFixedSize(iconButtonSize,iconButtonSize)
        self.AddAssetBTN.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.AddAssetBTN.setIcon(QtGui.QIcon(IconPath + "AddAsset2.png"))
        self.AddAssetBTN.setToolTip("  Add Asset  ")
        self.AddAssetBTN.clicked.connect(self.Add_Asset)
        self.ToolBarLyt.addWidget(self.AddAssetBTN, alignment=QtCore.Qt.AlignRight)




        """                     TAB CLICK MENU                      """
        # ******************************************
        #           TAB CLICK MENU
        # ******************************************
        self.tabMenu = QtWidgets.QMenu()
        self.closeAction = QtWidgets.QAction(QtGui.QIcon("AssetIt_IconShelf.png"), "Close Tab", self)
        self.tabMenu.addAction(self.closeAction)
        """                     COSIUS OUT                       """



        #******************************************
        #           TABS
        # ******************************************


        self.firstTab = QtWidgets.QTabWidget(self)
        #construct files tabs
        # liste tous les dossiers contenus dans le dossier Assets_library
        try:
            self.firstLevelFolderList = os.listdir(ASSET_LIBRARY_PATH)
        except:
            os.mkdir(str(ASSET_LIBRARY_PATH))
            os.mkdir(str(ASSET_LIBRARY_PATH) + "/MAINTAB")
            os.mkdir(str(ASSET_LIBRARY_PATH) + "/MAINTAB" + "/SecondTab")
            self.firstLevelFolderList = os.listdir(ASSET_LIBRARY_PATH)
            AssetIt_Global.WarningWindow("The Script lost link to your Asset Library folder. A default new one is create.", 500)


        #EMPTY FOLDER CHOOSEN
        if self.firstLevelFolderList == [] :
            os.mkdir(str(ASSET_LIBRARY_PATH) + "/MAINTAB")
            os.mkdir(str(ASSET_LIBRARY_PATH) + "/MAINTAB" + "/SecondTab")
            from . import AssetIt_UI
            import importlib
            importlib.reload(AssetIt_UI)
            AssetIt_UI.showUI()

        # first level tabs
        for i in self.firstLevelFolderList:
            firstTab_path = ASSET_LIBRARY_PATH + "/" + i
            try:  # check si le dossier du FirstLevel contient des dossiers
                self.secondLevelFolderList = os.listdir(firstTab_path)  # s'il ne contient pas de dossiers cette ligne va faire crash le try et le code va passer dirrect au except
                self.secondTab = QtWidgets.QTabWidget(self)

                print (str(self.secondLevelFolderList))
                if self.secondLevelFolderList == []:
                    print ("SECOND EMPTY")
                    print (str(firstTab_path) + "/SecondTab")
                    os.mkdir(str(firstTab_path) + "/SecondTab")
                    from . import AssetIt_UI
                    import importlib
                    importlib.reload(AssetIt_UI)
                    AssetIt_UI.showUI()


                # second level tabs
                for j in self.secondLevelFolderList:
                    secondTab_path = firstTab_path + "/" + j
                    os.listdir(secondTab_path)
                    widget = AssetIt_Widgets.AssetIt_ListWidget(path=secondTab_path, parent=self)
                    self.allListWidets.append(widget)

                    """                     COSIUS IN                       """
                    self.addTabAuto(parentTabWidget=self.secondTab, childWidget=widget, tabName=j)

                    self.secondTab.setCurrentIndex(TAB_OPEN_SECOND)

                # ******************************************
                #           + ADD TABS BUTTON SECOND TAB
                # ******************************************
                plus_lb2 = QtWidgets.QLabel("")
                self.secondTab.addTab(plus_lb2, "+")
                plus_index2 = self.secondTab.indexOf(plus_lb2)
                self.secondTab.setTabEnabled(plus_index2, True)
                #self.secondTab.currentChanged.connect(self.Add_New_Second_Tabs)

                self.addTabAuto(parentTabWidget=self.firstTab, childWidget=self.secondTab, tabName=i)

                self.secondTab.currentChanged.connect(partial(self.get_SubTabIndex, self.secondTab))
                self.secondTab.currentChanged.connect(self.SaveTabChange)
                self.secondTab.currentChanged.connect(self.Add_New_Second_Tabs)

                """                     COSIUS OUT                       """

            except:  # créer directement les fichiers si ya qu'un seul tab

                widget = AssetIt_Widgets.AssetIt_ListWidget(path=firstTab_path, parent=self)
                self.allListWidets.append(widget)
                """                     COSIUS IN                       """
                self.addTabAuto(parentTabWidget=self.firstTab, childWidget=widget, tabName=i)
                """                     COSIUS OUT                       """





        ##FIRST TAB SETTING
        self.firstTab.currentChanged.connect(self.SaveTabChange)




        # ******************************************
        #           FAVOURITES
        # ******************************************
        favouriteFilePath = ASSET_FAVOURITES_PATH
        with open(favouriteFilePath, 'r+') as file:
            pathString = file.read()

        self.favouritesWidget = AssetIt_Widgets.AssetIt_ListWidget(path=pathString, parent=self)
        self.allListWidets.append(self.favouritesWidget)
        self.firstTab.addTab(self.favouritesWidget, "❤")





        # ******************************************
        #           SLIDER
        # ******************************************
        SliderUserPref = open(PreferencePath + 'SliderUserPref.json', "r")
        SliderUserValue_pref = json.load(SliderUserPref)
        SLIDER_VALUE = (SliderUserValue_pref['SLIDER_VALUE'])



        self.sizeSlider = QtWidgets.QSlider()
        self.sizeSlider.setMaximum(28)#18
        self.sizeSlider.setMinimum(6)#6
        self.sizeSlider.setProperty("value", SLIDER_VALUE)
        self.sizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sizeSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.sizeSlider.setTickInterval(1)
        self.sizeSlider.valueChanged.connect(self.adjustIconSize)
        self.adjustIconSize()


        # ******************************************
        #           NAME
        # ******************************************
        self.AssetName = QtWidgets.QLabel(self)
        self.AssetName.setObjectName("AssetName")
        self.AssetName.setAlignment(QtCore.Qt.AlignCenter)
        self.AssetName.setMinimumSize(30,30)




        # ******************************************
        #           RESEARCH
        # ******************************************
        self.researchBar = QtWidgets.QLineEdit()
        self.researchBar.textChanged.connect(self.researchBarTextChanged)

        self.NEW_allAssets_list = []
        # listing de tous les assets de l'asset manager
        self.allAssets_list = []
        for QListWidget in self.allListWidets:
            for eachButtonInTheList in QListWidget.buttons:
                self.allAssets_list.append(eachButtonInTheList.itemPath)
                ## POUR EVITER DUPLICATION DE FAV TAB
                # truc magique qui remove tous les items en double de la liste
                self.NEW_allAssets_list = list(set(self.allAssets_list))



        self.NEW_allAssets_list = json.dumps(self.NEW_allAssets_list)





        #
        # création du tab research
        self.researchTab = AssetIt_Widgets.AssetIt_ListWidget(path=self.NEW_allAssets_list, parent=self)
        self.lyt = QtWidgets.QVBoxLayout()
        self.lyt.addWidget(self.researchTab)
        self.researchWidget = QtWidgets.QWidget()
        self.researchWidget.setLayout(self.lyt)
        self.firstTab.addTab(self.researchWidget, "/")
        self.researchTabIndex = self.firstTab.indexOf(self.researchWidget)
        self.allListWidets.append(self.researchTab)



        # ******************************************
        #           + ADD TABS BUTTON MAIN TAB
        # ******************************************
        plus_lb = QtWidgets.QLabel("")
        self.firstTab.addTab(plus_lb, "+")
        plus_index = self.firstTab.indexOf(plus_lb)
        self.firstTab.setTabEnabled(plus_index, True)
        #self.firstTab.tabBarClicked.connect(self.Add_New_Tabs)


        self.firstTab.currentChanged.connect(self.Add_New_Tabs)
        self.secondTab.currentChanged.connect(self.Add_New_Tabs)



        # ******************************************
        #           WIDGETS
        # ******************************************

        # Définit le label qui va afficher l'asset hovered
        self.hoveredAsset_lb = QtWidgets.QLabel()
        self.hoveredAsset_lb.setFixedSize(150, self.hoveredAsset_lb.sizeHint().height())
        self.hoveredAsset_lb.setAlignment(QtCore.Qt.AlignRight)






        # ******************************************
        #        LAYOUTS STRUCTURE
        # ******************************************
        self.hlayout = QtWidgets.QHBoxLayout()

        self.hlayout.addWidget(self.sizeSlider)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.researchBar)
        self.layout.addLayout(self.ToolBarLyt)

        self.layout.addWidget(self.firstTab)

        self.layout.addLayout(self.hlayout)
        self.layout.addWidget(self.AssetName)
        self.setLayout(self.layout)




    """                     COSIUS IN                       """
    def addTabAuto(self, parentTabWidget, childWidget, tabName, insert=False):
        """ Add a tab and creates the + button next to it
            insert parameter just handles if it adds the tab after the last one or if it inserts the tab before the last one (+ button)
        """

        if insert:
            parentTabWidget.insertTab(parentTabWidget.count()-3, childWidget, tabName)
        else:
            parentTabWidget.addTab(childWidget, tabName)

        index = parentTabWidget.indexOf(childWidget)
        #plus_btn = QtWidgets.QToolButton(self)
        #plus_btn.clicked.connect(partial(self.tabPlusButtonClicked, parentTabWidget, index))
        #plus_btn.setText("|")
        #plus_btn.setStyleSheet("color:#696969")
        #parentTabWidget.tabBar().setTabButton(index, QtWidgets.QTabBar.RightSide, plus_btn)


    def tabPlusButtonClicked(self, parentTabWidget, index):
        print ("SECOND INDEX == " + str(index))

        """ Shows the menu when we click the + on a tab"""

        self.tabMenu.popup(QtGui.QCursor.pos(), None)
        self.closeAction.triggered.connect(partial(self.closeTab, parentTabWidget, index))


    def closeTab(self, parentWidget, index):
        print ("CLOSE  == " + str(index))

    def mousePressEvent(self, event):

        # Override the default Qt function to clearFocus when the clicked widget is not a QLineEdit
        focused_widget = QtWidgets.QApplication.focusWidget()
        if isinstance(focused_widget, QtWidgets.QLineEdit):
            focused_widget.clearFocus()
            QtWidgets.QMainWindow.mousePressEvent(self, event)


    """                     COSIUS OUT                       """



    def SaveTabChange(self):
        getFirstTabIndex = self.firstTab.currentIndex()
        getTabName = self.firstTab.tabText(getFirstTabIndex)

        FirstTabinfoToSave = {"TAB_OPEN" : getFirstTabIndex}
        s = json.dumps(FirstTabinfoToSave)
        open(PreferencePath + 'TabOpen.json', "w").write(s)

        FavTabSave = {"TAB_ACTIVE_NAME" : str(getTabName)}
        s = json.dumps(FavTabSave)
        open(PreferencePath + 'KnowFavTab.json', "w").write(s)

        getSecondTabIndex = int(ACTIVESUBTAB)
        SecondTabinfoToSave = {"TAB_OPEN" : getSecondTabIndex}
        s = json.dumps(SecondTabinfoToSave)
        open(PreferencePath + 'TabOpenSecond.json', "w").write(s)


    def Add_Asset(self):
        #VERIF MTOA VERSION
        getMTOA_version = str(mc.pluginInfo('mtoa', query=True, version=True))

        print("MTOA Version = " + getMTOA_version)
        if getMTOA_version >= "5.2.0":
            print("Mtoa Version Ok")
        else:
            AssetIt_Global.WarningWindow("AssetIt only works with Mtoa 5.2.0 version and higher. Contact me on Discord for help. ", 550)
            return





        SELECTION = mc.ls(sl=True)
        if SELECTION == []:
            AssetIt_Global.WarningWindow("Please select your Asset", 250)
            return

        #Pour eviter la boucle infinie avec le atClose qui clean la THumbScene
        if mc.window("Add Asset", exists=True):
            mc.deleteUI("Add Asset")

        else:
            MainTabindex = self.firstTab.currentIndex()
            currentMainTabText = self.firstTab.tabText(MainTabindex)

            if currentMainTabText == "❤":
                currentMainTab = self.firstTab.tabText(0)

            elif currentMainTabText == "/":
                currentMainTab = self.firstTab.tabText(0)

            else:
                currentMainTab = currentMainTabText



            importlib.reload(AssetIt_AddAsset)
            AssetIt_AddAsset.SEND_INFO(str(currentMainTab), str(ACTIVESUBTAB_NAME))
            AssetIt_AddAsset.showUI()







    def BatchProcess(self):
        if mc.window("Multi Asset Creation from Files", exists=True):
            mc.deleteUI("Multi Asset Creation from Files")
        else:
            MainTabindex = self.firstTab.currentIndex()
            currentMainTabText = self.firstTab.tabText(MainTabindex)

            if currentMainTabText == "❤":
                currentMainTab = self.firstTab.tabText(0)

            elif currentMainTabText == "/":
                currentMainTab = self.firstTab.tabText(0)

            else:
                currentMainTab = currentMainTabText



            from . import AssetIt_BatchProcess
            import importlib
            importlib.reload(AssetIt_BatchProcess)
            AssetIt_BatchProcess.SEND_INFO(str(currentMainTab), str(ACTIVESUBTAB_NAME))
            AssetIt_BatchProcess.showUI()


    def CreateMultiFromScene(self):
        if mc.window("Multi Asset Creation from Scene", exists=True):
            mc.deleteUI("Multi Asset Creation from Scene")
        else:
            MainTabindex = self.firstTab.currentIndex()
            currentMainTabText = self.firstTab.tabText(MainTabindex)

            if currentMainTabText == "❤":
                currentMainTab = self.firstTab.tabText(0)

            elif currentMainTabText == "/":
                currentMainTab = self.firstTab.tabText(0)

            else:
                currentMainTab = currentMainTabText



            from . import AssetIt_MultiFromScene
            import importlib
            importlib.reload(AssetIt_MultiFromScene)
            AssetIt_MultiFromScene.SEND_INFO(str(currentMainTab), str(ACTIVESUBTAB_NAME))
            AssetIt_MultiFromScene.showUI()




    def QlineEditClear(self):
        self.researchBar.clearFocus()

    def adjustIconSize(self):
        iconSize = self.sizeSlider.value() * 14
        gridSize = iconSize + 5


        for i in self.allListWidets:
            try:
                i.setGridSize(QtCore.QSize(gridSize, gridSize))
                for g in i.buttons:
                   g.setIconSize(QtCore.QSize(iconSize, iconSize))

                SliderValueInfoToSave = {"SLIDER_VALUE": self.sizeSlider.value()}
                s = json.dumps(SliderValueInfoToSave)
                open(PreferencePath + 'SliderUserPref.json', "w").write(s)
            except:
                pass

    def researchBarTextChanged(self, string):
        self.firstTab.setCurrentIndex(self.researchTabIndex)
        self.researchTab.setParent(None)

        #ON CHANGE LE CONTENU
        pathsList = json.loads(self.NEW_allAssets_list)
        nameList = []
        newPythonList = []
        for each in pathsList:
            cleanPNG = each.replace(ASSET_LIBRARY_PATH + "/", "")
            nameList.append(cleanPNG)

        #print ("NameList : " + str(nameList))

        for i in nameList:
            if string.upper() in i.upper():
                add = ASSET_LIBRARY_PATH + "/" + i
                newPythonList.append(add)

        path = json.dumps(newPythonList)

        #recréation du list widget
        #print("Path : " + path)

        self.researchTab = AssetIt_Widgets.AssetIt_ListWidget(path=path, parent=self)
        self.allListWidets.append(self.researchTab)
        self.lyt.addWidget(self.researchTab)

    def Setting_Window(self):
       AssetIt_Setting.showUI()

    def Refresh(self):
        from . import AssetIt_UI
        import importlib
        importlib.reload(AssetIt_UI)
        ui = AssetIt_UI.showUI()

    def SelGroup(self):
        #Get Active Sel Mode
        activeSelMode = mc.selectMode(q=True, root=True)
        if activeSelMode == False:
            mc.selectMode(root=True)
            self.SelGroupBTN.setIcon(QtGui.QIcon(IconPath + "Sel_Group.png"))
        else:
            mc.selectMode(object=True)
            self.SelGroupBTN.setIcon(QtGui.QIcon(IconPath + "Sel_Group_OFF.png"))


    def OpenLibFolder(self):
        os.startfile(ASSET_LIBRARY_PATH)

    def PrintTest(self, bob, index):
        print ("INDEXX = " + str(index))

    def Add_New_Tabs(self):
        NumberOfFolder = len(os.listdir(ASSET_LIBRARY_PATH))
        indexValue = int(NumberOfFolder)+2
        if self.firstTab.currentIndex() == indexValue:
            self.firstTab.setCurrentIndex(0)
            AssetIt_NewTab.showUI()


    def get_SubTabIndex(self, tab, *args):
        global ACTIVESUBTAB
        global ACTIVESUBTAB_NAME

        SUBINDEX = str(tab.currentIndex())
        SUBINDEX_NAME = tab.tabText(int(SUBINDEX))

        ACTIVESUBTAB = SUBINDEX
        ACTIVESUBTAB_NAME = SUBINDEX_NAME

        return ACTIVESUBTAB + ACTIVESUBTAB_NAME






    def Add_New_Second_Tabs(self):
        FirstTabIndex = self.firstTab.currentIndex()
        FirstTabName = self.firstTab.tabText(FirstTabIndex)

        NumberOfFolder = len(os.listdir(ASSET_LIBRARY_PATH + "/" + FirstTabName))
        indexValue = int(NumberOfFolder)

        if ACTIVESUBTAB_NAME == "+" :
            self.secondTab.setCurrentIndex(0)
            AssetIt_NewSecondTab.showUI(FirstTabName)



    def PlacementOrigin(self):
        infoToSave = {"PLACEMENT_MODE": 0}
        open(PreferencePath + 'PlacementMode.json', "w").write(json.dumps(infoToSave))


        self.PlacementOriginGridBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Orign.png"))
        self.PlacementReplaceBTN.setIcon(QtGui.QIcon(IconPath + "Replace_OFF.png"))
        self.PlacementSelectionBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Selection_OFF.png"))
        self.PlacementTopOfBTN.setIcon(QtGui.QIcon(IconPath + "PlaceOnTopOf_OFF.png"))
        self.PlacementDragBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Drag_OFF.png"))


    def PlacementSelection(self):
        infoToSave = {"PLACEMENT_MODE": 1}
        open(PreferencePath + 'PlacementMode.json', "w").write(json.dumps(infoToSave))


        self.PlacementOriginGridBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Orign_OFF.png"))
        self.PlacementReplaceBTN.setIcon(QtGui.QIcon(IconPath + "Replace_OFF.png"))
        self.PlacementSelectionBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Selection.png"))
        self.PlacementTopOfBTN.setIcon(QtGui.QIcon(IconPath + "PlaceOnTopOf_OFF.png"))
        self.PlacementDragBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Drag_OFF.png"))

    def PlacementTopOf(self):
        infoToSave = {"PLACEMENT_MODE": 2}
        open(PreferencePath + 'PlacementMode.json', "w").write(json.dumps(infoToSave))


        self.PlacementOriginGridBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Orign_OFF.png"))
        self.PlacementReplaceBTN.setIcon(QtGui.QIcon(IconPath + "Replace_OFF.png"))
        self.PlacementSelectionBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Selection_OFF.png"))
        self.PlacementTopOfBTN.setIcon(QtGui.QIcon(IconPath + "PlaceOnTopOf.png"))
        self.PlacementDragBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Drag_OFF.png"))


    def PlacementDrag(self):
        infoToSave = {"PLACEMENT_MODE": 3}
        open(PreferencePath + 'PlacementMode.json', "w").write(json.dumps(infoToSave))


        self.PlacementOriginGridBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Orign_OFF.png"))
        self.PlacementReplaceBTN.setIcon(QtGui.QIcon(IconPath + "Replace_OFF.png"))
        self.PlacementSelectionBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Selection_OFF.png"))
        self.PlacementTopOfBTN.setIcon(QtGui.QIcon(IconPath + "PlaceOnTopOf_OFF.png"))
        self.PlacementDragBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Drag.png"))

    def PlacementReplace(self):
        infoToSave = {"PLACEMENT_MODE": 4}
        open(PreferencePath + 'PlacementMode.json', "w").write(json.dumps(infoToSave))

        self.PlacementReplaceBTN.setIcon(QtGui.QIcon(IconPath + "Replace.png"))
        self.PlacementOriginGridBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Orign_OFF.png"))
        self.PlacementSelectionBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Selection_OFF.png"))
        self.PlacementTopOfBTN.setIcon(QtGui.QIcon(IconPath + "PlaceOnTopOf_OFF.png"))
        self.PlacementDragBTN.setIcon(QtGui.QIcon(IconPath + "Placement_Drag_OFF.png"))



    def PivotBottom(self):
        sel = mc.ls(sl=True)
        bbox = mc.exactWorldBoundingBox(sel)
        bottom = [(bbox[0] + bbox[3]) / 2, bbox[1], (bbox[2] + bbox[5]) / 2]
        mc.xform(sel, piv=bottom, ws=True)

    def PivotGrid(self):
        sel = mc.ls(sl=True)
        bbox = mc.exactWorldBoundingBox(sel)
        bottom = [(bbox[0] + bbox[3]) / 2, bbox[1], (bbox[2] + bbox[5]) / 2]
        mc.xform(sel, piv=bottom, ws=True)
        mc.move(0, 0, 0, sel, rpr=True)

    def GridCenter(self):
        mc.group(n="GroupTemp")
        mc.CenterPivot()
        mc.move(0, 0, 0, rpr=True)
        mc.ungroup("GroupTemp")


def Dock(Widget, width=200, height=200, hp="free", show=True):
    name = AssetIt_Global.AssetItTitle
    label = getattr(Widget, "label", name)

    try:
        cmds.deleteUI(name)
    except RuntimeError:
        pass

    dockControl = cmds.workspaceControl(
        name,
        initialWidth=width,
        minimumWidth=False,
        widthProperty=hp,
        heightProperty=hp,
        label=label
    )

    dockPtr = omui.MQtUtil.findControl(dockControl)
    dockWidget = QtCompat.wrapInstance(int(dockPtr), QtWidgets.QWidget)
    dockWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    child = Widget(dockWidget)
    dockWidget.layout().addWidget(child)

    if show:
        cmds.evalDeferred(
            lambda *args: cmds.workspaceControl(
                dockControl,
                edit=True,
                widthProperty="free",
                restore=True
            )
        )
    return child

def atClose():
    if mc.window("Thumbnail Framing", exists=True):
        mc.deleteUI("Thumbnail Framing")
    if mc.window("Add Asset", exists=True):
        mc.deleteUI("Add Asset")

    if mc.objExists("AssetIt_Thumb_Group"):
        mc.delete("AssetIt_Thumb_Group")
        mc.delete("AssetIt_Thumb_shd")
        mc.delete("AssetIt_ThumbScene_HDR")
        mc.delete("AssetI_ThumbScene_place2dTexture")
        if mc.objExists("AssetIt_Thumb_Scene_uiConfigurationScriptNode"):
            mc.delete("AssetIt_Thumb_Scene_uiConfigurationScriptNode")
        if mc.objExists("AssetIt_Thumb_Scene_sceneConfigurationScriptNode"):
            mc.delete("AssetIt_Thumb_Scene_sceneConfigurationScriptNode")

def showUI():
    global FIRSTLAUNCH

    if FIRSTLAUNCH == 0:
        infoToSave = {"FIRST_LAUNCH" : 1}
        s = json.dumps(infoToSave)
        open(PreferencePath + 'FirstLaunch.json', "w").write(s)

        from . import AssetIt_Launcher
        importlib.reload(AssetIt_Launcher)


        AssetIt_Launcher.showUI()

    else:

        ui = Dock(AssetIt_UI)
        ui.show()

        ##DELETE PopUp UI
        if mc.window("Settings", exists=True):
            mc.deleteUI("Settings")
        if mc.window("WarningWindow", exists=True):
            mc.deleteUI("WarningWindow")
        if mc.window("Thumbnail Framing", exists=True):
            mc.deleteUI("Thumbnail Framing")
        if mc.window("Add Asset", exists=True):
            mc.deleteUI("Add Asset")
        if mc.window("Info Panel", exists=True):
            mc.deleteUI("Info Panel")
        if mc.window("Add New Tab", exists=True):
            mc.deleteUI("Add New Tab")
        if mc.window("Add New Sub Tab", exists=True):
            mc.deleteUI("Add New Sub Tab")
        if mc.window("Multi Asset Creation from Files", exists=True):
            mc.deleteUI("Multi Asset Creation from Files")
        if mc.window("Multi Asset Creation from Scene", exists=True):
            mc.deleteUI("Multi Asset Creation from Scene")

        ##CLEAN Scene
        if mc.objExists("AssetIt_Thumb_Group"):
            mc.delete("AssetIt_Thumb_Group")
            mc.delete("AssetIt_Thumb_shd")
            mc.delete("AssetIt_ThumbScene_HDR")
            mc.delete("AssetI_ThumbScene_place2dTexture")
            if mc.objExists("AssetIt_Thumb_Scene_uiConfigurationScriptNode"):
                mc.delete("AssetIt_Thumb_Scene_uiConfigurationScriptNode")
            if mc.objExists("AssetIt_Thumb_Scene_sceneConfigurationScriptNode"):
                mc.delete("AssetIt_Thumb_Scene_sceneConfigurationScriptNode")



        # Get a pointer and convert it to Qt Widget object
        qw = omui.MQtUtil.findWindow(AssetIt_Global.AssetItTitle)
        try:
            widget = wrapInstance(int(qw), QWidget)
            # Create a QIcon object
            icon = QIcon(IconPath + "Windows_Ico2.png")
            # Assign the icon
            widget.setWindowIcon(icon)
        except:
            pass #Pour si on reload alos qu'il est dock


        mc.setToolTo("Move")

        mc.scriptJob(uiDeleted=[AssetIt_Global.AssetItTitle, atClose])

        return ui






