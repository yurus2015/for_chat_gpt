import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMaya as OpenMaya


from PySide2.QtCore import QSettings, Qt
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from shiboken2 import wrapInstance
from full_metal_toolset.full_metal_keys import *
from full_metal_toolset.full_metal_items import *
from full_metal_toolset.full_metal_rig import *
from full_metal_toolset.full_metal_scene import *
from full_metal_toolset.full_metal_IO import *
from full_metal_toolset.full_metal_skin import *


from full_metal_toolset.src.middleware import skinWheels
import full_metal_toolset.full_metal_Qt as CustomQt

import os
import sys
import subprocess










def getMayaWindow():
    point = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(point), QWidget)

class mainWindow(QMainWindow):
    def __init__(self, parent=getMayaWindow()):
        QMainWindow.__init__(self, parent)







        self.winName = 'Full metal toolset: '
        self.setWindowTitle(self.winName + 'Untitled*')
        self.instance = FullMetalRig()
        self.instance.gatheringInformation()
        self.toolWatcher = ButtonWatcher()
        self.lodsWatcher = LodsWatcher()
        self.nodesWatcher = ButtonWatcher()
        self.centralWidget = QWidget(self)
        self.centralWidget.setAutoFillBackground(True)

        self.centralWidget.setPalette(QPalette(QColor(50, 50, 50)))
        self.mainLayoutVertical = QVBoxLayout(self.centralWidget)
        self.mainLayoutVertical.setSpacing(0)
        self.mainLayoutVertical.setContentsMargins(1, 3, 1, 1)
        self.mainLayoutHorizontal = QHBoxLayout()
        self.mainLayoutHorizontal.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = CustomQt.QView()
        self.skinTank = skinTank(self.graphicsView)
        self.sceneEventFilter = QSceneFilter(self.centralWidget)
        self.sceneEventFilter.setButtonWatcher(self.toolWatcher, self.nodesWatcher)
        self.currentScene = None
        self.toolPanel = QDockWidget()
        self.toolPanel.setTitleBarWidget(QWidget())
        self.toolPanel.setAutoFillBackground(True)
        self.toolPanel.setPalette(QPalette(QColor(50, 50, 50)))
        self.toolPanel.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        self.toolPanelWidget = QWidget()
        self.toolPanel.setWidget(self.toolPanelWidget)
        self.toolPanelLayout = QHBoxLayout()
        self.toolPanelLayout.setContentsMargins(5, 1, 1, 1)
        self.toolPanelLayout.setSpacing(2)
        self.toolPanelLayout.setAlignment(Qt.AlignLeft)
        self.toolPanelWidget.setLayout(self.toolPanelLayout)
        self.toolPanelTab1 = QTabWidget(self.toolPanelWidget)
        self.toolPanelTab1.setStyleSheet("  {border: 0px solid; background-color: rgb(68, 68, 68, );}")
        self.toolPanelTab1.setStyleSheet(
            " QTabWidget {  border: 0px solid;}  QTabBar { background-color: rgb(68, 68, 68, );}")
        self.tab1 = QWidget()
        self.tab1.setAutoFillBackground(True)

        self.tab1Layout = QHBoxLayout()
        self.tab1Layout.setContentsMargins(7, 5, 50, 5)
        self.tab1Layout.setSpacing(7)
        self.tab1Layout.setAlignment(Qt.AlignLeft)
        self.tab1.setLayout(self.tab1Layout)
        self.toolPanelTab1.addTab(self.tab1, "File")
        self.toolPanelLayout.addWidget(self.toolPanelTab1)
        self.toolPanelTab1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred);
        self.toolPanelTab2 = QTabWidget(self.toolPanelWidget)

        self.toolPanelTab2.setStyleSheet(
            "QTabWidget {  border: 0px solid;}  QTabBar {  border: 0px solid; background-color: rgb(68, 68, 68, );}")
        self.toolPanelTab2.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred);
        self.tab2 = QWidget()
        self.tab2.setAutoFillBackground(True)

        self.tab2Layout = QHBoxLayout()
        self.tab2Layout.setContentsMargins(7, 5, 50, 5)
        self.tab2Layout.setSpacing(7)
        self.tab2Layout.setAlignment(Qt.AlignLeft)
        self.tab2.setLayout(self.tab2Layout)
        self.toolPanelTab2.addTab(self.tab2, "Scene data")
        self.toolPanelLayout.addWidget(self.toolPanelTab2)
        self.toolPanelTab3 = QTabWidget(self.toolPanelWidget)
        self.toolPanelTab3.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred);
        self.toolPanelTab3.setStyleSheet("  {border: 0px solid; background-color: rgb(68, 68, 68, );}")
        self.toolPanelTab3.setStyleSheet(
            " QTabWidget {  border: 0px solid;}  QTabBar { border: 0px solid; background-color: rgb(68, 68, 68, );}")
        self.tab3 = QWidget()
        self.tab3.setAutoFillBackground(True)

        self.tab3Layout = QHBoxLayout()
        self.tab3Layout.setContentsMargins(7, 5, 50, 5)
        self.tab3Layout.setSpacing(7)
        self.tab3Layout.setAlignment(Qt.AlignLeft)
        self.tab3.setLayout(self.tab3Layout)
        self.toolPanelTab3.addTab(self.tab3, "Nodes")
        self.toolPanelLayout.addWidget(self.toolPanelTab3)
        self.toolPanelTab4 = QTabWidget(self.toolPanelWidget)

        self.toolPanelTab4.setStyleSheet("  {border: 0px solid; background-color: rgb(68, 68, 68, );}")
        self.toolPanelTab4.setStyleSheet(
            " QTabWidget {  border: 0px solid;}  QTabBar { background-color: rgb(68, 68, 68, );}")
        self.tab4 = QWidget()
        self.tab4.setAutoFillBackground(True)

        self.tab4Layout = QHBoxLayout()
        self.tab4Layout.setContentsMargins(7, 5, 5, 5)
        self.tab4Layout.setSpacing(7)
        self.tab4Layout.setAlignment(Qt.AlignLeft)
        self.tab4.setLayout(self.tab4Layout)
        self.toolPanelTab4.addTab(self.tab4, "Skin")
        self.toolPanelLayout.addWidget(self.toolPanelTab4)
        self.tab5Layout = QHBoxLayout()
        self.tab5Layout.setContentsMargins(0, 20, 0, 0)
        self.tab5Layout.setSpacing(7)
        self.tab5Layout.setAlignment(Qt.AlignRight)
        self.toolPanelLayout.addLayout(self.tab5Layout)
        self.leftPanel = QDockWidget()
        self.leftPanel.setTitleBarWidget(QWidget())
        self.leftPanel.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.leftPanelWidget = QWidget()
        self.leftPanel.setWidget(self.leftPanelWidget)
        self.leftPanelLayout = QVBoxLayout()
        self.leftPanelLayout.setContentsMargins(5, 20, 0, 0)
        self.leftPanelLayout.setAlignment(Qt.AlignTop)
        self.leftPanelWidget.setLayout(self.leftPanelLayout)
        self.rightPanel = QDockWidget()
        self.rightPanel.setTitleBarWidget(QWidget())
        self.rightPanel.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.rightPanel.setAutoFillBackground(True)
        self.rightPanel.setPalette(QPalette(QColor(50, 50, 50)))
        self.rightPanelWidget = QWidget()
        self.rightPanel.setWidget(self.rightPanelWidget)
        self.rightPanelLayout = QVBoxLayout()
        self.rightPanelLayout.setContentsMargins(1, 2, 0, 0)
        self.rightPanelLayout.setSpacing(1)
        self.rightPanelLayout.setAlignment(Qt.AlignTop)
        self.rightPanelWidget.setLayout(self.rightPanelLayout)
        self.rightPanelWeightTab = QTabWidget(self.rightPanelWidget)
        self.rightPanelWeightTab.setStyleSheet("  { border: 0px solid; background-color: rgb(68, 68, 68, );}")
        self.weightTab = QWidget()
        self.weightTab.setAutoFillBackground(True)
        self.rightPanelWeightTab.setStyleSheet(
            " QTabWidget {  border: 0px solid;}  QTabBar { background-color: rgb(68, 68, 68, );}")
        self.weightTab.setPalette(QPalette(QColor(68, 68, 68)))
        self.weightTabLayout = QVBoxLayout()

        self.weightTabLayout.setSpacing(15)

        self.weightTab.setLayout(self.weightTabLayout)
        self.rightPanelWeightTab.addTab(self.weightTab, "Weight options")
        self.rightPanelLayout.addWidget(self.rightPanelWeightTab)
        self.rightPanelWeightTab.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred);
        self.rightPanelLayersTab = QTabWidget(self.rightPanelWidget)
        self.rightPanelLayersTab.setStyleSheet(
            " QTabWidget {  border: 0px solid;}  QTabBar { background-color: rgb(68, 68, 68, );}")
        self.layersTab = QWidget()
        self.layersTab.setAutoFillBackground(True)

        self.layersTabLayout = QVBoxLayout()
        self.layersTabLayout.setContentsMargins(5, 5, 5, 5)


        self.layersTab.setLayout(self.layersTabLayout)
        self.rightPanelLayersTab.addTab(self.layersTab, "Layers")
        self.rightPanelLayout.addWidget(self.rightPanelLayersTab)
        self.rightPanelLayersTab.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred);
        self.rightPanelExceptionTab = QTabWidget(self.rightPanelWidget)
        self.rightPanelExceptionTab.setStyleSheet("  { border: 0px solid; background-color: rgb(68, 68, 68, );}")
        self.rightPanelExceptionTab.setStyleSheet(
            " QTabWidget {  border: 0px solid;}  QTabBar { background-color: rgb(68, 68, 68, );}")
        self.exceptionTab = QWidget()
        self.exceptionTab.setAutoFillBackground(True)

        self.exceptionTabLayout = QVBoxLayout()



        self.exceptionTab.setLayout(self.exceptionTabLayout)
        self.rightPanelExceptionTab.addTab(self.exceptionTab, "Exception")
        self.rightPanelLayout.addWidget(self.rightPanelExceptionTab)

        self.lodsPanel = QHBoxLayout()
        self.lodsPanel.setAlignment(Qt.AlignLeft)
        self.lodsPanel.setSpacing(0)
        self.lodsPanel.setContentsMargins(0, 0, 0, 0)
        self.horizontalBox1 = QHBoxLayout()
        self.horizontalBox2 = QHBoxLayout()
        self.horizontalBox3 = QHBoxLayout()
        self.horizontalBox4 = QHBoxLayout()
        self.commandLine = QLineEdit()
        self.commandLine.setReadOnly(True)
        self.commandLine.setDisabled(True)
        self.skinWeight = QLabel()
        self.skinWeight.setText("Skin Weight")
        self.skinWeightLine = QLineEdit()
        self.skinWeightLine.setDisabled(True)
        self.skinWeightLine.returnPressed.connect(lambda: self.setWeight())

        self.vBoneWeightLabel = QLabel()
        self.vBoneWeightLabel.setText("V bone Weight")
        self.vBoneWeight = QLineEdit()
        self.vBoneWeight.setText("0.0")
        self.vBoneWeight.setDisabled(True)
        self.vBoneWeight.returnPressed.connect(lambda: self.setWeight())

        self.weightDivider = QPushButton()
        self.weightDivider.setFixedSize(50, 50)
        self.sharedWeight = QCheckBox()
        self.sharedWeight.setText("Shared weight")
        self.sharedWeight.setDisabled(True)
        self.sharedWeight.released.connect(lambda: self.setWeightDivider())
        self.weightDivider.clicked.connect(lambda: self.setWeightDivider())
        self.weightGrid = QGridLayout()
        self.weightGrid.setAlignment(Qt.AlignRight)
        self.weightGrid.setSpacing(1)
        self.wght = 0.1
















        for i in range(10):
            if self.wght > 1:
                break
            self.weightButton = QPushButton()
            if self.wght == 0.1:
                self.weightButton.setText(str(self.wght))
                self.weightButton.setObjectName(str(self.wght))
            else:
                self.weightButton.setText(str(self.wght))
                self.weightButton.setObjectName(str(self.wght))
            self.weightButton.clicked.connect(self.setWeight(self.weightButton.text()))
            self.weightButton.setMinimumSize(25, 25)
            self.wght = self.wght + 0.1
            self.weightButton.setStyleSheet(" background-color: rgb(80, 80, 80);")
            self.weightGrid.addWidget(self.weightButton, 0, i)
        self.skinGradientFactorLayout = QHBoxLayout()
        self.skinGradientFactorLabel = QLabel()
        self.skinGradientFactorSlider = QSlider()
        self.skinGradientFactorSlider.setMinimum(1);
        self.skinGradientFactorSlider.setMaximum(10)
        self.skinGradientFactorSlider.setValue(2)
        self.skinGradientFactorSlider.setDisabled(True)
        self.skinGradientFactorLabel.setText(str(self.skinGradientFactorSlider.value()))
        self.skinGradientFactorLayout.addWidget(self.skinGradientFactorLabel)
        self.skinGradientFactorLayout.addWidget(self.skinGradientFactorSlider)
        self.skinGradientFactorSlider.sliderMoved[int].connect(lambda: self.setSkinGradientFactorLabel())
        self.highlightUnusedButton = QPushButton("Select unused")
        self.highlightUnusedButton.setStyleSheet(" background-color: rgb(80, 80, 80);")
        self.highlightUnusedButton.released.connect(lambda: self.showUnused())
        self.showBonesNameButton = QPushButton("show/hide bones name")
        self.showBonesNameButton.setStyleSheet(" background-color: rgb(80, 80, 80);")
        self.showBonesNameButton.setFixedSize(120, 20)
        self.showBonesNameButton.released.connect(lambda: self.showBonesName())
        self.gradientWeightCheckBox = QCheckBox()
        self.gradientWeightCheckBox.setText("Gradient weight")
        self.gradientWeightCheckBox.setDisabled(True)
        self.gradientWeightCheckBox.released.connect(lambda: self.gradientWeightState())
        self.gradientWeightArrow = CustomQt.QGradientWeight()








        self.skingGrid = QGridLayout()
        self.skingGrid.setContentsMargins(10, 11, 0, 0)
        self.skinAllFromCurrent = QCheckBox()
        self.skinAllFromCurrent.setChecked(True)
        self.skinAllFromCurrent.setText("Skin all lods from current")
        self.skinAllSides = QCheckBox()
        self.skinAllSides.setChecked(False)
        self.skinAllSides.setEnabled(True)
        self.skinAllSides.setText("Skin all sides from current window")
        self.skinOption3 = QCheckBox()
        self.skinOption3.setChecked(False)
        self.skinOption3.setText("Mesh")
        self.skinOption4 = QCheckBox()
        self.skinOption4.setChecked(False)
        self.skinOption4.setText("Clean up nodes")
        self.skingGrid.addWidget(self.skinAllFromCurrent, 0, 0)
        self.skingGrid.addWidget(self.skinAllSides, 1, 0)

        self.load_button = CustomQt.QToolNodeButton()
        self.load_button.setObjectName("load")

        self.load_button.setlabel("Load")
        self.load_button.clicked.connect(lambda: self.IO.loadProject())

        self.save_button = CustomQt.QToolNodeButton()
        self.save_button.setObjectName("save")
        self.save_button.setlabel("Save")
        self.save_button.clicked.connect(lambda: self.IO.saveProject())

        self.forceClose_button = CustomQt.QToolNodeButton()
        self.forceClose_button.setObjectName("forceClose")
        self.forceClose_button.setFixedHeight(95)
        self.forceClose_button.setlabel(" ")

        self.forceClose_button.clicked.connect(lambda: self.callHardReset())

        self.saveAs_button = CustomQt.QToolNodeButton()
        self.saveAs_button.setObjectName("save As")
        self.saveAs_button.setlabel("Save As")

        self.saveAs_button.clicked.connect(lambda: self.IO.saveProjectAs())

        self.gatheringInformation_button = CustomQt.QToolNodeButton()

        self.gatheringInformation_button.setlabel("Get data")
        self.gatheringInformation_button.setObjectName("gatheringInformationButton")
        self.gatheringInformation_button.clicked.connect(lambda: self.gatherNewInformation())
        self.insertSplitBoxes_button = CustomQt.QToolNodeButton()
        self.insertSplitBoxes_button.setText("Insert split boxes")
        self.insertSplitBoxes_button.setObjectName("insertSplitBoxes")
        self.insertSplitBoxes_button.clicked.connect(lambda: self.instance.insertSplitBoxes())
        self.debugInfo_button = QPushButton()
        self.debugInfo_button.setText("Debug Info")
        self.debugInfo_button.setObjectName("debugInfoButton")
        self.debugInfo_button.clicked.connect(lambda: self.instance.debugInfo())
        self.hideHulls_button = QPushButton()
        self.hideHulls_button.setText("Hide hull")
        self.hideHulls_button.setObjectName("hideHullButton")
        self.hideHulls_button.clicked.connect(lambda: self.instance.hideGroup(self.instance.hullData))
        self.hideChassisL_button = QPushButton()
        self.hideChassisL_button.setText("Hide chassis")
        self.hideChassisL_button.setObjectName("hideLeftChassisButton")
        self.hideChassisL_button.clicked.connect(lambda: self.instance.hideGroup(self.instance.chassisData[0]))
        self.hideChassisR_button = QPushButton()
        self.hideChassisR_button.setText("Hide chassis")
        self.hideChassisR_button.setObjectName("hideRightChassisButton")
        self.hideChassisR_button.clicked.connect(lambda: self.instance.hideGroup(self.instance.chassisData[1]))
        self.hideTracksL_button = QPushButton()
        self.hideTracksL_button.setText("Hide L tracks")
        self.hideTracksL_button.setObjectName("hideLeftTracksButton")
        self.hideTracksL_button.clicked.connect(lambda: self.instance.hideGroup(self.instance.tracksData[0]))
        self.hideTracksR_button = QPushButton()
        self.hideTracksR_button.setText("Hide R tracks")
        self.hideTracksR_button.setObjectName("hideRightTracksButton")
        self.hideTracksR_button.clicked.connect(lambda: self.instance.hideGroup(self.instance.tracksData[1]))
        self.skin_track_button = CustomQt.QToolNodeButton()
        self.skin_track_button.setText("Track")

        self.skin_track_button.setObjectName("skinButton")
        self.skin_track_button.setlabel("Skin track")
        self.skin_track_button.clicked.connect(lambda: self.skin("track"))
        self.skin_chassis_button = CustomQt.QToolNodeButton()
        self.skin_chassis_button.setText("Chassis")

        self.skin_chassis_button.setObjectName("skinButton")
        self.skin_chassis_button.setlabel("Skin chassis")
        self.skin_chassis_button.clicked.connect(lambda: self.skin("chassis"))
        self.skin_wheels_button = CustomQt.QToolNodeButton()
        self.skin_wheels_button.setText("Wheels")

        self.skin_wheels_button.setObjectName("skinWheelsButton")
        self.skin_wheels_button.setlabel("Skin wheels")
        self.skin_wheels_button.clicked.connect(lambda: self.callSkinWheels())
        self.createLocator_button = CustomQt.QToolNodeButton()
        self.createLocator_button.setText("Create Locator")
        self.createLocator_button.setObjectName("createLocatorButton")
        self.createLocator_button.clicked.connect(lambda: self.createLocators())
        self.createLocatorsCurve_button = CustomQt.QToolNodeButton()
        self.createLocatorsCurve_button.setText("Create Locator Curve")
        self.createLocatorsCurve_button.setObjectName("createLocatorCurveButton")
        self.createLocatorsCurve_button.clicked.connect(lambda: self.createLocatorsCurve())

        self.selectTool_button = CustomQt.QToolButton()

        self.selectTool_button.setObjectName("selectTool")


        self.toolWatcher.addButton(self.selectTool_button)
        self.selectTool_button.clicked.connect(lambda: self.toolWatcher.setTool(self.selectTool_button))
        self.moveTool_button = CustomQt.QToolButton()

        self.moveTool_button.setObjectName("moveTool")


        self.toolWatcher.addButton(self.moveTool_button)
        self.moveTool_button.clicked.connect(lambda: self.toolWatcher.setTool(self.moveTool_button))
        self.rotateTool_button = CustomQt.QToolButton()

        self.rotateTool_button.setObjectName("rotateTool")


        self.toolWatcher.addButton(self.rotateTool_button)
        self.rotateTool_button.clicked.connect(lambda: self.toolWatcher.setTool(self.rotateTool_button))
        self.scaleTool_button = CustomQt.QToolButton()

        self.scaleTool_button.setObjectName("scaleTool")


        self.toolWatcher.addButton(self.scaleTool_button)
        self.scaleTool_button.clicked.connect(lambda: self.toolWatcher.setTool(self.scaleTool_button))
        self.moveNodeBox_button = CustomQt.QToolButton()
        self.moveNodeBox_button.setText("Move node box")

        self.moveNodeBox_button.clicked.connect(lambda: self.toolWatcher.setTool(self.moveNodeBox_button))
        self.nodeConnection_button = CustomQt.QToolButton()
        self.nodeConnection_button.setText("Node Connection")
        self.nodeConnection_button.setObjectName("nodeConnectionTool")
        self.nodeConnection_button.clicked.connect(lambda: self.toolWatcher.setTool(self.nodeConnection_button))

        self.jointTool_button = CustomQt.QToolNodeButton()

        self.jointTool_button.setObjectName("jointsNodeTool")

        self.jointTool_button.setlabel("Joint node")
        self.toolWatcher.addButton(self.jointTool_button)
        self.jointTool_button.clicked.connect(lambda: self.toolWatcher.setTool(self.jointTool_button))
        self.LocatorTool_button = CustomQt.QToolNodeButton()

        self.LocatorTool_button.setObjectName("locatorsNodeTool")

        self.toolWatcher.addButton(self.LocatorTool_button)
        self.LocatorTool_button.clicked.connect(lambda: self.toolWatcher.setTool(self.LocatorTool_button))
        self.searchCircleNode_button = CustomQt.QToolNodeButton()

        self.searchCircleNode_button.setObjectName("areaCircleNodeTool")

        self.searchCircleNode_button.setlabel("Circle node")
        self.toolWatcher.addButton(self.searchCircleNode_button)
        self.searchCircleNode_button.clicked.connect(lambda: self.toolWatcher.setTool(self.searchCircleNode_button))
        self.searchBoxNode_button = CustomQt.QToolNodeButton()

        self.searchBoxNode_button.setObjectName("areaBoxNodeTool")

        self.searchBoxNode_button.setlabel("Box node")
        self.toolWatcher.addButton(self.searchBoxNode_button)
        self.searchBoxNode_button.clicked.connect(lambda: self.toolWatcher.setTool(self.searchBoxNode_button))
        self.searchFreeFormNode_button = CustomQt.QToolNodeButton()

        self.searchFreeFormNode_button.setObjectName("freeFormNodeTool")

        self.searchFreeFormNode_button.setlabel("FF node")
        self.toolWatcher.addButton(self.searchFreeFormNode_button)
        self.searchFreeFormNode_button.clicked.connect(lambda: self.toolWatcher.setTool(self.searchFreeFormNode_button))
        self.searchFFNodeCreation = CustomQt.QToolNodeButton()
        self.searchFFNodeCreation.setObjectName("fFNodeCreation")
        self.toolWatcher.addButton(self.searchFFNodeCreation)
        self.searchFFNodeCreation.obj = None
        self.searchFFNodeCreation.clicked.connect(lambda: self.toolWatcher.setTool(self.searchFFNodeCreation))

        self.tab1Layout.addWidget(self.load_button)
        self.tab1Layout.addWidget(self.saveAs_button)
        self.tab1Layout.addWidget(self.save_button)
        self.tab2Layout.addWidget(self.gatheringInformation_button)
        self.tab3Layout.addWidget(self.searchCircleNode_button)
        self.tab3Layout.addWidget(self.searchBoxNode_button)
        self.tab3Layout.addWidget(self.searchFreeFormNode_button)
        self.tab4Layout.addWidget(self.skin_track_button)
        self.tab4Layout.addWidget(self.skin_chassis_button)
        self.tab4Layout.addWidget(self.skin_wheels_button)

        self.tab4Layout.addLayout(self.skingGrid)
        self.tab5Layout.addWidget(self.forceClose_button)
        self.leftPanelLayout.addWidget(self.selectTool_button)
        self.leftPanelLayout.addWidget(self.moveTool_button)
        self.leftPanelLayout.addWidget(self.rotateTool_button)
        self.leftPanelLayout.addWidget(self.scaleTool_button)
        self.rightPanelLayout.addLayout(self.horizontalBox1)
        self.rightPanelLayout.addLayout(self.horizontalBox2)
        self.arrowGroupBox = QGroupBox("Gradient weight")
        self.arrowGroupBoxLayout = QVBoxLayout(self)
        self.arrowGroupBoxLayout.addWidget(self.gradientWeightCheckBox)
        self.arrowGroupBoxLayout.addWidget(self.gradientWeightArrow)

        self.weightTabLayout.addWidget(self.sharedWeight)
        self.weightTabLayout.addLayout(self.horizontalBox3)
        self.horizontalBox3.addWidget(self.skinWeight)
        self.horizontalBox3.addWidget(self.skinWeightLine)
        self.weightTabLayout.addLayout(self.weightGrid)
        self.weightTabLayout.addLayout(self.horizontalBox4)
        self.horizontalBox4.addWidget(self.vBoneWeightLabel)
        self.horizontalBox4.addWidget(self.vBoneWeight)
        self.weightTabLayout.addLayout(self.arrowGroupBoxLayout)




        self.graphicsSceneLeftLod0 = QScene();
        self.graphicsSceneLeftLod0.setObjectName("lod0Left")
        self.graphicsSceneLeftLod1 = QScene();
        self.graphicsSceneLeftLod1.setObjectName("lod1Left")
        self.graphicsSceneLeftLod2 = QScene();
        self.graphicsSceneLeftLod2.setObjectName("lod2Left")
        self.graphicsSceneLeftLod3 = QScene();
        self.graphicsSceneLeftLod3.setObjectName("lod3Left")
        self.graphicsSceneLeftLod4 = QScene();
        self.graphicsSceneLeftLod4.setObjectName("lod4Left")

        self.graphicsSceneRightLod0 = QScene();
        self.graphicsSceneRightLod0.setObjectName("lod0Right")
        self.graphicsSceneRightLod1 = QScene();
        self.graphicsSceneRightLod1.setObjectName("lod1Right")
        self.graphicsSceneRightLod2 = QScene();
        self.graphicsSceneRightLod2.setObjectName("lod2Right")
        self.graphicsSceneRightLod3 = QScene();
        self.graphicsSceneRightLod3.setObjectName("lod3Right")
        self.graphicsSceneRightLod4 = QScene();
        self.graphicsSceneRightLod4.setObjectName("lod4Right")
        self.tempScene = QScene();
        self.scenesLeftArray = [self.graphicsSceneLeftLod0, self.graphicsSceneLeftLod1, self.graphicsSceneLeftLod2,
                                self.graphicsSceneLeftLod3, self.graphicsSceneLeftLod4]
        self.scenesRightArray = [self.graphicsSceneRightLod0, self.graphicsSceneRightLod1, self.graphicsSceneRightLod2,
                                 self.graphicsSceneRightLod3, self.graphicsSceneRightLod4]
        for x in self.scenesLeftArray:
            x.selectionChanged.connect(lambda: self.changeSelection())
            x.installEventFilter(self.sceneEventFilter)
            x.setUpScene(0)
        for x in self.scenesRightArray:
            x.selectionChanged.connect(lambda: self.changeSelection())
            x.destroyed.connect(lambda: self.ololo)
            x.installEventFilter(self.sceneEventFilter)
            x.setUpScene(1)
        self.graphicsView.setScene(self.graphicsSceneLeftLod0)
        self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)
        self.graphicsView.setRubberBandSelectionMode(True)
        self.graphicsView.setSceneRect(-5000, -5000, 10000, 10000)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.lodsWatcher.setView(self.graphicsView)

        self.addDockWidget(Qt.TopDockWidgetArea, self.toolPanel)
        self.addDockWidget(Qt.RightDockWidgetArea, self.rightPanel)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftPanel)
        self.mainLayoutVertical.addLayout(self.lodsPanel)
        self.mainLayoutVertical.addLayout(self.mainLayoutHorizontal)
        self.mainLayoutVertical.addWidget(self.commandLine)
        self.mainLayoutHorizontal.addWidget(self.graphicsView)
        self.setCentralWidget(self.centralWidget)



        self.layersContainerLeftLod0 = CustomQt.QLayersWidget(self, self.graphicsView, self.graphicsSceneLeftLod0);
        self.graphicsSceneLeftLod0.layersWidget = self.layersContainerLeftLod0
        self.layersContainerLeftLod1 = CustomQt.QLayersWidget(self, self.graphicsView, self.graphicsSceneLeftLod1);
        self.graphicsSceneLeftLod1.layersWidget = self.layersContainerLeftLod1
        self.layersContainerLeftLod2 = CustomQt.QLayersWidget(self, self.graphicsView, self.graphicsSceneLeftLod2);
        self.graphicsSceneLeftLod2.layersWidget = self.layersContainerLeftLod2
        self.layersContainerLeftLod3 = CustomQt.QLayersWidget(self, self.graphicsView, self.graphicsSceneLeftLod3);
        self.graphicsSceneLeftLod3.layersWidget = self.layersContainerLeftLod3
        self.layersContainerLeftLod4 = CustomQt.QLayersWidget(self, self.graphicsView, self.graphicsSceneLeftLod4);
        self.graphicsSceneLeftLod4.layersWidget = self.layersContainerLeftLod4

        self.layersContainerRightLod0 = CustomQt.QLayersWidget(self, self.graphicsView, self.graphicsSceneRightLod0);
        self.graphicsSceneRightLod0.layersWidget = self.layersContainerRightLod0
        self.layersContainerRightLod1 = CustomQt.QLayersWidget(self, self.graphicsView, self.graphicsSceneRightLod1);
        self.graphicsSceneRightLod1.layersWidget = self.layersContainerRightLod1
        self.layersContainerRightLod2 = CustomQt.QLayersWidget(self, self.graphicsView, self.graphicsSceneRightLod2);
        self.graphicsSceneRightLod2.layersWidget = self.layersContainerRightLod2
        self.layersContainerRightLod3 = CustomQt.QLayersWidget(self, self.graphicsView, self.graphicsSceneRightLod3);
        self.graphicsSceneRightLod3.layersWidget = self.layersContainerRightLod3
        self.layersContainerRightLod4 = CustomQt.QLayersWidget(self, self.graphicsView, self.graphicsSceneRightLod4);
        self.graphicsSceneRightLod4.layersWidget = self.layersContainerRightLod4
        self.layersContainerLeftArray = [self.layersContainerLeftLod0, self.layersContainerLeftLod1,
                                         self.layersContainerLeftLod2, self.layersContainerLeftLod3,
                                         self.layersContainerLeftLod4]
        self.layersContainerRightArray = [self.layersContainerRightLod0, self.layersContainerRightLod1,
                                          self.layersContainerRightLod2, self.layersContainerRightLod3,
                                          self.layersContainerRightLod4]
        tempAdding = True
        for x in self.layersContainerLeftArray:
            self.layersTabLayout.addWidget(x)
            if not tempAdding:
                x.hide()
            tempAdding = False
        for x in self.layersContainerRightArray:
            self.layersTabLayout.addWidget(x)
            x.hide()



        self.exclusionContainerLeftLod0 = CustomQt.QExceptionWidget(self.graphicsView, self.graphicsSceneLeftLod0);
        self.graphicsSceneLeftLod0.exceptionWidget = self.exclusionContainerLeftLod0
        self.exclusionContainerLeftLod1 = CustomQt.QExceptionWidget(self.graphicsView, self.graphicsSceneLeftLod1);
        self.graphicsSceneLeftLod1.exceptionWidget = self.exclusionContainerLeftLod1
        self.exclusionContainerLeftLod2 = CustomQt.QExceptionWidget(self.graphicsView, self.graphicsSceneLeftLod2);
        self.graphicsSceneLeftLod2.exceptionWidget = self.exclusionContainerLeftLod2
        self.exclusionContainerLeftLod3 = CustomQt.QExceptionWidget(self.graphicsView, self.graphicsSceneLeftLod3);
        self.graphicsSceneLeftLod3.exceptionWidget = self.exclusionContainerLeftLod3
        self.exclusionContainerLeftLod4 = CustomQt.QExceptionWidget(self.graphicsView, self.graphicsSceneLeftLod4);
        self.graphicsSceneLeftLod4.exceptionWidget = self.exclusionContainerLeftLod4

        self.exclusionContainerRightLod0 = CustomQt.QExceptionWidget(self.graphicsView, self.graphicsSceneRightLod0);
        self.graphicsSceneRightLod0.exceptionWidget = self.exclusionContainerRightLod0
        self.exclusionContainerRightLod1 = CustomQt.QExceptionWidget(self.graphicsView, self.graphicsSceneRightLod1);
        self.graphicsSceneRightLod1.exceptionWidget = self.exclusionContainerRightLod1
        self.exclusionContainerRightLod2 = CustomQt.QExceptionWidget(self.graphicsView, self.graphicsSceneRightLod2);
        self.graphicsSceneRightLod2.exceptionWidget = self.exclusionContainerRightLod2
        self.exclusionContainerRightLod3 = CustomQt.QExceptionWidget(self.graphicsView, self.graphicsSceneRightLod3);
        self.graphicsSceneRightLod3.exceptionWidget = self.exclusionContainerRightLod3
        self.exclusionContainerRightLod4 = CustomQt.QExceptionWidget(self.graphicsView, self.graphicsSceneRightLod4);
        self.graphicsSceneRightLod4.exceptionWidget = self.exclusionContainerRightLod4
        self.exclusionContainerLeftArray = [self.exclusionContainerLeftLod0, self.exclusionContainerLeftLod1,
                                            self.exclusionContainerLeftLod2, self.exclusionContainerLeftLod3,
                                            self.exclusionContainerLeftLod4]
        self.exclusionContainerRightArray = [self.exclusionContainerRightLod0, self.exclusionContainerRightLod1,
                                             self.exclusionContainerRightLod2, self.exclusionContainerRightLod3,
                                             self.exclusionContainerRightLod4]
        tempAdding = True
        for x in self.exclusionContainerLeftArray:
            self.exceptionTabLayout.addWidget(x)
            if not tempAdding:
                x.hide()
            tempAdding = False
        for x in self.exclusionContainerRightArray:
            self.exceptionTabLayout.addWidget(x)
            x.hide()
        self.spacer = QSpacerItem(0, 15)




        self.setLeftScene0_button = CustomQt.QLodButton()
        self.setLeftScene0_button.setText("lod0")
        self.setLeftScene0_button.setObjectName("leftLod0")
        self.setLeftScene0_button.clicked.connect(
            lambda: self.lodsWatcher.setTool(self.setLeftScene0_button, self.graphicsSceneLeftLod0,
                                             self.exclusionContainerLeftLod0, self.layersContainerLeftLod0))
        self.setLeftScene1_button = CustomQt.QLodButton()
        self.setLeftScene1_button.setText("lod1")
        self.setLeftScene1_button.setObjectName("leftLod1")
        self.setLeftScene1_button.clicked.connect(
            lambda: self.lodsWatcher.setTool(self.setLeftScene1_button, self.graphicsSceneLeftLod1,
                                             self.exclusionContainerLeftLod1, self.layersContainerLeftLod1))
        self.setLeftScene2_button = CustomQt.QLodButton()
        self.setLeftScene2_button.setText("lod2")
        self.setLeftScene2_button.setObjectName("leftLod2")
        self.setLeftScene2_button.clicked.connect(
            lambda: self.lodsWatcher.setTool(self.setLeftScene2_button, self.graphicsSceneLeftLod2,
                                             self.exclusionContainerLeftLod2, self.layersContainerLeftLod2))
        self.setLeftScene3_button = CustomQt.QLodButton()
        self.setLeftScene3_button.setText("lod3")
        self.setLeftScene3_button.setObjectName("leftLod3")
        self.setLeftScene3_button.clicked.connect(
            lambda: self.lodsWatcher.setTool(self.setLeftScene3_button, self.graphicsSceneLeftLod3,
                                             self.exclusionContainerLeftLod3, self.layersContainerLeftLod3))
        self.setLeftScene4_button = CustomQt.QLodButton()
        self.setLeftScene4_button.setText("lod4")
        self.setLeftScene4_button.setObjectName("leftLod4")
        self.setLeftScene4_button.clicked.connect(
            lambda: self.lodsWatcher.setTool(self.setLeftScene4_button, self.graphicsSceneLeftLod4,
                                             self.exclusionContainerLeftLod4, self.layersContainerLeftLod4))
        self.setRightScene0_button = CustomQt.QLodButton()
        self.setRightScene0_button.setText("lod0")
        self.setRightScene0_button.setObjectName("rightLod0")
        self.setRightScene0_button.clicked.connect(
            lambda: self.lodsWatcher.setTool(self.setRightScene0_button, self.graphicsSceneRightLod0,
                                             self.exclusionContainerRightLod0, self.layersContainerRightLod0))
        self.setRightScene1_button = CustomQt.QLodButton()
        self.setRightScene1_button.setText("lod1")
        self.setRightScene1_button.setObjectName("rightLod1")
        self.setRightScene1_button.clicked.connect(
            lambda: self.lodsWatcher.setTool(self.setRightScene1_button, self.graphicsSceneRightLod1,
                                             self.exclusionContainerRightLod1, self.layersContainerRightLod1))
        self.setRightScene2_button = CustomQt.QLodButton()
        self.setRightScene2_button.setText("lod2")
        self.setRightScene2_button.setObjectName("rightLod2")
        self.setRightScene2_button.clicked.connect(
            lambda: self.lodsWatcher.setTool(self.setRightScene2_button, self.graphicsSceneRightLod2,
                                             self.exclusionContainerRightLod2, self.layersContainerRightLod2))
        self.setRightScene3_button = CustomQt.QLodButton()
        self.setRightScene3_button.setText("lod3")
        self.setRightScene3_button.setObjectName("rightLod3")
        self.setRightScene3_button.clicked.connect(
            lambda: self.lodsWatcher.setTool(self.setRightScene3_button, self.graphicsSceneRightLod3,
                                             self.exclusionContainerRightLod3, self.layersContainerRightLod3))
        self.setRightScene4_button = CustomQt.QLodButton()
        self.setRightScene4_button.setText("lod4")
        self.setRightScene4_button.setObjectName("rightLod4")
        self.setRightScene4_button.clicked.connect(
            lambda: self.lodsWatcher.setTool(self.setRightScene4_button, self.graphicsSceneRightLod4,
                                             self.exclusionContainerRightLod4, self.layersContainerRightLod4))
        self.leftLabel = QLabel()
        self.leftLabel.setText(" left:")
        self.lodsPanel.addWidget(self.leftLabel)
        self.lodsPanel.addWidget(self.setLeftScene0_button)
        self.lodsPanel.addWidget(self.setLeftScene1_button)
        self.lodsPanel.addWidget(self.setLeftScene2_button)
        self.lodsPanel.addWidget(self.setLeftScene3_button)
        self.lodsPanel.addWidget(self.setLeftScene4_button)
        self.RightLabel = QLabel()
        self.RightLabel.setText("      right: ")
        self.lodsPanel.addWidget(self.RightLabel)
        self.lodsPanel.addWidget(self.setRightScene0_button)
        self.lodsPanel.addWidget(self.setRightScene1_button)
        self.lodsPanel.addWidget(self.setRightScene2_button)
        self.lodsPanel.addWidget(self.setRightScene3_button)
        self.lodsPanel.addWidget(self.setRightScene4_button)
        self.lodsPanel.addItem(QSpacerItem(100, 0))
        self.lodsPanel.addWidget(self.highlightUnusedButton)
        self.lodsPanel.addWidget(self.showBonesNameButton)
        self.IO = IO(self.scenesLeftArray, self.scenesRightArray, self)
        self.toolWatcher.setTool(self.selectTool_button)
        self.lodsWatcher.setTool(self.setLeftScene0_button, self.graphicsSceneLeftLod0, self.exclusionContainerLeftLod0,
                                 self.layersContainerLeftLod0)
    def showBonesName(self):
        showBN = True
        for x in self.graphicsView.scene().items():
            if x.type == "jointsItem":
                if x.showBoneName:
                    showBN = False
        for x in self.graphicsView.scene().items():
            if x.type == "jointsItem":
                x.showBoneName = showBN
        self.graphicsView.scene().update()
    def callSkinWheels(self):
        if (skinWheels.chassisClastersSkin()):
            self.popUpMessage("success", "Wheels are skinned")
        else:
            self.popUpMessage("error", "Wheels wasn't skinned")
    def drawScene(self, scene, i, side):
        self.setWindowTitle(self.winName + 'Untitled*')
        self.IO.currentFile = False
        self.currentScene = self.graphicsView.scene()
        self.graphicsView.setScene(scene)
        for x in self.exclusionContainerLeftArray:
            if x.scrollAreaLayout.count() > 0:
                for y in range(x.scrollAreaLayout.count()):
                    x.scrollAreaLayout.itemAt(y).widget().close()
        for x in self.exclusionContainerRightArray:
            if x.scrollAreaLayout.count() > 0:
                for y in range(x.scrollAreaLayout.count()):
                    x.scrollAreaLayout.itemAt(y).widget().close()
        scene.clear()
        scene.createRotLocator()
        scene.setUpScene(side)
        try:
            self.hullDraw = drawMesh()
            self.hullDraw.setPen(QPen(scene.layersWidget.tanksMeshColor, .2, Qt.SolidLine))
            self.hullDraw.assignMesh(self.instance.hullData[i], "convex")
            self.hullDraw.layer = "Hull"
            self.hullDraw.type = "Hull"
            scene.addItem(self.hullDraw)
        except:
            pass
        try:
            self.suspensionDraw = drawSuspension(
                QPen(scene.layersWidget.chassisMeshColor, .1, Qt.SolidLine), self)
            self.suspensionDraw.assignMesh(self.instance.suspensionData[side][i], scene, "Chassis")
        except:
            pass
        try:
            self.trackDraw = drawMesh()
            self.trackDraw.layer = "Tracks"
            self.trackDraw.type = "Track"
            self.trackDraw.assignMesh(self.instance.tracksData[side][i], "full")
            self.trackDraw.setPen(QPen(scene.layersWidget.trackMeshColor, .1, Qt.SolidLine))
            scene.addItem(self.trackDraw)
            self.vertices = drawVertices()
            self.vertices.vertColor(216, 172, 37)
            self.vertices.assignMesh(self.instance.tracksData[side][i], scene, "Tracks")
        except:
            pass

        if side == 0:
            try:
                for x in self.instance.chassisLodsLeft[i]:
                    self.wheelsDraw = drawMesh()
                    self.wheelsDraw.type = "Wheels"
                    self.wheelsDraw.assignMesh(x, "convex")
                    self.wheelsDraw.layer = "Wheels"
                    self.wheelsDraw.setPen(QPen(scene.layersWidget.wheelsMeshColor, .5, Qt.SolidLine))
                    scene.addItem(self.wheelsDraw)
            except:
                pass

        if side == 1:
            try:
                for x in self.instance.chassisLodsRight[i]:
                    self.wheelsDraw = drawMesh()
                    self.wheelsDraw.assignMesh(x, "convex")
                    self.wheelsDraw.layer = "Wheels"
                    self.wheelsDraw.setPen(QPen(scene.layersWidget.wheelsMeshColor, .1, Qt.SolidLine))
                    scene.addItem(self.wheelsDraw)
            except:
                pass

        try:
            for x in self.instance.jointsData[side]:
                self.jointsDraw = jointsItem()
                self.jointsDraw.assignJoint(x)
                self.jointsDraw.setInPosition()
                scene.addItem(self.jointsDraw)
        except:
            pass

        try:
            for x in self.instance.vJointData:
                self.vJointDraw = vJointItem()
                self.vJointDraw.assignJoint(x)
                self.vJointDraw.setInPosition()
                scene.addItem(self.vJointDraw)
        except:
            print ("can't create joint data")
        try:
            for x in self.instance.tankJointData:
                self.tankJointDraw = jointsItem()
                self.tankJointDraw.assignJoint(x)
                self.tankJointDraw.setInPosition()
                scene.addItem(self.tankJointDraw)
        except:
            print ("can't create tankjoint data")
        self.graphicsView.setScene(self.currentScene)
    def setTool(self, number):
        for x in self.scenesLeftArray:
            x.setTool(number)
        for x in self.scenesRightArray:
            x.setTool(number)
    def createLocators(self):
        if self.graphicsView.scene().getSide() == 0:
            self.graphicsView.scene().createLocators(self.instance.tracksData[0][0])
        else:
            self.graphicsView.scene().createLocators(self.instance.tracksData[1][0])
    def callHardReset(self):
        packages = ['wg_menu']
        for i in sys.modules.keys()[:]:
            for package in packages:
                if i.startswith(package):
                    sys.modules[i].fmtCleanStart = True
        self.close()
    def createLocatorsCurve(self):
        if self.graphicsView.scene().getSide() == 0:
            self.graphicsView.scene().createLocatorsCurve(self.instance.tracksData[0][0])
        else:
            self.graphicsView.scene().createLocatorsCurve(self.instance.tracksData[1][0])
    def gatherNewInformation(self):
        sceneCondition = self.getSceneCondition()
        if sceneCondition == 'crash':
            self.skin_chassis_button.freeze = True
            self.skin_chassis_button.setEnabled(False)
            self.skin_wheels_button.freeze = True
            self.skin_wheels_button.setEnabled(False)

            for layerWidget in self.layersContainerLeftArray:
                layerWidget.tankLayer.visibleLayer.setChecked(True)
                layerWidget.chassisLayer.visibleLayer.setChecked(False)
            for layerWidget in self.layersContainerRightArray:
                layerWidget.tankLayer.visibleLayer.setChecked(True)
                layerWidget.chassisLayer.visibleLayer.setChecked(False)
        else:


            self.skin_chassis_button.freeze = False
            self.skin_chassis_button.setEnabled(True)
            self.skin_wheels_button.freeze = False
            self.skin_wheels_button.setEnabled(True)

            for layerWidget in self.layersContainerLeftArray:
                layerWidget.tankLayer.visibleLayer.setChecked(False)
                layerWidget.chassisLayer.visibleLayer.setChecked(True)
            for layerWidget in self.layersContainerRightArray:
                layerWidget.tankLayer.visibleLayer.setChecked(False)
                layerWidget.chassisLayer.visibleLayer.setChecked(True)
        self.popUpMessage('force', 'close', True)
        self.instance.clearData()
        self.instance.gatheringInformation()
        for x in range(len(self.scenesLeftArray)):
            self.drawScene(self.scenesLeftArray[x], x, 0)
        for x in range(len(self.scenesRightArray)):
            self.drawScene(self.scenesRightArray[x], x, 1)
        self.graphicsView.update()
        activeButton = None
        for ll in reversed(range(0, 5)):
            searchButton = "setLeftScene" + str(ll) + "_button"
            if getattr(self, searchButton).isActive:
                activeButton = getattr(self, searchButton)
            searchButton = "setRightScene" + str(ll) + "_button"
            if getattr(self, searchButton).isActive:
                activeButton = getattr(self, searchButton)
        for ll in reversed(range(0, 5)):
            searchButton = "setLeftScene" + str(ll) + "_button"
            getattr(self, searchButton).click()
            for x in self.layersContainerLeftArray[ll].layersArray:
                x.showHide()
            searchButton = "setRightScene" + str(ll) + "_button"
            getattr(self, searchButton).click()
            for x in self.layersContainerRightArray[ll].layersArray:
                x.showHide()
            activeButton.click()
        self.popUpMessage("success", "Gathered")
    def getSceneCondition(self):
        fileName = cmds.file(q=True, sn=True)
        condition = ''
        if 'crash' in fileName:
            condition = "crash"
        else:
            condition = "normal"
        return condition
    def skin(self, skinPart):
        condition = self.getSceneCondition()
        if condition == '':
            self.popUpMessage("error", "Not Normal, not Export!")
            return
        self.popUpMessage('force', 'close', True)
        if self.checkUnused():
            return
        def skinCurrentScene():
            self.skinTank.parseScene()
            if skinPart == "track":
                result = self.skinTank.skinTrack(condition)
            if skinPart == "chassis":
                result = self.skinTank.skinChassis()
        def moveToTempScene():
            if skinPart == "track":
                for x in self.graphicsView.scene().items():
                    if str(type(x)).find("drawMesh") != -1:
                        if x.type == "Track":
                            self.tempScene.addItem(x)
                    if str(type(x)).find("verticeItem") != -1:
                        if x.layer == "Tracks":
                            self.tempScene.addItem(x)
            if skinPart == "chassis":
                for x in self.graphicsView.scene().items():
                    if str(type(x)).find("suspensionItemGroup") != -1:
                        self.tempScene.addItem(x)
                    if str(type(x)).find("verticeItem") != -1:
                        if x.layer == "Chassis":
                            self.tempScene.addItem(x)
        def removeNodes(scene):
            nodesToClear = 1
            while nodesToClear != 0:
                nodesToClear = 0
                for node in scene.items():
                    if node.type in ["searchBoxItem", "searchCircleItem", "searchFreeFormItem"]:
                        scene.removeItem(node)
                        nodesToClear += 1
        def skinFromCurrent(scenesSide):

            for scene in scenesSide:
                if scene != self.graphicsView.scene():
                    self.flowingItems = []
                    for x in scene.items():
                        if skinPart == "track":
                            if str(type(x)).find("drawMesh") != -1:
                                if x.type == "Track":
                                    self.graphicsView.scene().addItem(x)
                                    self.flowingItems.append(x)
                            if str(type(x)).find("verticeItem") != -1:
                                if x.layer == "Tracks":
                                    self.graphicsView.scene().addItem(x)
                                    self.flowingItems.append(x)
                        if skinPart == "chassis":
                            if str(type(x)).find("suspensionItemGroup") != -1:
                                self.graphicsView.scene().addItem(x)
                                self.flowingItems.append(x)
                            if str(type(x)).find("verticeItem") != -1:
                                if x.layer == "Chassis":
                                    self.graphicsView.scene().addItem(x)
                                    self.flowingItems.append(x)

                    if scene.objectName()[3] != "4":
                        try:
                            skinCurrentScene()
                        except:
                            print
                            "cant skin from ", scene.objectName()
                    else:

                        skinWheels.skinTrackFourLod(condition)
                        pass
                    for x in self.flowingItems:
                        scene.addItem(x)

            for x in self.tempScene.items():
                self.graphicsView.scene().addItem(x)
        if not self.skinAllFromCurrent.isChecked():
            skinCurrentScene()
        else:
            skinCurrentScene()
            moveToTempScene()
            if not self.skinAllSides.isChecked():
                if self.lodsWatcher.currentToolName[0:4] == "left":
                    skinFromCurrent(self.scenesLeftArray)
                if self.lodsWatcher.currentToolName[0:4] == "righ":
                    skinFromCurrent(self.scenesRightArray)
            else:
                if self.lodsWatcher.currentToolName[0:4] == "left":
                    skinFromCurrent(self.scenesLeftArray)

                    for node in self.graphicsView.scene().items():
                        node.setSelected(True)
                    copyPaster = CopyPastClipBoard()
                    copyPaster.copyToClipBoard(self.graphicsView.scene())
                    for node in self.graphicsView.scene().items():
                        node.setSelected(False)

                    removeNodes(self.scenesRightArray[0])

                    copyPaster.pasteFromClipboard(self.scenesRightArray[0], QPointF(0, 0))

                    self.setRightScene0_button.click()

                    skinFromCurrent(self.scenesRightArray)
                    moveToTempScene()
                    skinFromCurrent(self.scenesRightArray)

                    removeNodes(self.scenesRightArray[0])

                    self.setLeftScene0_button.click()
                else:
                    skinFromCurrent(self.scenesRightArray)

                    for node in self.graphicsView.scene().items():
                        node.setSelected(True)
                    copyPaster = CopyPastClipBoard()
                    copyPaster.copyToClipBoard(self.graphicsView.scene())
                    for node in self.graphicsView.scene().items():
                        node.setSelected(False)

                    removeNodes(self.scenesLeftArray[0])

                    copyPaster.pasteFromClipboard(self.scenesLeftArray[0], QPointF(0, 0))

                    self.setLeftScene0_button.click()

                    skinFromCurrent(self.scenesLeftArray)
                    moveToTempScene()
                    skinFromCurrent(self.scenesLeftArray)

                    removeNodes(self.scenesLeftArray[0])

                    self.setRightScene0_button.click()
        self.popUpMessage("success", "Skined")
    def changeSelection(self):
        def changeState(state, gradEnable=True):
            self.skinGradientFactorSlider.setEnabled(state)
            self.gradientWeightCheckBox.setEnabled(state * gradEnable)
            if state:
                for x in self.graphicsView.scene().selectedItems():
                    if x.type in ['searchBoxItem', 'searchCircleItem', 'searchFreeFormItem']:
                        if x.gradient:


                            self.gradientText()
                            break
                        else:

                            self.gradientText()
                        if x.type == 'searchCircleItem':
                            if not x.weightDivider:
                                self.vBoneWeight.setEnabled(state)
                        if len(x.outputArray()) != 1:
                            self.vBoneWeight.setEnabled(state)
                        else:
                            self.vBoneWeight.setEnabled(False)
            else:


                self.gradientText()
            self.skinWeightLine.setEnabled(state)
        if len(self.graphicsView.scene().selectedItems()) > 0:
            self.item = self.graphicsView.scene().selectedItems()
            self.commandLine.setText(str(self.item))
            if self.graphicsView.scene().selectedItems()[0].type == 'searchBoxItem':
                self.skinWeightLine.setText(str(self.item[0].weight))
                self.vBoneWeight.setText(str(self.item[0].vBoneWeight))
                self.gradientWeightCheckBox.setChecked(self.item[0].gradient)
                changeState(True)
            if self.graphicsView.scene().selectedItems()[0].type == 'searchFreeFormItem':
                self.skinWeightLine.setText(str(self.item[0].weight))
                self.vBoneWeight.setText(str(self.item[0].vBoneWeight))
                self.gradientWeightCheckBox.setChecked(self.item[0].gradient)
                changeState(True, False)
            if self.graphicsView.scene().selectedItems()[0].type == 'searchCircleItem':
                self.sharedWeight.setEnabled(True)
                self.sharedWeight.setChecked(self.graphicsView.scene().selectedItems()[0].weightDivider)
                if self.graphicsView.scene().selectedItems()[0].weightDivider:
                    self.skinWeightLine.setText('')
                    self.vBoneWeight.setText('0')
                else:
                    self.skinWeightLine.setText(str(self.item[0].weight))
                    self.vBoneWeight.setText(str(self.item[0].vBoneWeight))
                    changeState(True, False)
        else:
            changeState(False)
            self.skinWeightLine.setText("")
            self.vBoneWeight.setText("")
            self.commandLine.setText("")
            self.sharedWeight.setEnabled(False)
            self.sharedWeight.setChecked(False)
    def gradientWeightState(self):
        if len(self.graphicsView.scene().selectedItems()) > 0:
            for x in self.graphicsView.scene().selectedItems():
                if x.type == 'searchBoxItem':
                    x.gradient = self.gradientWeightCheckBox.isChecked()
                    if x.gradient:
                        x.showArrow()

                        self.vBoneWeight.setEnabled(False)
                        self.vBoneWeight.setText('0')
                    else:
                        x.hideArrow()

                        self.vBoneWeight.setEnabled(True)
                        self.vBoneWeight.setText(str(x.vBoneWeight))
    def gradientSetWeight(self):
        for x in self.graphicsView.scene().selectedItems():
            if x.type == 'searchBoxItem' or x.type == 'searchFreeFormItem':
                if x.gradient:


                    print (x.weightGradient)
    def setWeight(self, *args):
        if args:

            if self:
                try:
                    if len(self.graphicsView.scene().selectedItems()) > 0:
                        for x in self.graphicsView.scene().selectedItems():
                            if x.type == 'searchBoxItem' or x.type == 'searchFreeFormItem':
                                self.checkNodesConnectionCount(x, args[0])
                                vWeight = float(self.vBoneWeight.text())
                                self.skinWeightLine.setText(args[0])
                                x.setWeight(float(args[0]), vWeight)
                                self.graphicsView.update()
                            if x.type == 'searchCircleItem':
                                if not x.weightDivider:
                                    self.checkNodesConnectionCount(x, args[0])
                                    vWeight = float(self.vBoneWeight.text())
                                    self.skinWeightLine.setText(args[0])
                                    x.setWeight(float(args[0]), vWeight)
                                    self.graphicsView.update()
                except:
                    print
                    "Start Exception"

            def doSet():
                if len(self.graphicsView.scene().selectedItems()) > 0:
                    for x in self.graphicsView.scene().selectedItems():
                        if x.type == 'searchBoxItem' or x.type == 'searchFreeFormItem':
                            self.checkNodesConnectionCount(x, args[0])
                            vWeight = float(self.vBoneWeight.text())
                            self.skinWeightLine.setText(args[0])
                            x.setWeight(float(args[0]), vWeight)
                            self.graphicsView.update()
                        if x.type == 'searchCircleItem':
                            if not x.weightDivider:
                                self.checkNodesConnectionCount(x, args[0])
                                vWeight = float(self.vBoneWeight.text())
                                self.skinWeightLine.setText(args[0])
                                x.setWeight(float(args[0]), vWeight)
                                self.graphicsView.update()
            return doSet
        if len(self.graphicsView.scene().selectedItems()) > 0:
            for x in self.graphicsView.scene().selectedItems():
                if x.type == 'searchBoxItem' or x.type == 'searchFreeFormItem' or x.type == 'searchCircleItem':
                    self.checkNodesConnectionCount(x, self.skinWeightLine.text())
                    x.setWeight(self.skinWeightLine.text(), self.vBoneWeight.text())
                    self.graphicsView.update()
    def checkNodesConnectionCount(self, node, inWeight):
        if len(node.outputArray()) == 1:
            vWeight = (1.0 - float(inWeight))
            self.vBoneWeight.setText(str(vWeight))
            self.vBoneWeight.setEnabled(False)
        else:
            self.vBoneWeight.setEnabled(True)
            vWeight = float(self.vBoneWeight.text())
            node.twoConnectionVWeight = vWeight
    def connectionsChage(self, node):
        if len(node.outputArray()) == 1:
            vWeight = (1.0 - node.weight)
            self.vBoneWeight.setText(str(vWeight))
            node.vBoneWeight = vWeight
            self.vBoneWeight.setEnabled(False)
            print("1 connection")
        else:
            vWeight = node.twoConnectionVWeight
            self.vBoneWeight.setText(str(vWeight))
            node.vBoneWeight = vWeight
            self.vBoneWeight.setEnabled(True)
            print("2 connection")
    def setWeightDivider(self):
        condition = self.sharedWeight.isChecked()
        if len(self.graphicsView.scene().selectedItems()) > 0:
            for x in self.graphicsView.scene().selectedItems():
                if x.type == 'searchCircleItem':
                    if not condition:
                        x.weightDividerOff()
                        self.skinWeightLine.setText(str(x.weight))
                        self.vBoneWeight.setText(str(x.vBoneWeight))
                        self.skinWeightLine.setEnabled(True)
                        self.vBoneWeight.setEnabled(True)
                    if condition:
                        x.weightDividerOn()
                        self.skinWeightLine.setText('')
                        self.vBoneWeight.setText('0')
                        self.skinWeightLine.setEnabled(False)
                        self.vBoneWeight.setEnabled(False)
    def setSkinGradientFactorLabel(self):
        self.skinGradientFactorLabel.setText(str(self.skinGradientFactorSlider.value()))
    def closeEvent(self, event):
        self.hide()
    def keyPressEvent(self, event):
        pass
    def popUpMessage(self, messageType="warning", message="text", forceClose=False):
        if forceClose:
            try:
                self.a.close()
                self.b.close()
                self.c.close()
                self.d.close()
            except:
                pass
        else:
            pos = self.graphicsView.pos()
            corner = self.mapToGlobal(QPoint(self.graphicsView.width(), self.graphicsView.height()))
            if messageType == "success":
                corner.setY(corner.y())
                try:
                    self.a.close()
                except:
                    pass
                self.a = CustomQt.Header(self, messageType, message)
                self.assignAnim(self.a, corner)
                self.a.show()
            if messageType == "warning":
                corner.setY(corner.y() - 60)
                try:
                    self.b.close()
                except:
                    pass
                self.b = CustomQt.Header(self, messageType, message)
                self.assignAnim(self.b, corner)
                self.b.show()
            if messageType == "processing":
                corner.setY(corner.y() - 120)
                try:
                    self.c.close()
                except:
                    pass
                self.c = CustomQt.Header(self, messageType, message)
                self.assignAnim(self.c, corner)
                self.c.show()
            if messageType == "error":
                corner.setY(corner.y() - 180)
                try:
                    self.d.close()
                except:
                    pass
                self.d = CustomQt.Header(self, messageType, message)
                self.assignAnim(self.d, corner)
                self.d.show()
    def assignAnim(self, widget, corner):
        widget.animate = QPropertyAnimation(widget, "geometry")
        widget.animate.setDuration(100);
        widget.animate.setStartValue(QRect(corner.x() + 200, corner.y() + 50, 200, 20));
        widget.animate.setEndValue(QRect(corner.x() - 150, corner.y() + 50, 200, 20));
        widget.animate.start()
        widget.animate2 = QPropertyAnimation(widget, "windowOpacity")
        widget.animate2.setDuration(7000);
        widget.animate2.setStartValue(1);
        widget.animate2.setEndValue(0);
        widget.animate2.start()
    def showUnused(self):
        self.graphicsView.scene().clearSelection()
        for x in self.graphicsView.scene().items():
            if x.type == 'searchBoxItem' or x.type == 'searchFreeFormItem':
                if not len(x.outputArray()):
                    x.setSelected(True)
            if x.type == 'searchCircleItem':
                if not len(x.outputArray()):
                    x.setSelected(True)
    def checkUnused(self):
        message = []
        def check(scenesArray):
            for x in scenesArray:
                for y in x.items():
                    if y.type == 'searchBoxItem' or y.type == 'searchFreeFormItem':
                        if not len(y.outputArray()):
                            message.append(str(x.objectName()))
                            break
                    if y.type == 'searchCircleItem':
                        if not len(y.outputArray()):
                            message.append(str(x.objectName()))
                            break
        check(self.scenesLeftArray)
        check(self.scenesRightArray)
        flattenText = "\n"
        for x in message:
            flattenText += "   scene " + x[4:] + ": " + x[0:4] + "\n"
        if len(message):
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Unused nodes")
            dialog.move(
                QPoint(self.pos()) + QPoint(self.rect().center().x() - 100, self.rect().center().y()))
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setIcon(QMessageBox.Warning)
            dialog.setText("Some nodes don't have connections:\n" + flattenText)
            dialog.exec_()
            return True
        return False
    def gradientText(self):
        print('OPS')



def reload_all_modules(module_name):
    for m in list(sys.modules):
        if module_name in m:
            print(m)
            del (sys.modules[m])

def main():
    print('OPS')
    reload_all_modules('full_metal_toolset')
    gui = mainWindow()
    gui.show()


if __name__ == '__main__':

    main()
