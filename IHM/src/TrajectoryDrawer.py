#!/usr/bin/python

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import math


sizeW = 450.0  
sizeH = 370.0
sizeRobot = 15.0
Threshold = 10.0
OffsetX = 7.0
OffsetY = 0.0


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
        self.clear_draw()
        
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
    
    def clear_draw(self):
        self.Scene_.clear()
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
        