from PyQt4.QtGui import *
from PyQt4.QtCore import *
import math
import pypot.dynamixel

repo = "/home/pi/Desktop/Kimeo/kimeo/IHM/"


sizeW = 540.0  
sizeH = 380.0
sizeRobot = 25.0
Threshold = 40.0
OffsetX = 7.0
OffsetY = 0.0
SpeedLimit_linear = 0.8
SpeedMotor_limit = 500
OmegaLimit_linear = 100.0
PixelToReal = 0.005
coeff_dis = 30
acc_limit = 100.0
dist_thres = 2.0

def ConvertTrajectory(Trajectory = []):
    RobotTrajData = []
    x_ = (-Trajectory[1][1] + Trajectory[0][1])*PixelToReal
    y_ = (-Trajectory[1][0] + Trajectory[0][0])*PixelToReal
    theta = math.degrees(math.atan2(y_,x_))
    last_theta = theta
    RobotTrajData.append([0.0, theta])
    for i_pt in range(1,len(Trajectory)):
        x_ = (-Trajectory[i_pt][1] + Trajectory[i_pt-1][1])*PixelToReal
        y_ = (-Trajectory[i_pt][0] + Trajectory[i_pt-1][0])*PixelToReal
        d_ = math.sqrt(x_*x_ + y_*y_) 
        theta = math.degrees(math.atan2(y_,x_))
        dtheta = theta - last_theta
        if(math.fabs(dtheta)>180.0): ## 
                if(dtheta > 0.0): #targetAngle > actAngle
                    dtheta = dtheta - 360.0
                else: #targetAngle < actAngle
                    dtheta = 360.0 + dtheta
        last_theta = theta
        RobotTrajData.append([d_,dtheta])
        
    return RobotTrajData

def Curve(Pt1 = [0.0,0.0], Pt2 = [0.0,0.0], Pt3 = [0.0,0.0], Pt4 = [0.0,0.0]):
    global last_pt
    curve_bezier = []
    for i_pt in range(0,(3*coeff_dis +1)):
        t = float(i_pt)/(3*coeff_dis)
        x_curve = (1-t)*(1-t)*(1-t)*(Pt1[0]) +3*t*(1-t)*(1-t)*Pt2[0]+3*t*t*(1-t)*Pt3[0]+t*t*t*Pt4[0]
        y_curve = (1-t)*(1-t)*(1-t)*(Pt1[1]) +3*t*(1-t)*(1-t)*Pt2[1]+3*t*t*(1-t)*Pt3[1]+t*t*t*Pt4[1]
        curve_bezier.append([x_curve,y_curve])
    return curve_bezier

class RobotController(QWidget):
    
    update_robot = pyqtSignal()
    
    def __init__(self):
        QWidget.__init__(self)
        self.MotorRight = None
        self.MotorLeft = None
        self.MotorRight_py = None ##11
        self.MotorLeft_py = None ##7
        self.dxl_io = None
        self.LastPoint = False
        self.MotorConnected = False
        self.CmdList = []
        self.ActualPosition = 0
        self.Pose = [0.0,0.0,0.0]
        self.GearRatio = 1.0
        self.DWheel = 0.40 
        self.RGear = 0.12
        self.RobotTrajectoryData = []
        self.Control = QTimer(self)
        self.connect(self.Control, SIGNAL("timeout()"),
                     self.SendNextCmd)

        
    def setTrajectoryData(self, data):
        self.LastPoint = False
        self.RobotTrajectoryData = data
        self.ActualPosition = 0
        self.Pose = [0.0,0.0,0.0]
        
    def RobotStop(self):
        self.Control.stop()
        self.MotorLeft = 0.0
        self.MotorRight = 0.0
        self.SetMotorSpeed()
            
    def SetMotorSpeed(self):
        if(self.MotorConnected):
            self.dxl_io.set_moving_speed({self.MotorRight_py:self.MotorRight})
            self.dxl_io.set_moving_speed({self.MotorLeft_py:self.MotorLeft})
    
    def ConnectMotor(self, IndexRight, IndexLeft, dxl_link):
        self.MotorConnected = True
        self.MotorRight_py = IndexRight
        self.MotorLeft_py = IndexLeft
        self.dxl_io = dxl_link
    
    def ComputeTargetSpeed(self):
        self.CmdList = []
        for i_pt in range(0, len(self.RobotTrajectoryData)):  
            if(i_pt == len(self.RobotTrajectoryData)):
                self.CmdList.append(0.0,0.0,0.001)
                return
            if(i_pt == 0):
                t_ = 3.0
                Omega = self.RobotTrajectoryData[i_pt][1]/t_
                Cmd = self.ComputeRobotCmd(0.0, Omega)
            else:
                t_ = self.RobotTrajectoryData[i_pt][0]/SpeedLimit_linear
                Omega = self.RobotTrajectoryData[i_pt][1]/t_
                Cmd = self.ComputeRobotCmd(SpeedLimit_linear, Omega)
                if(math.fabs(Omega) > OmegaLimit_linear):
                    t_ = math.fabs(self.RobotTrajectoryData[i_pt][1])/OmegaLimit_linear
                    Speed_linear = self.RobotTrajectoryData[i_pt][0]/t_
                    if(Omega>0):
                        Cmd = self.ComputeRobotCmd(Speed_linear, OmegaLimit_linear)
                    else:        
                        Cmd = self.ComputeRobotCmd(Speed_linear, -OmegaLimit_linear)
            self.CmdList.append([Cmd[0],Cmd[1],t_])
            
        self.SmoothSpeed()
                                                  
    def SmoothSpeed(self):
        NewCmdList = []
        last_speed = [0.0,0.0]
        for i_pt in range(0, len(self.CmdList)):
            t_ = self.CmdList[i_pt][2]
            Cmd0_init = self.CmdList[i_pt][0]
            Cmd1_init = self.CmdList[i_pt][1]
            theta0 = Cmd0_init*t_
            theta1 = Cmd1_init*t_
            acc0 = 2*(Cmd0_init-last_speed[0])/t_
            acc1 = 2*(Cmd1_init-last_speed[1])/t_
            
            if(math.fabs(acc0) > acc_limit):
                if(acc0 > 0):
                    acc0 = acc_limit
                else:
                    acc0 = -acc_limit
            
            if(math.fabs(acc1) > acc_limit):
                if(acc1 > 0):
                    acc1 = acc_limit
                else:
                    acc1 = -acc_limit
            
            t0 = self.FindTime(acc0, last_speed[0], theta0)
            t1 = self.FindTime(acc1, last_speed[1], theta1)
            if(t0 > t1):
                t_ = t0
            else:
                t_ = t1
            
            Cmd0 = theta0/t_
            Cmd1 = theta1/t_
            
            if(math.fabs(Cmd0) > SpeedMotor_limit):
                t0 = math.fabs(theta0)/SpeedMotor_limit
            if(math.fabs(Cmd1) > SpeedMotor_limit):
                t1 = math.fabs(theta1)/SpeedMotor_limit
            if(t0 > t1):
                t_ = t0
            else:
                t_ = t1
                
            Cmd0 = theta0/t_
            Cmd1 = theta1/t_
            last_speed = [Cmd0, Cmd1]
            NewCmdList.append([Cmd0, Cmd1,t_])
            
        self.CmdList = NewCmdList
                        
    def FindTime(self, acc, speed, theta):
        a_ = 0.5*acc
        b_ = speed
        c_ = -theta
        delta_ = b_*b_ - 4.0*a_*c_
        if(delta_ == 0.0):
            t_ = -b_/(2.0*a_)
        else:
            t1_ = (-b_ - math.sqrt(delta_))/(2.0*a_)
            t2_ = (-b_ + math.sqrt(delta_))/(2.0*a_)
            
            if(t1_ >0.0 and t2_>0.0):
                if(t1_ < t2_):
                    t_ = t1_
                else:
                    t_ = t2_
                    
            elif(t1_ >0.0):
                t_ = t1_
            else:
                t_ = t2_
            
        return t_
                   
    def SendNextCmd(self):
        self.Control.stop()
        if(self.LastPoint == True):
            self.MotorRight = 0.0
            self.MotorLeft = 0.0
            self.SetMotorSpeed()
            return
        if(self.ActualPosition +1 == len(self.CmdList)):
            self.LastPoint = True
        self.MotorRight = self.CmdList[self.ActualPosition][0]
        self.MotorLeft = self.CmdList[self.ActualPosition][1]
        self.ComputeRobotPose(self.CmdList[self.ActualPosition][2])
        self.Control.start(self.CmdList[self.ActualPosition][2]*1000.0)
        self.SetMotorSpeed()
        self.ActualPosition = self.ActualPosition+1
            
    def ComputeRobotCmd(self,V_linear, Omega):
        ## Compute Speed of each wheel 
        VWheelRight = V_linear + math.radians(Omega)*(self.DWheel/2) ##Speed of the Right Wheel
        VWheelLeft = V_linear - math.radians(Omega)*(self.DWheel/2) ##Speed of the Right Wheel
        ##FRom Wheel to motor cmd
        CmdMotorRight = math.degrees((VWheelRight/self.RGear)/self.GearRatio) ##Cmd in degree of the Right Motor
        CmdMotorLeft = math.degrees((VWheelLeft/self.RGear)/self.GearRatio) ##Cmd in degree of the Left Motor

        return [CmdMotorRight, CmdMotorLeft]
    
    def ComputeRobotPose(self,time):
        VLeft =  math.radians(self.MotorLeft)*self.GearRatio*self.RGear
        VRight = math.radians(self.MotorRight)*self.GearRatio*self.RGear
        x_ = self.Pose[0]
        y_ = self.Pose[1]
        theta_ = self.Pose[2]
        d = ((VLeft + VRight)/2)*time
        dtheta = ((VRight - VLeft)/(self.DWheel))*time
        
        theta_ = theta_ + math.degrees(dtheta)
        x_ = x_ + d*math.cos(math.radians(theta_))
        y_ = y_ + d*math.sin(math.radians(theta_))
        
        self.Pose = [x_, y_, theta_]
        self.update_robot.emit()

class QPainting_tool(QGraphicsView):
    
    def __init__(self):
        super(QPainting_tool, self).__init__()
        self.setMouseTracking(True)
        self.Scene_ = QGraphicsScene()
        self.clicked = False
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent")
        self.setScene(self.Scene_)
        self.setSceneRect(0.0,0.0,sizeW,sizeH)
        self.Trajectory = []
        self.Robot = RobotController()
        self.Robot.update_robot.connect(self.update_robot_pose)
        self.clear_draw()
        self.ExecuteOn = False
        self.Counter = None
        self.Count = 6
        self.Timer_ = QTimer(self)
        self.connect(self.Timer_,SIGNAL("timeout()"),
                     self.Countdown)
        
    def mouseMoveEvent(self, event):
        if(self.clicked):          
            x_line = event.x() - self.LastWaypoint[0] - OffsetX
            y_line = event.y() - self.LastWaypoint[1] - OffsetY
            self.Scene_.removeItem(self.Line)
            self.Line = QGraphicsLineItem(0, 0,x_line, y_line)
            self.Line.setPen(QPen(Qt.green,3))
            mat = QTransform()
            mat.translate(self.LastWaypoint[0],self.LastWaypoint[1])
            self.Line.setTransform(mat)
            self.Scene_.addItem(self.Line)
            self.X_pos = event.x() - OffsetX
            self.Y_pos = event.y() - OffsetY
            self.Converted = False
            #print 'mouse : x = %d, y=%d' % (self.X_pos, self.Y_pos)
            delta_x = self.X_pos - self.LastWaypoint[0]
            delta_y = self.Y_pos - self.LastWaypoint[1]
            distance_ = math.sqrt(delta_x * delta_x + delta_y * delta_y)
            if(distance_ > Threshold):
                self.AddWaypoint()
                
            self.update()
    
    def clear_draw(self):
        self.Scene_.clear()
        self.Robot_pict = QGraphicsPixmapItem(QPixmap(repo + "resources/robottraj.png"))
        mat = QTransform()
        mat.translate(sizeW/2 - sizeRobot, sizeH/2 - sizeRobot)
        self.Robot_pict.setTransform(mat)
        self.Scene_.addItem(self.Robot_pict)
        self.WaypointList = []
        self.LastWaypoint = [sizeW/2, sizeH/2]
        self.WaypointList.append(self.LastWaypoint)
        self.Line = QGraphicsLineItem(0, 0, 0, 0)
        mat = QTransform()
        mat.translate(self.LastWaypoint[0],self.LastWaypoint[1])
        self.Scene_.addItem(self.Line)
        self.Line.setTransform(mat)
        self.X_pos = 0.0
        self.Y_pos = 0.0
        self.Converted = False      
        self.update()
        
    
    def mousePressEvent(self, event):
        if(self.ExecuteOn == True):
            self.StopTrajectory()
            return
        if(event.buttons() == Qt.LeftButton):
            self.clicked = True
        
    
    def mouseReleaseEvent(self, event):
        if(self.clicked == True):
            self.clicked = False
            x_line = event.x() - self.LastWaypoint[0] - OffsetX
            y_line = event.y() - self.LastWaypoint[1] - OffsetY
            self.Scene_.removeItem(self.Line)
            self.Line = QGraphicsLineItem(0, 0,x_line, y_line)
            self.Line.setPen(QPen(Qt.green,3))
            mat = QTransform()
            mat.translate(self.LastWaypoint[0],self.LastWaypoint[1])
            self.Line.setTransform(mat)
            self.Scene_.addItem(self.Line)
            self.X_pos = event.x() - OffsetX
            self.Y_pos = event.y() - OffsetY
            #print 'mouse : x = %d, y=%d' % (self.X_pos, self.Y_pos)
            self.AddWaypoint()
            self.update()       
        
    def AddWaypoint(self):
        x_line = self.X_pos - self.LastWaypoint[0]
        y_line = self.Y_pos - self.LastWaypoint[1]
        line_ = QGraphicsLineItem(0, 0,x_line, y_line)
        line_.setPen(QPen(Qt.green,3))
        mat = QTransform()
        mat.translate(self.LastWaypoint[0],self.LastWaypoint[1])
        line_.setTransform(mat)
        self.Scene_.addItem(line_)
        self.update()
        self.LastWaypoint = [self.X_pos, self.Y_pos]
        X_ = self.X_pos
        Y_ = self.Y_pos
        self.WaypointList.append([X_, Y_])
        
    def getTrajectory(self):
        TrajPt = []
        for i_pt in range(len(self.WaypointList)):
            TrajPt.append([(self.WaypointList[i_pt][0] - self.WaypointList[0][0])/800, (self.WaypointList[i_pt][1] - self.WaypointList[0][1])/800])
        
        return TrajPt  
    
    def ConvertToCurve(self):
        trajcurve = []
        if(len(self.WaypointList) == 1):
            return
        elif(len(self.WaypointList) == 2):
            for i_pt in range(0,coeff_dis+1):
                t = float(i_pt)/coeff_dis
                x_curve = (1-t)*(self.WaypointList[0][0]) +t*(self.WaypointList[1][0])
                y_curve = (1-t)*(self.WaypointList[0][1]) +t*(self.WaypointList[1][1])
                trajcurve.append([x_curve,y_curve])
        elif(len(self.WaypointList) == 3):
            for i_pt in range(0,2*coeff_dis+1):
                t = float(i_pt)/(2*coeff_dis)
                x_curve = (1-t)*(1-t)*(self.WaypointList[0][0]) +t*(1-t)*(self.WaypointList[1][0]) +t*t*(self.WaypointList[2][0]) 
                y_curve = (1-t)*(1-t)*(self.WaypointList[0][1]) +t*(1-t)*(self.WaypointList[1][1]) +t*t*(self.WaypointList[2][1])
                trajcurve.append([x_curve,y_curve])
        elif(len(self.WaypointList) == 4):
            
            start_pt = self.WaypointList[0]
            mid_pt1 = self.WaypointList[1]
            mid_pt2 = self.WaypointList[2]
            last_pt = self.WaypointList[3]
            curve = Curve(start_pt, mid_pt1, mid_pt2,last_pt)
            for i_pt2 in range(len(curve)):
                trajcurve.append(curve[i_pt2])
        else: #5 or more pts
            start_pt = self.WaypointList[0]
            mid_pt1 = self.WaypointList[1]
            mid_pt2 = self.WaypointList[2]
            last_pt =[0.0,0.0]
            last_pt[0] = (self.WaypointList[3][0] + self.WaypointList[2][0])/2
            last_pt[1] = (self.WaypointList[3][1] + self.WaypointList[2][1])/2  
            curve = Curve(start_pt, mid_pt1, mid_pt2,last_pt)
            for i_pt2 in range(len(curve)-1):
                trajcurve.append(curve[i_pt2])
            for i_pt in range(3,len(self.WaypointList)-2,2):
                start_pt[0] = (self.WaypointList[i_pt][0] + self.WaypointList[i_pt-1][0])/2
                start_pt[1] = (self.WaypointList[i_pt][1] + self.WaypointList[i_pt-1][1])/2   
                mid_pt1 = self.WaypointList[i_pt]
                mid_pt2 = self.WaypointList[i_pt+1]
                last_pt[0] = (self.WaypointList[i_pt+2][0] + self.WaypointList[i_pt+1][0])/2
                last_pt[1] = (self.WaypointList[i_pt+2][1] + self.WaypointList[i_pt+1][1])/2  
                curve = Curve(start_pt, mid_pt1, mid_pt2,last_pt)
                for i_pt2 in range(len(curve)-1):
                    trajcurve.append(curve[i_pt2])
                
                if((len(self.WaypointList)-i_pt) == 1): ## 2pt
                    pt1 = self.WaypointList[len(self.WaypointList)-1]
                    pt2 = self.WaypointList[len(self.WaypointList)]
                    for i_pt2 in range(0,coeff_dis+1):
                        t = float(i_pt2)/coeff_dis
                        x_curve = (1-t)*(pt1[0]) +t*(pt2[0])
                        y_curve = (1-t)*(pt1[1]) +t*(pt2[1])
                        trajcurve.append([x_curve,y_curve])
        
        trajcurve = self.CheckTraj(trajcurve)
        
        self.Trajectory = trajcurve
        last = [self.Trajectory[0][0],self.Trajectory[0][1]]
        for i_pt in range(1,len(self.Trajectory)):
            line_ = QGraphicsLineItem(0, 0,(self.Trajectory[i_pt][0]-self.Trajectory[i_pt-1][0])
                                      , (self.Trajectory[i_pt][1]-self.Trajectory[i_pt-1][1]))
            mat = QTransform()
            mat.translate(last[0],last[1])
            line_.setTransform(mat)
            line_.setPen(QPen(Qt.black,3,Qt.DashLine))
            self.Scene_.addItem(line_)
            self.update()
            last = [self.Trajectory[i_pt][0], self.Trajectory[i_pt][1]]
            
    def CheckTraj(self, data):
        checked = []
        last_data = data[0]
        checked.append(data[0])
        for i_pt in range(1,len(data)):
            x_ = data[i_pt][0] - last_data[0] 
            y_ = data[i_pt][1] - last_data[1]
            dist = math.sqrt(x_*x_ + y_*y_)
            if(dist > dist_thres):
                checked.append(data[i_pt])
                last_data = data[i_pt]
            
        return checked
    
    def Countdown(self):
        self.Timer_.stop()
        if(self.Count >0):
            self.Count = self.Count - 1
            #self.Counter.setPixmap(QPixmap(repo + "resources/Counter/"+str(self.Count)+".png"))
            self.Counter.setText(str(self.Count))
            self.Counter.setVisible(True)
            self.Timer_.start(1000)
        if(self.Count == 0):
            self.Timer_.stop()
            self.Count = 6
            if(self.ExecuteOn == True):
                self.Counter.setVisible(False)
                self.Robot.SendNextCmd()
    
    def SetLabel(self, Label):
        self.Counter = Label
        self.Counter.setVisible(False)
            
    def ExecuteTrajectory(self):
        if(self.Converted == True):
            self.ExecuteOn = True
            Robot_Traj = ConvertTrajectory(self.Trajectory)
            self.Robot.setTrajectoryData(Robot_Traj)
            self.Robot.ComputeTargetSpeed()
            self.Countdown()
            
        if(self.Converted == False):
            self.ConvertToCurve()
            self.Converted = True
    
    def SendTrajectory(self):
        return self.WaypointList
        
    
    def StopTrajectory(self):
        self.Robot.RobotStop()
        self.clear_draw()
        self.ExecuteOn = False
        self.Count = 6
        self.Counter.setVisible(False)
        self.Timer_.stop()
        
    def update_robot_pose(self):
        x_pixel = -self.Robot.Pose[1]/PixelToReal 
        y_pixel = -self.Robot.Pose[0]/PixelToReal
        self.Robot_pict.setZValue(10)
        mat = QTransform()
        #
        mat.translate(sizeW/2 + x_pixel, sizeH/2 + y_pixel)
        mat.rotate(-self.Robot.Pose[2])
        mat.translate(-sizeRobot,-sizeRobot)
        self.Robot_pict.setTransform(mat)
        self.update()
            