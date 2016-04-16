from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import loadUi
from TrajectoryDrawer import QPainting_tool
from Brain import *


repo = "/home/pi/Desktop/Kimeo/kimeo/IHM/"
#repo = "../"
class MainWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # Package resources provider
        my_ui_path = repo + "MainWindow.ui"
        # Load and sets your ui file parameters
        loadUi(my_ui_path, self)

        #self.MainWidget.setStyleSheet(" #MainWidget { background-color: black }")
        self.MainWidget.setStyleSheet(" #MainWidget { background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(223, 191, 255, 255), stop:1 rgba(0, 0, 0, 255)); }")
        
        
        self.PageSelector.setCurrentIndex(0)
        self.isReduced = False
        self.FirstOpening = False
        self.NotNeutral = False
        self.ConnectButton()
        self.SetStyleButton()
        self.MouthStyle = "CleanFace"
        self.EyeStyle = "CleanFace"
        self.startGifMovie = QMovie(repo + "resources/on-in.gif")
        self.startGifMovie2 = QMovie(repo + "resources/on-out.gif")
        self.EyeGif = QMovie("")
        self.MouthGif = QMovie("")
        self.startGif.setMovie(self.startGifMovie)
        self.main_screen.setVisible(False)
        self.Eye.setMovie(self.EyeGif)
        self.Mouth.setMovie(self.MouthGif)
        self.Brain_ = QTimer(self)
        self.Emotional = Brain()
        self.Opening_ = QTimer(self)
        self.Opening_.stop()
        self.playStart()
        self.connect(self.Opening_, SIGNAL("timeout()"),
                     self._slot_Openned)
        self.connect(self.Brain_, SIGNAL("timeout()"),
                     self._slot_brain)
        self.Brain_.start(3000)
        self.TrajectoryDrawer = QPainting_tool()
        self.TrajectoryDrawer.resize(540,380)
        self.Trajectory_Layout.addWidget(self.TrajectoryDrawer)
        self.TrajectoryDrawer.SetLabel(self.Countdown)
        self.connect(self.close_button,SIGNAL("clicked()"),
		     self.close)
        

    def mousePressEvent(self, event):
        if(self.TrajectoryDrawer.ExecuteOn == True):
            self.TrajectoryDrawer.StopTrajectory()
           
    def playStart(self):
        self.startGif.setVisible(True)
        self.startGifMovie.setSpeed(70)
        self.startGifMovie.start()
        self.Opening_.start(2500)
    
    def _slot_Openned(self):
        self.Opening_.stop()
        if(self.FirstOpening):
            self.setFace()
            self.startGif.setVisible(False)
            self.main_screen.setVisible(True)
        else:
            self.startGif.setMovie(self.startGifMovie2)
            self.FirstOpening = True
            self.startGifMovie2.setSpeed(70)
            self.startGifMovie2.start()
            self.Opening_.start(2500)
            
        
    def _slot_brain(self):
        self.Brain_.stop()
        if(self.NotNeutral == True):
            self.NotNeutral = False
            self.MouthGif = QMovie(self.Emotional.Anim.MouthAnim.TN)
            self.EyeGif = QMovie(self.Emotional.Anim.EyeAnim.TN)
            self.EyeGif.setScaledSize(QSize(520,165))
            self.MouthGif.setScaledSize(QSize(340,120))
            self.Eye.setMovie(self.EyeGif)
            self.Mouth.setMovie(self.MouthGif)
            self.EyeGif.start()
            self.MouthGif.start()
            self.Brain_.start(1000)
        else:
            self.NotNeutral = True
            self.Emotional.RandomState()
            self.MouthGif = QMovie(self.Emotional.Anim.MouthAnim.FN)
            self.EyeGif = QMovie(self.Emotional.Anim.EyeAnim.FN)
            self.EyeGif.setScaledSize(QSize(520,165))
            self.MouthGif.setScaledSize(QSize(340,120))
            self.Eye.setMovie(self.EyeGif)
            self.Mouth.setMovie(self.MouthGif)
            self.EyeGif.start()
            self.MouthGif.start()
            self.Brain_.start(3000)
        
        self.update()
        
    def _animation_slot(self):
        print("test")
        
    def SetStyleButton(self):
        str_return_icon = "  QPushButton {background-image : url(\"" + repo + "resources/back_arrow.png\");}"
        str_ok_icon = "  QPushButton {background-image : url(\"" + repo + "resources/grospicto-valider.png\");}"
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
        '''
        self.Light_button.setStyleSheet(" QPushButton {background-image : url(\"" + repo + "resources/grospicto-light.png\");}")
        self.CustomFace_button.setStyleSheet(" QPushButton {background-image : url(\"" + repo + "resources/grospicto-face.png\");}")
        self.Parameter_button.setStyleSheet(" QPushButton {background-image : url(\"" + repo + "resources/grospicto-presets.png\");}")
        self.Sound_button.setStyleSheet(" QPushButton{background-image : url(\"" + repo + "resources/grosoicto-musique.png\");}")
        self.Trajectory_button.setStyleSheet(" QPushButton {background-image : url(\"" + repo + "resources/grospicto-trajectoire.png\");}")
        self.Com_button.setStyleSheet(" QPushButton {background-image : url(\"" + repo + "resources/grospicto-message.png\");}")
        '''
        pix  = QPixmap(repo + "resources/grospicto-light.png");
        icon = QIcon(pix);
        self.Light_button.setIcon(icon)
        self.Light_button.setIconSize(pix.size())
        
        pix  = QPixmap(repo + "resources/grospicto-face.png");
        icon = QIcon(pix);
        self.CustomFace_button.setIcon(icon)
        self.CustomFace_button.setIconSize(pix.size())
        
        pix  = QPixmap(repo + "resources/grospicto-presets.png");
        icon = QIcon(pix);
        self.Parameter_button.setIcon(icon)
        self.Parameter_button.setIconSize(pix.size())

        pix  = QPixmap(repo + "resources/grospicto-musique.png");
        icon = QIcon(pix);
        self.Sound_button.setIcon(icon)
        self.Sound_button.setIconSize(pix.size())
        
        pix  = QPixmap(repo + "resources/grospicto-trajectoire.png");
        icon = QIcon(pix);
        self.Trajectory_button.setIcon(icon)
        self.Trajectory_button.setIconSize(pix.size())
        
        pix  = QPixmap(repo + "resources/grospicto-message.png");
        icon = QIcon(pix);
        self.Com_button.setIcon(icon)
        self.Com_button.setIconSize(pix.size())

        self.Battery.setPixmap(QPixmap(repo +"resources/Icon_band/petitpicto-batterie.png"))
        self.Connectivity.setPixmap(QPixmap(repo +"resources/Icon_band/Connect_icon.png"))
        self.Sound_volume.setPixmap(QPixmap(repo +"resources/Icon_band/petitpicto-sound.png"))
        
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
                     lambda: self.TrajectoryDrawer.ExecuteTrajectory())
        
        self.connect(self.TD_return_button,SIGNAL("clicked()"),
                     lambda: self.PageSelector.setCurrentIndex(0))
        
        self.connect(self.TD_return_button,SIGNAL("clicked()"),
                     lambda: self.TrajectoryDrawer.StopTrajectory())
        
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
        
    def setFace(self):
        str_mouth = (repo + "resources/FaceGif/" + self.MouthStyle + "/whiteMouth-happy.gif")
        str_eye = (repo + "resources/FaceGif/" + self.EyeStyle + "/glassesEyes-neutral.gif")
        self.MouthGif = QMovie(str_mouth)
        self.EyeGif = QMovie(str_eye)
        self.EyeGif.setScaledSize(QSize(520,165))
        self.MouthGif.setScaledSize(QSize(340,120))
        self.Eye.setMovie(self.EyeGif)
        self.Mouth.setMovie(self.MouthGif)
        self.EyeGif.start()
        self.MouthGif.start()
        
    def _slot_reduce_menu(self):
        self.CustomFace_button.setVisible(self.isReduced)
        self.Trajectory_button.setVisible(self.isReduced)
        self.Light_button.setVisible(self.isReduced)
        self.Sound_button.setVisible(self.isReduced)
        self.Com_button.setVisible(self.isReduced)
        self.Parameter_button.setVisible(self.isReduced)
        self.isReduced = not(self.isReduced)
    
