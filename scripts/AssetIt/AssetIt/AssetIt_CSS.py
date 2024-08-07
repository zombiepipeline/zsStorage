##GLOBAL VARIABLEs
from PySide2 import QtWidgets, QtCore, QtGui
from maya import cmds as mc
import maya.mel as mel
import json
import os
import maya.cmds as cmds
from maya import OpenMayaUI as omui


##THEME_SET
USERAPPDIR = mc.internalVar(userAppDir=True)
VERSION = mc.about(v=True)
IconPath = os.path.join(USERAPPDIR, VERSION+'/scripts/AssetIt/Icons/Theme_Classic/')


# Attention l'ordre est important notamen pour le QPushButton!!
##COLORS SCHEME

### GREY BG : #272727
### GREY Line : #444444
### GREEN : #b3b523
### YELLOW : #c49e19

###BLUE
  #Cyan :      A2D5D8
  #Blue Soft : 65BEF1

## Add                 border: 0px;    to Background to remove border lines


AssetIt_CSS = """

                        *{
                background: #272727;
                border: 0px;
                }

                QMenu{ 
                   background-color: #222222; 
                   border: 1px solid gray;
                   border-radius: 2px;
                   border-color: #385E74;
                }
           
                QMenu::item{
                    color: #909090;
                }                            
                
                
                QMenu::item:selected{
                    background-color: #262626;
                    color: #65BEF1;
                }                            
                
                  
                
                
                QLineEdit{ 
                   background-color: #222222; 
                   border: 1px solid gray;
                   border-radius: 3px;
                   border-color: #444444;

                }


                QLineEdit:hover{
                   background-color: #222222; 
                   border: 1px solid gray;
                   border-radius: 3px;
                   border-color: #999999;

                }


                QLineEdit:focus{
                   background-color: #222222; 
                   border: 1px solid gray;
                   border-radius: 3px;
                   border-color: #65BEF1;

                }




  
                QScrollBar::handle:vertical {
                        background: #2094D6;
                        border-radius: 3px;
                        
                }

  
                QScrollBar:vertical {
                        width: 12px;

                      }
  
  




                QListWidget{
                    background: #202020;          /* Background de la fenetre Widgets */
                    border: 2px solid #202020;
                    border-radius: 3px;
                    padding: 0px;
                }


                QListView::item:hover{
                    border : 2px solid black;
                    background : green;
                }





                /*QWidget:hover{
                    background: #808080;          
                }*/

                
                
     



                QTabWidget::pane {                    /* Ligne Ar a la suite des tabs */
                    background: #202020;

                }



                QTabBar::tab {
                    background: #282828;
                    border: 1px solid #202020;
                    border-radius: 3px;
                    min-width: 12ex;/* taille du Tab Largeur */
                    padding: 5px;/* taille du Tab Hauteur */
                    color: #909090

                }

                QTabBar::tab:hover {
                    background: #454545;
                    border: 1px solid #202020;
                    border-top: 1px solid #E3E3E3;
                    border-radius: 3px;
                    color: #E3E3E3               
                }


                QTabBar::tab:selected {
                    background: #292929;
                    border: 1px solid #202020;
                    border-top: 1px solid #419ED3;
                    border-radius: 3px;
                    color: #419ED3               
                }







                QSlider {
                    min-height: 12;
                    max-height: 12;
                }


                QSlider::handle:horizontal {
                background: #65BEF1;
                width: 22px;
                margin-top: -4px;
                margin-bottom: -4px;
                border-radius: 2px;
                min-height: 10;
                max-height: 10;
                }



                QSlider::groove:horizontal {
                background: #404040;
                height: 1px;
        
                }





                QToolTip {
                    background-color : #202020;
                    color : #65BEF1;
                    font-size: 16px;
                }



                QPushButton{ background-color: #282828; 

                }
                
                
                QPushButton:hover{ background-color: #404040; 
                                   border-radius: 3px;
                }

                QPushButton:pressed{ background-color: #222222; 

                }


                QPushButton[objectName^="Items"]{ 
                             background-color: #232323; 
                             border: 1px solid gray; 
                             border-color: #202020; 
                }
                
                QPushButton[objectName^="Items"]:hover{ 
                            background-color: #303030;
                            border: 2px solid gray; 
                            border-color: #505050; 
                }

           
                QToolButton{ 
                                color : #404040; 
                }

                QToolButton:hover{ 
                                color : #606060; 
                }


           
           
           
           

                QPushButton[objectName^="AddAsset"]{ 
                                background-color : #222222;
                                color : #808080; 
                }

                QPushButton[objectName^="AddAsset"]:hover{ 
                                background-color : #252525;
                               border: 1px solid gray; 
                                 border-color: #65BEF1; 
                                color : #65BEF1; 
                }

                QPushButton[objectName^="AddAsset"]:pressed{ 
                                background-color : #141414;
                                border: 1px solid gray; 
                                 border-color: #222222; 
                                color : #404040; 
                }





                QPushButton[objectName^="SaveSetting"]:hover{ 
                                background-color : #252525;
                                border: 1px solid gray; 
                                border-color: #FFFFFF;
                                border-radius: 2px; 
                                color : #FFFFFF; 
                }

                QPushButton[objectName^="SaveSetting"]{ 
                                background-color : #252525;
                                border: 1px solid gray; 
                                border-color: #65BEF1; 
                                border-radius: 2px; 
                                color : #65BEF1; 
                }

                QPushButton[objectName^="SaveSetting"]:pressed{ 
                                background-color : #202020;
                                border: 1px solid gray; 
                                border-color: #606060; 
                                border-radius: 2px; 
                                color : #606060; 
                }







                QPushButton[objectName^="CleanFav"]{ 
                                background-color : #252525;
                                border: 1px solid gray; 
                                border-color: #b7842a; 
                                color : #b7842a; 
                }

                QPushButton[objectName^="CleanFav"]:hover{ 
                                background-color : #252525;
                                border: 1px solid gray; 
                                border-color: #FF9B22; 
                                color : #FF9B22; 
                }

                QPushButton[objectName^="CleanFav"]:pressed{ 
                                background-color : #141414;
                                border: 1px solid gray; 
                                 border-color: #222222; 
                                color : #404040; 
                }




                QPushButton[objectName^="Separator"]{ 
                             background-color: #272727; 
                }


                     
                QLineEdit[objectName^="UserLibPathField"]{ 
                        background-color: #222222;
                        color: #65BEF1;
                }
                



                QLabel[objectName^="AssetName"]{
                        background-color : #1E1E1E; 
                        color : #65BEF1;  
                        border: 1px solid gray; 
                        border-color: #353535; 
                        border-radius: 2px; 
                }

                QLabel[objectName^="AssetTitle"]{
                        color : #65BEF1;  
                }


                QLabel[objectName^="ThumbAsset"]{
                        background-color : #232323; 
                        color : #65BEF1;  
                        border: 1px solid gray; 
                        border-color: #383838; 
                        border-radius: 2px; 
                }



                QDoubleSpinBox{
                    font-size:17px;
                    background-color: #242424;
                    width: 60px;
                    
                }
                
                QDoubleSpinBox::focus{
                        border: 1px solid #b3b523;
                        font-size:17px;
                        background-color: #1e1e1e;
                        border-color: #65BEF1; 
                        border-radius: 2px; 
                        width: 60px;
                                
                }
                       




                QComboBox {
                    border: 2px solid gray;
                    border-radius: 4px; 
                    background: #232323;
                    border-color: #232323;
                    padding: 1px 2px 1px 3px;
                    min-width: 6em;
                    color: #C2C2C2;
                }
                
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 15px;
                 
                    border-top-right-radius: 3px;
                    border-bottom-right-radius: 3px;
                }
                
                QComboBox::down-arrow {
                     image: url(""" + IconPath + """ComboBox_Arrow.png);
                     
                }






                QCheckBox[objectName^="ClayRender"]::indicator:Unchecked:hover{image: url(""" + IconPath + """ClayRender_ON.png);
                        border: 0px solid #444444;
                }     
                QCheckBox[objectName^="ClayRender"]::indicator:checked {image: url(""" + IconPath + """ClayRender_ON.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="ClayRender"]::indicator:Unchecked {image: url(""" + IconPath + """ClayRender_OFF.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="ClayRender"]::indicator:checked:hover{image: url(""" + IconPath + """ClayRender_OVER.png);
                        border: 0px solid #444444;
                }
                 
                
                
                QGroupBox {
                    border: 1px solid gray;
                    border-color: #444444;
                    border-radius: 4px; 
                    color : #65BEF1;
                    margin-top: 18px;
                    font-size: 16px;

                }
                
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10x;
                    padding: 1px 12px;

                }   


                QRadioButton::indicator::unchecked{ 
                border: 1px solid; 
                border-color: #444444;
                border-radius: 5px;
                background-color: #444444; 
                width: 9px; 
                height: 9px; 
                }
                
                QRadioButton::indicator:unchecked:hover
                {
                border: 1px solid; 
                border-color: #888888;
                border-radius: 5px;
                background-color: #888888; 
                width: 9px; 
                height: 9px; 
                }
                                
                
                
                QRadioButton::indicator::checked{ 
                border: 1px solid; 
                border-color: #65BEF1;
                border-radius: 5px;
                background-color: #65BEF1; 
                width: 9px; 
                height: 9px; 
                }
                
                
     
                
                
                

                """

Maya_CSS = """

                        *{

                }

                QPushButton{ 
                    border: 0px;

                }
                
                
                QPushButton:hover{ background-color: #656565; 

                }

                QPushButton:pressed{ background-color: #303030; 

                }



                """


EnvIt_CSS = """
               
                        *{
                background: #1e1e1e;
                border: 0px;
                }
                        
                QProgressBar{
                    border: 1px solid #b3b523;
                    border-radius: 5px;
                    text-align: center;
                    color: grey;
                }
                
                QProgressBar::chunk {
                    background-color: #b3b523;
                }

                QScrollArea[objectName^="AssetLister"]{
                    background: #739900;
                    border: 1px solid gray;
                    border-radius: 1px;
                    border-color: #b3b523;
 
                }
  
                  QScrollArea[objectName^="LayerLister"]{
                    background: #444444;
                    border: 1px solid gray;
                    border-radius: 1px;
                    border-color: #444444;
 
                }
  
   
                   QScrollArea[objectName^="SurfaceLister"]{
                    background: #739900;
                    border: 1px solid gray;
                    border-radius: 1px;
                    border-color: #2da6ec;
 
                }
                     
      
                
                 QGroupBox::indicator:unchecked{ 
                            border: 1px solid gray;
                            border-radius: 1px;
                            border-color: #444444;
                            
                 }
                 QGroupBox::indicator:unchecked:hover{ 
                            border: 1px solid gray;
                            border-radius: 1px;
                            border-color: #b3b523;
                            
                 }
                QGroupBox::indicator:Checked{
                                border: 1px solid #444444;
                                image: url(""" + IconPath + """Checkbox_Checked.png);

                                
                            }
                            
                QGroupBox::indicator:Checked:hover{
                                border: 1px solid #b3b523;

                                
                            }
                
                QSpinBox{
                                font-size:17px;
                                background-color: #242424;
                                width: 60px;
                                
                            }
                
                QSpinBox::focus{
                                border: 1px solid #b3b523;
                                font-size:17px;
                                background-color: #1e1e1e;
                                width: 60px;
                                
                            }
                            
                QSpinBox::down-button{
                                image: url(""" + IconPath + """LoadLand_Button.png);
                                width: 12;
                            }
                            
                QSpinBox::up-button{
                                image: url(""" + IconPath + """LoadLand_ButtonUp.png);
                                width: 12;
                            }
                            
                            
                QSpinBox[objectName^="SliderMax"]{
                                font-size:17px;
                                background-color: #1e1e1e;
                                color: #666666;
                                width: 40px;
                                
                            }               
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                QDoubleSpinBox{

                                font-size:17px;
                                background-color: #242424;
                                width: 57px;
                                
                            }            
                
                QDoubleSpinBox::focus{
                                border: 1px solid #b3b523;
                                font-size:17px;
                                background-color: #1e1e1e;
                                width: 57px;
                                
                            }
                
                QGroupBox {
                    border: 1px solid gray;
                    border-color: #444444;
                    background-color : #1e1e1e;
                    color : #b3b523;
                    margin-top: 18px;
                    font-size: 16px;

                }
                
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10x;
                    padding: 1px 12px;
                    background-color: #1e1e1e;

                }            
                                        
                QScrollArea[objectName^="AssetTab"]{
                    background: #739900;
                    border: 1px solid gray;
                    border-radius: 1px;
                    border-color: #444444;
 
                }
                     
                QToolTip {
                    background-color : #1e1e1e;
                    color : #b3b523;
                    margin-top: 15px;
                    font-size: 16px;

                }

                QPushButton{ background-color: #282828; 
                             border-radius: 3px;

                }
                
                
                QPushButton:hover{ background-color: #383838; 
                                   border-radius: 3px;

                }

                QPushButton:pressed{ background-color: #010101; 
                                     border: 1px solid gray;
                                     border-radius: 3px;
                                     border-color: #161616;

                }



                QPushButton[objectName^="layerON"]{
                    background-color: #97991d;
                    color: #1e1e1e
                }
                QPushButton[objectName^="layerOFF"]{
                    background-color: #222222; 
                    color: #555555
                }

                QPushButton[objectName^="PauseOFF"]{image: url(""" + IconPath + """Lister_Pause_Off.png);
                    background-color: #1e1e1e; 
                }
                QPushButton[objectName^="PauseOFF"]:hover{image: url(""" + IconPath + """Lister_Pause_On.png);
                    background-color: #1e1e1e; 
                }

                QPushButton[objectName^="LayerDelete"]{image: url(""" + IconPath + """Layer_Supp_off.png);
                    background-color: #1e1e1e; 
                }
                QPushButton[objectName^="LayerDelete"]:hover{image: url(""" + IconPath + """Layer_Supp.png);
                    background-color: #1e1e1e; 
                }
                
                QPushButton[objectName^="GroundDelete"]{image: url(""" + IconPath + """DeleteGround_Off.png);
                    background-color: #1e1e1e; 
                }
                QPushButton[objectName^="GroundDelete"]:hover{image: url(""" + IconPath + """DeleteGround_Over.png);
                    background-color: #1e1e1e; 
                }



                QPushButton[objectName^="AssetNameLabel"]{
                    color: #b3b3b3
                }

                QPushButton[objectName^="iconButton"]{
                    background-color: #1e1e1e; 
                }


                QPushButton[objectName^="AssetListerSelectBtn"]{image: url(""" + IconPath + """Lister_Tree_Default_Ico.png);
                    background-color: #1e1e1e;
                }
                QPushButton[objectName^="AssetListerSelectBtn"]:hover{image: url(""" + IconPath + """Lister_Tree_DefaultHover_Ico.png);
                    background-color: #1e1e1e; 
                }

                QPushButton[objectName^="AssetListerShaderBtn"]{image: url(""" + IconPath + """Lister_Shader_Off.png);
                    background-color: #1e1e1e; 
                }
                QPushButton[objectName^="AssetListerShaderBtn"]:hover{image: url(""" + IconPath + """Lister_Shader_On.png);
                    background-color: #1e1e1e; 
                }
                
                QPushButton[objectName^="AssetListerReload"]{image: url(""" + IconPath + """Lister_ReloadOff_Ico.png);
                    background-color: #1e1e1e; 
                }
                QPushButton[objectName^="AssetListerReload"]:hover{image: url(""" + IconPath + """Lister_ReloadHover_Ico.png);
                    background-color: #1e1e1e; 
                }


                QPushButton[objectName^="AssetListerDelete"]{image: url(""" + IconPath + """Lister_DeleteOff_Ico.png);
                    background-color: #1e1e1e; 
                }
                QPushButton[objectName^="AssetListerDelete"]:hover{image: url(""" + IconPath + """Lister_DeleteHover_Ico.png);
                    background-color: #1e1e1e; 
                }








                QPushButton[objectName^="SurfaceListerSelectBtn"]{image: url(""" + IconPath + """Lister_Mesh_Default_Ico.png);
                    background-color: #1e1e1e; 
                }
                QPushButton[objectName^="SurfaceListerSelectBtn"]:hover{image: url(""" + IconPath + """Lister_Mesh_DefaultHover_Ico.png);
                    background-color: #1e1e1e; 
                }


                QTabWidget::pane {
                    border-top: 0px solid grey;
                }

                
                
                
                
                
                
                QSlider[objectName^="GreySlider"] {
                    min-height: 24;
                    max-height: 24;
                }
                
                QSlider[objectName^="GreySlider"]::groove:horizontal {
                border: 1px solid #404040;
                background: qlineargradient(x0:0, y1:1, x2:1, y2:1, stop:0 #000000, stop:1 #ffffff);
                height: 15;
                border-radius: 4px;
                }
                
                
                QSlider[objectName^="GreySlider"]::handle:horizontal {
                border: 1px solid #000000;
                background: #e5e5e5;
                width: 6px;
                margin-top: -4px;
                margin-bottom: -4px;
                border-radius: 2px;
                min-height: 24;
                max-height: 24;
                }
                

  
                
                
                
                
                
                
                
                
                
  
                

                
                QSlider[objectName^="GreenSlider"] {
                    min-height: 24px;
                    max-height: 24px;
                }

                QSlider[objectName^="GreenSlider"]::groove:horizontal {
                background: #444444;
                height: 5px;
                border-radius: 2px;
                }
                
                QSlider[objectName^="GreenSlider"]::sub-page:horizontal {
                background: #b3b523;
                }
                
                QSlider[objectName^="GreenSlider"]::add-page:horizontal {
                background: #444444;
                border-radius: 4px;
                }
                
                QSlider[objectName^="GreenSlider"]::handle:horizontal {
                background: #b3b523;
                width: 9px;
                margin: -7px -2px;
                border-radius: 2px;
                }
                           













                QTabWidget::pane {
                    border-top: 0px solid grey;
                }




                QListWidget{
                    background: #444444;
                    border: 2px solid gray;
                    border-radius: 10px;

                }

                QTableWidget{
                    background: #444444;
                    border: 2px solid gray;
                    border-radius: 10px;

                }             
                

                
                QTabBar::tab {
                    background: #1e1e1e;
                    min-width: 12ex;/* taille du Tab Largeur */
                    padding: 3px;/* taille du Tab Hauteur */
                    color: #505050

                }

                QTabBar::tab:hover {
                    background: #1e1e1e;
                    border: 2px solid #1e1e1e;
                    border-top-color: #e7e251; /* same as the pane color */
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;                
                }

                QTabBar::tab:selected {
                    background: #1e1e1e;
                    border: 2px solid #1e1e1e;
                    border-top-color: #b3b523; /* same as the pane color */
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    color: #b3b523              
                }














                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: #1e1e1e;
                    border:0;
                }

            
    
                


                QCheckBox::indicator:Unchecked:hover{
                                border: 1px solid #b3b523;
 
                                background-color: #1e1e1e;
                                
                            }
                QCheckBox::indicator:Unchecked{
                                border: 1px solid #444444;
                                background-color: #1e1e1e;
                                
                            }
                QCheckBox::indicator:Checked{
                                border: 1px solid #444444;
                                image: url(""" + IconPath + """Checkbox_Checked.png);

                                
                            }
                            
                QCheckBox::indicator:Checked:hover{
                                border: 1px solid #b3b523;

                                
                            }
                
                QCheckBox[objectName^="AssetListerCheckBox"]::indicator:Unchecked:hover{image: url(""" + IconPath + """Lister_HideOver_Ico.png);
                        border: 0px solid #444444;
                }     
                QCheckBox[objectName^="AssetListerCheckBox"]::indicator:checked {image: url(""" + IconPath + """Lister_Show_Ico.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="AssetListerCheckBox"]::indicator:Unchecked {image: url(""" + IconPath + """Lister_Hide_Ico.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="AssetListerCheckBox"]::indicator:checked:hover{image: url(""" + IconPath + """Lister_ShowOver_Ico.png);
                        border: 0px solid #444444;
                }
     
     
     
                QCheckBox[objectName^="LayerCb"]::indicator:Unchecked:hover{image: url(""" + IconPath + """Layer_Show_ON.png);
                        border: 0px solid #444444;
                }     
                QCheckBox[objectName^="LayerCb"]::indicator:checked {image: url(""" + IconPath + """Layer_Show_ON.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="LayerCb"]::indicator:Unchecked {image: url(""" + IconPath + """Layer_Show_OFF.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="LayerCb"]::indicator:checked:hover{image: url(""" + IconPath + """Layer_Show_ON_Over.png);
                        border: 0px solid #444444;
                }
                 
                
                
                
                QCheckBox[objectName^="MeshListerCheckBox"]::indicator:Unchecked:hover{image: url(""" + IconPath + """Lister_Mesh_HideOver_Ico.png);
                        border: 0px solid #444444;
                }     
                QCheckBox[objectName^="MeshListerCheckBox"]::indicator:checked {image: url(""" + IconPath + """Lister_Mesh_Show_Ico.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="MeshListerCheckBox"]::indicator:Unchecked {image: url(""" + IconPath + """Lister_Mesh_Hide_Ico.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="MeshListerCheckBox"]::indicator:checked:hover{image: url(""" + IconPath + """Lister_Mesh_ShowOver_Ico.png);
                        border: 0px solid #444444;
                }
                             
                             
                             
                             
                QCheckBox[objectName^="SurfaceAddSubListerCheckBox"]::indicator:Unchecked:hover{image: url(""" + IconPath + """Lister_Mesh_Sub_Over_Ico.png);
                        border: 0px solid #444444;
                }     
                QCheckBox[objectName^="SurfaceAddSubListerCheckBox"]::indicator:checked {image: url(""" + IconPath + """Lister_Mesh_Add_Ico.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="SurfaceAddSubListerCheckBox"]::indicator:Unchecked {image: url(""" + IconPath + """Lister_Mesh_Sub_Ico.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="SurfaceAddSubListerCheckBox"]::indicator:checked:hover{image: url(""" + IconPath + """Lister_Mesh_Add_Over_Ico.png);
                        border: 0px solid #444444;
                }
                                
                  QCheckBox[objectName^="PauseBtn"]::indicator:Unchecked:hover{image: url(""" + IconPath + """PauseOver.png);
                        border: 0px solid #444444;
                }     
                QCheckBox[objectName^="PauseBtn"]::indicator:checked {image: url(""" + IconPath + """PauseRed.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="PauseBtn"]::indicator:Unchecked {image: url(""" + IconPath + """Pause.png);
                        border: 0px solid #444444;
                }
                QCheckBox[objectName^="PauseBtn"]::indicator:checked:hover{image: url(""" + IconPath + """PauseRedOver.png);
                        border: 0px solid #444444;
                }                              
                                
                                
                                
                QRadioButton::indicator::unchecked{ 
                border: 1px solid; 
                border-color: #444444;
                border-radius: 5px;
                background-color: #444444; 
                width: 9px; 
                height: 9px; 
                }
                
                QRadioButton::indicator:unchecked:hover
                {
                border: 1px solid; 
                border-color: #888888;
                border-radius: 5px;
                background-color: #888888; 
                width: 9px; 
                height: 9px; 
                }
                                
                
                
                QRadioButton::indicator::checked{ 
                border: 1px solid; 
                border-color: #65BEF1;
                border-radius: 5px;
                background-color: #65BEF1; 
                width: 9px; 
                height: 9px; 
                }
                
                
                
                
                
                
                
                QComboBox {
                    border: 1px solid gray;
                    border-radius: 4px; 
                    background: #282828;
                    border-color: #282828;
                    padding: 1px 23px 1px 3px;
                    min-width: 6em;
                    color: #ffffff;
                }
                
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 20px;
                 
                    border-top-right-radius: 3px;
                    border-bottom-right-radius: 3px;
                }
                
                QComboBox::down-arrow {
                     image: url(""" + IconPath + """ComboBox_Arrow.png);
                     
                }
                                
                }

                """


