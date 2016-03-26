#!/usr/bin/python

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import loadUi
from TrajectoryDrawer import QPainting_tool
from random import randint

class MainWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # Package resources provider
        my_ui_path = "../MainWindow_Izar.ui"
        # Load and sets your ui file parameters
        loadUi(my_ui_path, self)
        
        self.MainWidget.setStyleSheet(""" #MainWidget { background-image: url("../resources/kimeo.png");}""")
        
        self.PageSelector.setCurrentIndex(0)
        self.isReduced = False
        self.ConnectButton()
        self.SetStyleButton()
        #self.EyeGif = QMovie("../resources/eye_test1/clintest.gif")
        self.FaceDisplay.setPixmap(QPixmap("../resources/eye_test1/clin1.png"))
        self.FaceDisplay.lower()
        #self.FaceDisplay.setMovie(self.EyeGif)
        #self.EyeGif.start()
        self.Brain_ = QTimer(self)
        self.connect(self.Brain_, SIGNAL("timeout()"),
                     self._slot_brain)
        self.Brain_.start(5000)
        self.TrajectoryDrawer = QPainting_tool()
        self.TrajectoryDrawer.resize(450,370)
        self.Trajectory_Layout.addWidget(self.TrajectoryDrawer)
        #self.PageSelector.setCurrentIndex(3)
        
    def _slot_brain(self):
        new_eye = randint(1,6)
        str_ = "../resources/eye_test1/clin" + str(new_eye) +".png"
        self.FaceDisplay.setPixmap(QPixmap(str_))
        self.update()
        
    def SetStyleButton(self):
        str_return_icon = """  QPushButton {background-image : url("../resources/back_icon.png");}"""
        str_ok_icon = """  QPushButton {background-image : url("../resources/ok_icon.png");}"""
        ##OK Button
        self.CF_ok_button.setStyleSheet(str_ok_icon)
        self.PF_ok_button.setStyleSheet(str_ok_icon)
        self.TD_ok_button.setStyleSheet(str_ok_icon)
        self.SM_ok_button.setStyleSheet(str_ok_icon)
        self.LM_ok_button.setStyleSheet(str_ok_icon)
        self.Com_ok_button.setStyleSheet(str_ok_icon)
        self.PM_ok_button.setStyleSheet(str_ok_icon)
        
        ##Return Button
        self.CF_return_button.setStyleSheet(str_return_icon)
        self.PF_return_button.setStyleSheet(str_return_icon)
        self.TD_return_button.setStyleSheet(str_return_icon)
        self.SM_return_button.setStyleSheet(str_return_icon)
        self.LM_return_button.setStyleSheet(str_return_icon)
        self.Com_return_button.setStyleSheet(str_return_icon)
        self.PM_return_button.setStyleSheet(str_return_icon)
        
        ##Other
        self.Light_button.setStyleSheet("""  QPushButton {background-image : url("../resources/Parameter_Icon.png");}""")
        self.CustomFace_button.setStyleSheet(""" QPushButton {background-image : url("../resources/Parameter_Icon.png");}""")
        self.Parameter_button.setStyleSheet(""" QPushButton {background-image : url("../resources/Parameter_Icon.png");}""")
        self.Sound_button.setStyleSheet(""" QPushButton{background-image : url("../resources/Parameter_Icon.png");}""")
        self.Trajectory_button.setStyleSheet(""" QPushButton {background-image : url("../resources/Draw_Icon.png");}""")
        self.Com_button.setStyleSheet(""" QPushButton {background-image : url("../resources/Parameter_Icon.png");}""")
        self.Battery.setPixmap(QPixmap("../resources/Icon_band/Battery_icon.png"))
        self.Connectivity.setPixmap(QPixmap("../resources/Icon_band/Connect_icon.png"))
        self.Sound_volume.setPixmap(QPixmap("../resources/Icon_band/Sound_icon.png"))
        
    def ConnectButton(self):
        '''
        '''
        self.connect(self.Reduce_button,SIGNAL("clicked()"),
                    self._slot_reduce_menu)
        
        self.connect(self.CustomFace_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(1))
        
        self.connect(self.Trajectory_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(3))
        
        self.connect(self.Light_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(4))
        
        self.connect(self.Sound_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(5))
        
        self.connect(self.Com_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(6))
        
        self.connect(self.Parameter_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(7))
        
        self.connect(self.CF_ok_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(2))
        
        self.connect(self.CF_return_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.PF_ok_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.PF_return_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(1))
        
        self.connect(self.TD_ok_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.TD_ok_button,SIGNAL("clicked()"),
                     lambda: self.TrajectoryDrawer.clear_draw())
        
        self.connect(self.TD_return_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.TD_return_button,SIGNAL("clicked()"),
                     lambda: self.TrajectoryDrawer.clear_draw())
        
        self.connect(self.SM_ok_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.SM_return_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.LM_ok_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.LM_return_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.Com_ok_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.Com_return_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.PM_ok_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.PM_return_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
    def _slot_reduce_menu(self):
        self.CustomFace_button.setVisible(self.isReduced)
        self.Trajectory_button.setVisible(self.isReduced)
        self.Light_button.setVisible(self.isReduced)
        self.Sound_button.setVisible(self.isReduced)
        self.Com_button.setVisible(self.isReduced)
        self.Parameter_button.setVisible(self.isReduced)
        self.isReduced = not(self.isReduced)
    