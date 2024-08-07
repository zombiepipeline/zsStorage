#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2 import QtWidgets, QtCore
from maya import OpenMayaUI, cmds, mel
from shiboken2 import wrapInstance

from .ui import dialog
import time
import copy
import imp
import sys
import os

imp.reload(dialog)
from .ui.dialog import Ui_Dialog

_translate = QtCore.QCoreApplication.translate


class Dialog:
    name = 'TranferShader'
    shaders = []
    meshes = []

    def __init__(self):
        self.main = QtWidgets
        self.widget = self.main.QWidget

        if cmds.workspaceControl(self.name, query=True, exists=True):
            cmds.workspaceControl(self.name, edit=True, close=True)
            cmds.deleteUI(self.name)

        control = cmds.workspaceControl(self.name)
        cmds.workspaceControl(self.name, edit=True, label='Tranfer Shader v0.1', ttc=["AttributeEditor", 0])
        control_widget = OpenMayaUI.MQtUtil.findControl(control)
        control_wrap = wrapInstance(int(control_widget), self.widget)

        control_wrap.setObjectName(self.name)
        self.ui = Ui_Dialog()
        self.ui.setupUi(control_wrap)

        self.ui.setOrigin.clicked.connect(self.set_origin)
        self.ui.setDestiny.clicked.connect(self.set_destiny)
        self.ui.tranfer.clicked.connect(self.transfer_shaders)
        self.ui.addMesh.clicked.connect(self.add_mesh)
        self.ui.delMesh.clicked.connect(self.delete_mesh)

        self.ui.tranfer.setDisabled(True)
        self.ui.addMesh.setDisabled(True)
        self.ui.delMesh.setDisabled(True)
        self.ui.meshes.setDisabled(True)
        self.ui.progress.setVisible(False)

    def set_origin(self):
        node = cmds.ls(selection=True)

        if len(node) <= 0:
            QtWidgets.QMessageBox.information(None, _translate("Dialog", "Origem nao definda"),
                                              "Selecione a origem para obter os shaders", QtWidgets.QMessageBox.Ok)
            return
        node = node[0]

        self.ui.origin.setText(node)
        listAllMeshs = cmds.listRelatives(node, allDescendents=True, path=True)
        listAllMeshs = list(filter(lambda m: 'Shape' not in m, listAllMeshs))
        meshes = []
        errors = {}
        _erro = ""
        for mesh in listAllMeshs:
            try:
                meshes.append(mesh)
            except Exception as error:
                errors[mesh] = "<b>NAO ENCONTRADO:</b><br/>{ms}<br/>{err}<br/><br/>".format(ms=str(mesh), err=error)
        self.meshes = meshes
        self.ui.meshes.clear()
        for mesh in meshes:
            try:
                meshName = mesh.split(":")[1]
            except:
                meshName = mesh
            item_mesh = QtWidgets.QTreeWidgetItem(self.ui.meshes)
            item_mesh.setText(0, meshName)
            item_mesh.setData(0, QtCore.Qt.UserRole, meshName)

        cmds.select(clear=True)
        self.ui.addMesh.setDisabled(False)
        self.ui.delMesh.setDisabled(False)
        self.ui.meshes.setDisabled(False)

        if len(errors) > 0:
            errors = "".join(errors)
            QtWidgets.QMessageBox.information(None, "ERROR",
                                              "<b size='20px'>MESHES QUE PRECISA DE ATENCAO:</b><br/><br/>{}".format(
                                                  errors), QtWidgets.QMessageBox.Ok)

    def set_destiny(self):
        node = cmds.ls(selection=True)

        if len(node) <= 0:
            QtWidgets.QMessageBox.information(None, _translate("Dialog", "Destino nao defindo"),
                                              "Selecione o destino para tranferir os shaders", QtWidgets.QMessageBox.Ok)
            return

        node = node[0]

        self.ui.destiny.setText(node)
        cmds.select(clear=True)
        self.ui.tranfer.setDisabled(False)

    def block(self, status):
        self.ui.progress.setVisible(status)
        self.ui.setDestiny.setDisabled(status)
        self.ui.setOrigin.setDisabled(status)
        self.ui.origin.setDisabled(status)
        self.ui.destiny.setDisabled(status)
        self.ui.addMesh.setDisabled(status)
        self.ui.delMesh.setDisabled(status)
        self.ui.meshes.setDisabled(status)
        self.ui.tranfer.setDisabled(status)

    def transfer_shaders(self):
        origin = self.ui.origin.text()
        try:
            origin_name = origin.split(":")[0]
            origin_name = "{}:".format(origin_name)
        except:
            origin_name = origin

        destiny = self.ui.destiny.text()
        try:
            destiny_name = destiny.split(":")[0]
            destiny_name = "{}:".format(destiny_name)
        except:
            destiny_name = destiny

        self.block(True)

        total = self.ui.meshes.topLevelItemCount()
        counter = 0
        for m in range(self.ui.meshes.topLevelItemCount()):
            try:
                mesh = self.ui.meshes.topLevelItem(m)
                nodeMesh = mesh.data(0, QtCore.Qt.UserRole)
                nodeMesh = "{}{}".format(origin_name, nodeMesh)

                if len(nodeMesh.split('|')) > 1:
                    nodeMesh = nodeMesh.split('|')
                    nodeMesh[0] = origin_name.replace(":", "")
                    nodeMesh = "|".join(nodeMesh)
                shaderGroups = cmds.listSets(o=nodeMesh, ets=True, type=True)

                if shaderGroups:
                    for shader in shaderGroups:
                        sgMembers = cmds.sets(shader, q=True)
                        for face in sgMembers:
                            QtCore.QCoreApplication.processEvents()
                            shaderFace = face.replace(origin_name, destiny_name)
                            if len(shaderFace.split('|')) > 1:
                                shaderFace = shaderFace.split('|')
                                shaderFace[0] = destiny_name.replace(":", "")
                                shaderFace = "|".join(shaderFace)
                            cmds.sets(shaderFace, fe=shader, e=True)

                QtCore.QCoreApplication.processEvents()
                pct = ((counter * 100) / total)
                self.ui.progress.setProperty("value", pct)
                counter += 1
            except Exception as error:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("{}: {} | {} | {}".format(error, exc_type, fname, exc_tb.tb_lineno))

        QtCore.QTimer.singleShot(500, self.finalize_transfer)
        self.block(False)

    def finalize_transfer(self):
        self.ui.progress.setVisible(False)
        self.ui.progress.setProperty("value", 0)

    def add_mesh(self):
        node = cmds.ls(selection=True)

        if len(node) <= 0:
            QtWidgets.QMessageBox.information(None, _translate("Dialog", "Mesh nao selecionada"),
                                              "Selecione uma mesh para adicionar", QtWidgets.QMessageBox.Ok)
            return

        node = node[0]
        if node in self.meshes:
            QtWidgets.QMessageBox.information(None, _translate("Dialog", "Mesh ja adicionada"),
                                              "A mesh {} ja foi adicionada!".format(node), QtWidgets.QMessageBox.Ok)
            return

        shader = cmds.listHistory(node, f=1, pdo=1)
        shader = shader[0]

        if node not in self.meshes:
            self.meshes.append(node)

            try:
                shaderName = node.split('|')[-1:][0]
            except Exception as error:
                shaderName = node

            item_mesh = QtWidgets.QTreeWidgetItem(self.ui.meshes)
            item_mesh.setText(0, shaderName)
            item_mesh.setData(0, QtCore.Qt.UserRole, node)

    def delete_mesh(self):
        if len(self.ui.meshes.selectedItems()) <= 0:
            QtWidgets.QMessageBox.information(None, "Não selecionado", "Selecione as meshes que deseja remover!",
                                              QtWidgets.QMessageBox.Ok)
            return

        result = QtWidgets.QMessageBox.information(None, "REMOVER", "Deseja remover essa mesh?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        removeds = []
        meshes = copy.deepcopy(self.meshes)
        if result == QtWidgets.QMessageBox.Yes:
            root = self.ui.meshes.invisibleRootItem()
            for item in self.ui.meshes.selectedItems():
                getData = item.data(0, QtCore.Qt.UserRole)
                removeds.append(getData)
                (item.parent() or root).removeChild(item)
                meshes.pop(self.meshes.index(getData))
            self.meshes = meshes
            QtWidgets.QMessageBox.information(None, "Meshs removidas",
                                              "As meshes selecionadas foram removidas\n\n - {}".format(
                                                  "\n - ".join(removeds)), QtWidgets.QMessageBox.Ok)
