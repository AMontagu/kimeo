#!/usr/bin/env python
from python_qt_binding import loadUi
from python_qt_binding.QtGui import QApplication
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#from python_qt_binding.QtGui import *
#from python_qt_binding.QtCore import *


import sys

try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time
import math
SizeScreenW = 740.0
SizeScreenH = 470.0
sizeW = 700.0  
sizeH = 400.0
sizeRobot = 15.0
Threshold = 10.0
RWheel = 200.0/1000.0
LWheel = 400.0/1000.0
OmegaMax = 0.60;
OffsetX = 0.0
OffsetY = 0.0

#def choose(i,n):
    #return factorial(n)/(factorial(i)*factorial(n-i))

def distance(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def further(a,b,d):
    return (distance(a,b)> d)

def length(l):
    d = 0
    for i in range(len(l)-1):
        d += distance(l[i],l[i+1])
    return d

class BCurve(object):
    
    def __init__(self):
        self.nodes = []

    def add_node(self,p):
        if type(p[0]) == list:
            self.nodes.extend(p)
        else:
            self.nodes.append(p)
        return self

    def path_len(self):
        return int(len(self.nodes)/3)

    def length(self,n = 10):
        """
        return an approximate length of the Bezier curve using n points for each bezier curve
        n is an integer
        """
        nb = n*self.path_len()
        step = 1.0/n
        d = 0
        o = self.nodes[0]
        for i in range(nb):
            e = self.get((i+1)*step)
            d += distance(o,e)
            o = e
        return d

    def get(self,t):
        """
        Return the t parameter point in the bezier curve
        0 <= t <= 1 first Bezier curve
        1 < t < 2 second Bezier curve
        ...
        n-1 < t <= n last Bezier curve

        Example:

        >>> p = BCurve().add_node([[4,3],[4,1],[3,0],[1,0]])
        >>> m = p.get(0.5)
        >>> print(m)
        [3.25,0.75]
        """
        if t > self.path_len():
            raise ValueError('{val} exceeds max : {vmax}'.format(val = t, vmax = self.path_len()))
        else:
            p = int(t)
            if p == self.path_len():
                p -= 1
            t -= p

            x = 0
            y = 0
            for i in range(4):
                ##c = choose(i,3)*t**i*(1-t)**(3-i)
                x += c*self.nodes[3*p+i][0]
                y += c*self.nodes[3*p+i][1]
            return [x,y]

    def from_lines(self,l,start):
        
        try:
            self.nodes = []
            self.add_node(l[start])
            d = length(l[start:])
            if start:
                k = distance(l[start],l[start-1])
                self.add_node([l[start][0]+(l[start][0]-l[start-1][0])*d/(2*k),l[start][1]+(l[start][1]-l[start-1][1])*d/(2*k)])
            else:
                k = distance(l[0],l[1])
                self.add_node([l[0][0]+(l[1][0]-l[0][0])*d/(2*k),l[0][1]+(l[1][1]-l[0][1])*d/(2*k)])
            k = distance(l[-2],l[-1])
            self.add_node([l[-1][0]+(l[-2][0]-l[-1][0])*d/(2*k),l[-1][1]+(l[-2][1]-l[-1][1])*d/(2*k)])
            self.add_node(l[-1])
        except:
            self.nodes = []

    def draw(self,canvas):
        ## procedure rajoutee pour le trace des courbes de bezier. peut etre inutile sur qt
        pas = 20 ## nombre de segments pour approximer la courbe de bezier
        if len(self.nodes):
            p = self.get(0)
            for i in range(pas*self.path_len()):
                q = self.get((i+1)/pas)
                canvas.create_line(p[0],p[1],q[0],q[1],fill='lightgray',width=2)
                p = q[:]

##            for i in range(len(self.nodes)-1):
##                canvas.create_line(self.nodes[i][0],self.nodes[i][1],self.nodes[i+1][0],self.nodes[i+1][1],fill='blue')
##
##            i = 0
##            while i < len(self.nodes):
##                canvas.create_rectangle(self.nodes[i][0]-1,self.nodes[i][1]-1,self.nodes[i][0]+1,self.nodes[i][1]+1,fill='blue')
##                i+=3
    

    def distance(self,l):
        pas = 32 ## nombre de pas pour la courbe de bezier pour calcul rapide de la distance entre courbe de bezier et ligne polygonale

        btol = [self.get(0)]
        for i in range(pas*self.path_len()):
                btol.append(self.get((i+1)/pas))
        d = 0
        xj = [0,0]
        for j in range(len(l)):
            xi = -1
            dmin = 1000000
            for i in range(len(btol)):
                dd = distance(btol[i],l[j])
                if dd < dmin:
                    dmin = dd
                    xi = i
            if dmin > d:
                d = dmin
                xj = [j,xi]
        return d

    def append(self,curve):
        if self.nodes:
            self.nodes.extend(curve.nodes[1:])
        else:
            self.nodes.extend(curve.nodes[:])

class QPainting_tool(QGraphicsView):
    def __init__(self):
        super(QPainting_tool, self).__init__()
        self.setMouseTracking(True)
        self.Scene_ = QGraphicsScene()
        self.clicked = False
        self.setScene(self.Scene_)
        self.setSceneRect(0.0,0.0,sizeW,sizeH)
        self.Circle = QGraphicsEllipseItem(0.0,0.0,2*sizeRobot,2*sizeRobot)
        mat = QTransform()
        mat.translate(sizeW/2 - sizeRobot, sizeH/2 - sizeRobot)
        self.Circle.setTransform(mat)
        self.Scene_.addItem(self.Circle)
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
        self.curve = BCurve()
        self.update()
        
    def mouseMoveEvent(self, event):
        if(self.clicked):
            
            x_line = event.x() - self.LastWaypoint[0] - OffsetX
            y_line = event.y() - self.LastWaypoint[1] - OffsetY
            self.Scene_.removeItem(self.Line)
            self.Line = QGraphicsLineItem(0, 0,x_line, y_line)
            mat = QTransform()
            mat.translate(self.LastWaypoint[0],self.LastWaypoint[1])
            self.Line.setTransform(mat)
            self.Scene_.addItem(self.Line)
            self.X_pos = event.x() - OffsetX
            self.Y_pos = event.y() - OffsetY
            print 'mouse : x = %d, y=%d' % (self.X_pos, self.Y_pos)
            delta_x = self.X_pos - self.LastWaypoint[0]
            delta_y = self.Y_pos - self.LastWaypoint[1]
            distance_ = math.sqrt(delta_x * delta_x + delta_y * delta_y)
            if(distance_ > Threshold):
                self.AddWaypoint()
                
            self.update()
            
    
    def mousePressEvent(self, event):
        if(event.buttons() == Qt.LeftButton):
            self.clicked = True
    
    def mouseReleaseEvent(self, event):
        self.clicked = False
        
        
    def AddWaypoint(self):
        x_line = self.X_pos - self.LastWaypoint[0]
        y_line = self.Y_pos - self.LastWaypoint[1]
        line_ = QGraphicsLineItem(0, 0,x_line, y_line)
        mat = QTransform()
        mat.translate(self.LastWaypoint[0],self.LastWaypoint[1])
        line_.setTransform(mat)
        self.Scene_.addItem(line_)
        self.update()
        self.LastWaypoint = [self.X_pos, self.Y_pos]
        X_ = self.X_pos + OffsetX
        Y_ = self.Y_pos + OffsetY
        self.WaypointList.append([X_, Y_])
        
    def getTrajectory(self):
        TrajPt = []
        for i_pt in range(len(self.WaypointList)):
            TrajPt.append([(self.WaypointList[i_pt][0] - self.WaypointList[0][0])/800, (self.WaypointList[i_pt][1] - self.WaypointList[0][1])/800])
        
        return TrajPt  
    
    def getTrajectoryPxl(self):
        TrajPt = []
        for i_pt in range(len(self.WaypointList)):
            TrajPt.append([self.WaypointList[i_pt][0], self.WaypointList[i_pt][1]])
        
        return TrajPt              
        

class VREPclient():
    def __init__(self):
        self.clientID = -1
        self.LWMotor_hdl = None
        self.RWMotor_hdl = None
        self.Robot_hdl = None
        self.VLeft = 0.0
        self.VRight = 0.0
        self.actAngle = 180.0

    def start(self):
        print ('Program started')
        vrep.simxFinish(-1) # just in case, close all opened connections
        self.clientID = vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
        if self.clientID != -1:
            print ('Connected to remote API server')
            self.LWMotor_hdl = vrep.simxGetObjectHandle(self.clientID,'LeftWheel_Motor', vrep.simx_opmode_oneshot_wait) # LeftWheel Motor handle
            self.RWMotor_hdl = vrep .simxGetObjectHandle(self.clientID,'RightWheel_Motor', vrep.simx_opmode_oneshot_wait) # RightWheel Motor handle
            self.Robot_hdl = vrep.simxGetObjectHandle(self.clientID, 'Cubot', vrep.simx_opmode_oneshot_wait)
            print ('Handle acquired !!')
        else:
            print ('Error : connection to vrep failed')
    
    def computeVelocityAngle(self, LastPosition, NextPosition):
        if self.clientID != -1:
            targetAngle = math.degrees(math.atan2(-(NextPosition[0]-LastPosition[0]),-(NextPosition[1]-LastPosition[1]))) + 180.0
            print ('Angleact : %f') % (self.actAngle)
            print ('Angle : %f') % (targetAngle)
            distanceang_ = targetAngle - self.actAngle
            if(math.fabs(distanceang_)>180.0): ## 
                if(distanceang_ > 0.0): #targetAngle > actAngle
                    distanceang_ = distanceang_ - 360.0
                else: #targetAngle < actAngle
                    distanceang_ = 360.0 + distanceang_
                    
            print ('Distance Angle : %f') % (distanceang_)
            Vmax = OmegaMax*RWheel
            OmegaMax_ = Vmax/(LWheel/2)
            Time_needed = (math.fabs(math.radians(distanceang_)) / OmegaMax_)/2
            
            if(distanceang_ > 0):
                vrep.simxSetJointTargetVelocity(self.clientID,self.LWMotor_hdl[1],-OmegaMax,vrep.simx_opmode_oneshot)
                vrep.simxSetJointTargetVelocity(self.clientID,self.RWMotor_hdl[1],OmegaMax,vrep.simx_opmode_oneshot)
            else:
                vrep.simxSetJointTargetVelocity(self.clientID,self.LWMotor_hdl[1],OmegaMax,vrep.simx_opmode_oneshot)
                vrep.simxSetJointTargetVelocity(self.clientID,self.RWMotor_hdl[1],-OmegaMax,vrep.simx_opmode_oneshot)
                
            time.sleep(Time_needed)
            vrep.simxSetJointTargetVelocity(self.clientID,self.LWMotor_hdl[1],0.0,vrep.simx_opmode_oneshot)
            vrep.simxSetJointTargetVelocity(self.clientID,self.RWMotor_hdl[1],0.0,vrep.simx_opmode_oneshot)
            self.actAngle = targetAngle
            print ('OrientationDone')
            
    def computeVelocityStraight(self, LastPosition, NextPosition ):
        if self.clientID != -1:
            vector_displacement = [NextPosition[0]-LastPosition[0],NextPosition[1]-LastPosition[1]] 
            distanceStaight = math.sqrt(vector_displacement[0]*vector_displacement[0] + vector_displacement[1]*vector_displacement[1])
            Vmax = OmegaMax*RWheel
            Time_needed = math.fabs(distanceStaight) / Vmax
            print(Time_needed)
            vrep.simxSetJointTargetVelocity(self.clientID,self.LWMotor_hdl[1],OmegaMax,vrep.simx_opmode_oneshot)
            vrep.simxSetJointTargetVelocity(self.clientID,self.RWMotor_hdl[1],OmegaMax,vrep.simx_opmode_oneshot)
            time.sleep(Time_needed)
            vrep.simxSetJointTargetVelocity(self.clientID,self.LWMotor_hdl[1],0.0,vrep.simx_opmode_oneshot)
            vrep.simxSetJointTargetVelocity(self.clientID,self.RWMotor_hdl[1],0.0,vrep.simx_opmode_oneshot)             
            print ('MovementDone')
    
    def execute_trajectory(self, Trajectory):
        for i_pt in range(len(Trajectory)-1):
            self.computeVelocityAngle(Trajectory[i_pt], Trajectory[i_pt+1])
            self.computeVelocityStraight(Trajectory[i_pt], Trajectory[i_pt+1])
            
    def close_connection(self):
        if self.clientID != -1:
            # BeforeQSize closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
            vrep.simxGetPingTime(self.clientID)
        
            # Now close the connection to V-REP:
            vrep.simxFinish(self.clientID)
            print ('Program ended')
            
            
class MainWidget(QWidget):
    
    def __init__(self):
        QWidget.__init__(self)
        self.Drawer = QPainting_tool()
        # Package resources provider
        my_ui_path = "./mainwindow.ui"
        # Load and sets your ui file parameters
        loadUi(my_ui_path, self)
        self.Drawer.resize(sizeH,sizeW)
        self.setFixedSize(QSize(SizeScreenW,SizeScreenH))
        self.setMinimumSize(SizeScreenW, SizeScreenH)
        self.horizontalLayout_2.addWidget(self.Drawer)
        self.client = VREPclient()
        self.Q_timer = QTimer()
        self.Q_timer.start(3000)
        self.connect(self.execute_button,
                     SIGNAL("clicked()"),
                      self._slot_Execute_button)
        
        self.connect(self.connect_button,
                     SIGNAL("clicked()"),
                      self._slot_Connect_button)
        
        self.connect(self.Q_timer,
                     SIGNAL("timeout()"),
                     self._slot_print_size)
        
        self.connect(self.record_button,
                     SIGNAL("clicked()"),
                     self._slot_Record_button)
        
        self.record_file = open("./trajectory_pt.txt",'w')

        
    def _slot_print_size(self):
        print ("")
        #print (self.size())
    
    def _slot_Execute_button(self):
        traj = self.Drawer.getTrajectory()
        self.client.execute_trajectory(traj)
        
    def _slot_Connect_button(self):
        self.client.start()
    
    def _slot_Record_button(self):
        traj = self.Drawer.getTrajectoryPxl()
        print traj
        for i_pt in range(len(traj)):
            str_ = ("%f\t %f\n") % (traj[i_pt][0],traj[i_pt][1])
            self.record_file.write(str(str_))
        
        self.record_file.close()
        
    def closeEvent(self,event):
        self.client.close_connection()
        
def main():
    app = QApplication(sys.argv)
    
    test_g = MainWidget()
    test_g.show()
    
    return app.exec_()
    
if __name__ == '__main__':
    main()
    
####
##
##
##
##
##
##
##
##
##
####
##
##
##
##
##
##
####
##
##
##
##
##
##
##
##
####
    