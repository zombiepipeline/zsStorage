from PySide2 import QtWidgets
from sgtk.platform.qt import QtCore, QtGui
from maya import OpenMayaUI, cmds, mel
from shiboken2 import wrapInstance
import sgtk
import os, sys, time

from .ui import dialog

reload(dialog)

from .ui.dialog import Ui_Dialog

FORMATS = ['HD1080', 'HD720', 'HD540', 'RENDER']
FRAME_TYPES = ['Start/End', 'Timer Slider', 'Current Frame']


class Dialog:
    name = 'PlayblastControl'
    shotgun = None
    shot = None
    user = None
    entity = None
    task = None
    project = None
    sequence = None
    config = None
    project_path = None
    panel = None

    def __init__(self):
        try:
            self.main = QtWidgets
            self.widget = self.main.QWidget

            if cmds.workspaceControl(self.name, query=True, exists=True):
                cmds.workspaceControl(self.name, edit=True, close=True)
                cmds.deleteUI(self.name)

            control = cmds.workspaceControl(self.name)
            cmds.workspaceControl(self.name, edit=True, label='Playblast v0.1', floating=True, restore=True, iw=300,
                                  mw=True,
                                  wp='preferred', )
            control_widget = OpenMayaUI.MQtUtil.findControl(control)
            control_wrap = wrapInstance(long(control_widget), self.widget)

            control_wrap.setObjectName(self.name)
            self.ui = Ui_Dialog()
            self.ui.setupUi(control_wrap)

            app = sgtk.platform.current_engine()
            self.shotgun = app.shotgun
            self.project_path = app.tank.project_path
            tk = sgtk.sgtk_from_path(self.project_path)
            ctx = tk.context_from_path(self.project_path)
            self.config = app.context.tank.pipeline_configuration
            self.user = sgtk.util.get_current_user(app.sgtk)
            self.step = app.context.step
            self.entity = app.context.entity
            self.task = app.context.task
            self.project = ctx.project

            self.panel = cmds.getPanel(withFocus=True)
            if self.panel != "modelPanel4":
                self.panel = "modelPanel4"
            cmds.setFocus(self.panel)

            try:
                self.shot = self.shotgun.find_one("Shot", [["id", "is", self.entity.get("id")]], ['code', 'sg_cut_in', 'sg_cut_out', 'sg_sequence'])
                self.sequence = self.shot.get('sg_sequence')

                self.ui.listFormat.addItems(FORMATS)
                self.ui.listCameras.addItems(self.AllCameras())
                self.ui.frameRangeOptions.addItems(FRAME_TYPES)

                max = cmds.playbackOptions(max=True, q=True)
                min = cmds.playbackOptions(min=True, q=True)
                self.ui.frame_in.setValue(int(min))
                self.ui.frame_out.setValue(int(max))

                if max != self.shot['sg_cut_out'] or min != self.shot['sg_cut_in']:
                    result = cmds.confirmDialog(title='Update Frame Range', message="Is the frame range of your maya different\nfrom what was defined in {}\ndo you want to update now?".format(self.shot.get('code')), button=['Yes', 'No'], defaultButton='No', cancelButton='No', dismissString='No')
                    if result == 'Yes':
                        self.setFrameRange(self.shot['sg_cut_in'], self.shot['sg_cut_out'])
            except:
                pass

            self.ui.frameRangeOptions.currentIndexChanged.connect(self.setFrameRangeType)
            self.ui.listCameras.currentIndexChanged.connect(self.setCamera)
            self.ui.frame_in.valueChanged.connect(self.setFameRage)
            self.ui.frame_out.valueChanged.connect(self.setFameRage)
            self.ui.frameRangeOptions.currentIndexChanged.connect(self.setFrameRangeType)
            self.ui.buttonRecored.clicked.connect(self.record)
            self.ui.buttonPreview.clicked.connect(self.preview)

            self.createHuds()

        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(error, exc_type, fname, exc_tb.tb_lineno)

    def setCamera(self):
        camera = self.ui.listCameras.currentText()
        cmds.modelEditor(self.panel, e=True, camera=camera)

    def setFrameRangeType(self):
        index = self.ui.frameRangeOptions.currentIndex()

        if index <= 0:
            self.ui.frame_in.setEnabled(True)
            self.ui.frame_out.setEnabled(True)
        else:
            self.ui.frame_in.setEnabled(False)
            self.ui.frame_out.setEnabled(False)

    def setFrameRange(self, in_frame, out_frame):
        self.ui.frame_in.setValue(in_frame)
        self.ui.frame_out.setValue(out_frame)

    def AllCameras(self):
        self.ui.listCameras.clear()
        cameras = list(reversed(cmds.listCameras(p=True)))
        return cameras

    def getFrames(self):
        index = int(self.ui.frameRangeOptions.currentIndex())
        frames = [
            {
                'min': self.ui.frame_in.value(),
                'max': self.ui.frame_out.value()
            },
            {
                'min': cmds.playbackOptions(min=True, q=True),
                'max': cmds.playbackOptions(max=True, q=True)
            },
            {
                'min': cmds.currentTime(q=True),
                'max': cmds.currentTime(q=True)
            }
        ]
        return frames[index]

    def setFameRage(self):
        in_frame = self.ui.frame_in.value()
        out_frame = self.ui.frame_out.value()
        cmds.playbackOptions(
            minTime=in_frame,
            maxTime=out_frame,
            animationStartTime=in_frame,
            animationEndTime=out_frame,
        )
        cmds.setAttr("defaultRenderGlobals.startFrame", in_frame)
        cmds.setAttr("defaultRenderGlobals.endFrame", out_frame)
        cmds.currentTime(in_frame)

    def record(self):
        try:
            QtCore.QCoreApplication.processEvents()
            mel.eval('setNamedPanelLayout "Single Perspective View";')
            self.setCamera()
            self.createHuds()

            time.sleep(0.7)

            SIZE = {
                'HD1080': {'width': 1920, 'height': 1080},
                'HD720': {'width': 1280, 'height': 720},
                'HD540': {'width': 960, 'height': 540},
                'RENDER': {'width': cmds.getAttr("defaultResolution.width"),
                           'height': cmds.getAttr("defaultResolution.width")}
            }

            getFormat = self.ui.listFormat.currentText()

            getSize = SIZE[getFormat]
            frame = self.getFrames()

            fileName = self.getFileName()
            path = os.path.join(self.project_path, self.getPipe(), 'movies', '_APPROVED', self.sequence['name'],
                                self.entity['name'])

            if not os.path.exists(path):
                os.makedirs(path)

            QtCore.QCoreApplication.processEvents()
            cmds.playblast(
                compression='PNG',
                format='qt',
                percent=100,
                quality=100,
                viewer=True,
                sequenceTime=False,
                combineSound=True,
                sound=self.getAudio(),
                clearCache=True,
                startTime=int(frame['min']),
                endTime=int(frame['max']),
                offScreen=True,
                showOrnaments=True,
                forceOverwrite=True,
                filename='{}/{}.mov'.format(path, fileName),
                widthHeight=[getSize['width'], getSize['height']],
                rawFrameNumbers=False,
                framePadding=4)

            QtCore.QCoreApplication.processEvents()
            self.clearHuds()
            cmds.modelEditor(self.panel, e=True, allObjects=True)

            if cmds.workspaceControl(self.name, query=True, exists=True):
                cmds.workspaceControl(self.name, edit=True, close=True)
                cmds.deleteUI(self.name)

        except RuntimeError as error:
            cmds.confirmDialog(title='Quicktime notfound',
                               message="Unable to start playblast because Quicktime is not installed!",
                               button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK')
            if cmds.workspaceControl(self.name, query=True, exists=True):
                cmds.workspaceControl(self.name, edit=True, close=True)
                cmds.deleteUI(self.name)
        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(error, exc_type, fname, exc_tb.tb_lineno)

    def preview(self):
        fileName = '{}.mov'.format(self.getFileName())
        path_name = os.path.join(self.getPipe(), 'movies', '_APPROVED', self.sequence.get('name'),
                                 self.entity.get('name'), fileName)
        path = os.path.join(self.project_path, self.getPipe(), 'movies', '_APPROVED', self.sequence.get('name'),
                            self.entity.get('name'), fileName)
        if not os.path.exists(path):
            cmds.confirmDialog(title='Playblast notfound',
                               message="Could not load preview of this playblast\nbecause the current version does not exist\n{}".format(
                                   path_name), button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK')
            return
        cmds.launch(mov=path)

    def getPipe(self):
        data = self.shotgun.find_one('PipelineConfiguration', [['code', 'is', self.config.get_name()]],
                                     ['code', 'sg_pipe_path'])
        return data['sg_pipe_path']

    def getFileName(self):
        name = cmds.file(query=True, sceneName=True, shortName=True)
        name = name.replace('.ma', '')
        return name

    def getVersion(self):
        name = cmds.file(query=True, sceneName=True, shortName=True)
        name = name.replace('.ma', '')
        return name.split('.')[-1:][0]

    def getAudio(self):
        audio = cmds.ls(type='audio')
        if audio:
            return audio[0]
        else:
            return None

    def createHuds(self):
        try:
            self.clearHuds()

            cameraName = self.ui.listCameras.currentText()
            cmds.modelEditor(self.panel, e=True, camera=cameraName)

            cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", True)
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", True)
            cmds.setAttr("hardwareRenderingGlobals.motionBlurEnable ", False)
            cmds.setAttr("hardwareRenderingGlobals.ssaoAmount", 0.2)
            cmds.setAttr("hardwareRenderingGlobals.ssaoRadius", 3)
            cmds.setAttr("hardwareRenderingGlobals.ssaoFilterRadius", 12)
            cmds.setAttr("hardwareRenderingGlobals.ssaoSamples", 16)

            cmds.select(clear=True)
            cmds.grid(toggle=False)

            cmds.modelEditor(self.panel, e=True, allObjects=False)
            cmds.modelEditor(self.panel, e=True, polymeshes=True)
            cmds.modelEditor(self.panel, e=True, xray=False)
            cmds.modelEditor(self.panel, e=True, useDefaultMaterial=False)
            cmds.modelEditor(self.panel, e=True, displayTextures=True)
            cmds.modelEditor(self.panel, e=True, shadows=False)

            cmds.modelEditor(self.panel, e=True, displayLights='default')
            cmds.modelEditor(self.panel, e=True, displayAppearance='smoothShaded')
            cmds.modelEditor(self.panel, e=True, wireframeOnShaded=False)

            cmds.camera(cameraName, e=True, displayFilmGate=False)
            cmds.camera(cameraName, e=True, displaySafeAction=False)
            cmds.camera(cameraName, e=True, displaySafeTitle=False)
            cmds.camera(cameraName, e=True, displayGateMask=False)
            cmds.camera(cameraName, e=True, displayResolution=False)
            cmds.camera(cameraName, e=True, displayFieldChart=False)

            cmds.colorManagementPrefs(e=True, ocioRulesEnabled=False)
            cmds.colorManagementPrefs(e=True, cmConfigFileEnabled=False)
            cmds.colorManagementPrefs(e=True, cmEnabled=True)
            cmds.colorManagementPrefs(e=True, viewTransformName="sRGB gamma")

            cmds.colorManagementPrefs(e=True, ocioRulesEnabled=False)
            cmds.colorManagementPrefs(e=True, cmConfigFileEnabled=False)
            cmds.colorManagementPrefs(e=True, cmEnabled=True)

            cmds.headsUpDisplay('hudProject', section=1, block=1, blockSize='small', label=self.project.get('name'),
                                labelFontSize='large')

            if self.task.get('name').lower() == 'animation':
                cmds.headsUpDisplay('hudEntityProject', section=1, block=2, blockSize='small',
                                    label='{} / {}'.format(self.sequence.get('name'), self.shot.get('code')),
                                    labelFontSize='large')
                cmds.headsUpDisplay('hudStep', section=1, block=3, blockSize='small',
                                    label='{} / {}'.format(self.step.get('name'), self.getSceneStep()),
                                    labelFontSize='large')
                cmds.headsUpDisplay('hudUser', section=1, block=4, blockSize='small',
                                    label='USER: {}'.format(self.user.get('name')), labelFontSize='large')

                cmds.headsUpDisplay('hudFrameRate', section=3, block=1, labelFontSize='large',
                                    label='FPS: {}'.format(self.getFps()))
                cmds.headsUpDisplay('hudCurrentFrame', section=3, block=2, labelFontSize='large', attachToRefresh=True,
                                    label='FRAME:', command=self.getFrame)
                cmds.headsUpDisplay('hudFrameRage', section=3, block=3, labelFontSize='large',
                                    label=self.getFrameRange())
            else:
                cmds.headsUpDisplay('hudEntityProject', section=1, block=2, blockSize='small',
                                    label='{} / {}'.format(self.task['name'].upper(), self.shot.get('code')),
                                    labelFontSize='large')
                cmds.headsUpDisplay('hudUser', section=1, block=3, blockSize='small',
                                    label='USER: {}'.format(self.user.get('name')), labelFontSize='large')
                pass

        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, error)

    def clearHuds(self):
        try:
            cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", False)
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", False)
            cmds.setAttr("hardwareRenderingGlobals.motionBlurEnable ", False)
            cmds.grid(toggle=True)

            if cmds.headsUpDisplay('hudProject', ex=True):
                cmds.headsUpDisplay('hudProject', rem=True)

            if cmds.headsUpDisplay('hudEntityProject', ex=True):
                cmds.headsUpDisplay('hudEntityProject', rem=True)

            if cmds.headsUpDisplay('hudStep', ex=True):
                cmds.headsUpDisplay('hudStep', rem=True)

            if cmds.headsUpDisplay('hudUser', ex=True):
                cmds.headsUpDisplay('hudUser', rem=True)

            if cmds.headsUpDisplay('hudFrameRate', ex=True):
                cmds.headsUpDisplay('hudFrameRate', rem=True)

            if cmds.headsUpDisplay('hudCurrentFrame', ex=True):
                cmds.headsUpDisplay('hudCurrentFrame', rem=True)

            if cmds.headsUpDisplay('hudFrameRage', ex=True):
                cmds.headsUpDisplay('hudFrameRage', rem=True)
        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, error)

    def getSceneStep(self):
        try:
            file = cmds.file(query=True, sceneName=True, shortName=True)
            file = file.split('SH')
            file = file[1].split('.')[0]
            step_file = ''
            if 'AnimBlock' in file:
                step_file = 'AnimBlock'
            if 'AnimBlockPlus' in file:
                step_file = 'AnimBlockPlus'
            if 'AnimPolish' in file:
                step_file = 'AnimPolish'
            if 'AnimRefine' in file:
                step_file = 'AnimRefine'

            return step_file.upper()
        except:
            return ''

    def getFps(self):
        return {"12fps": 12, "game": 15, "16fps": 16, "film": 24, "pal": 25, "ntsc": 30, "show": 48, "palf": 50,
                "ntscf": 60}.get(cmds.currentUnit(query=True, time=True))

    def getFrame(self):
        return cmds.currentTime(q=True)

    def getFrameRange(self):
        max = cmds.playbackOptions(max=True, q=True)
        min = cmds.playbackOptions(min=True, q=True)
        return 'FRAME RANGE: {} - {}'.format(int(min), int(max))
