#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from math import *

def choose(i,n):
    return factorial(n)/(factorial(i)*factorial(n-i))

def distance(a,b):
    return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def further(a,b,d):
     return distance(a,b)> d

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
                c = choose(i,3)*t**i*(1-t)**(3-i)
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
        ## procedure rajoutée pour le tracé des courbes de bezier. peut être inutile sur qt
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
        

class Pen(object):
    def __init__(self,canvas):
        self.dmax = 10 ## distance max de la souris après laquelle on rajoute un point
        self.tolerance = 30 ## distance max entre la ligne polygonale et la courbe de bezier - parametre reglable sur le robot ???
        self.dend = 5 ## distance à partir de laquelle on rajoute un dernier point au relachement de la souris

        self.canvas = canvas
        self.pos = []
        self.curve = BCurve()
        self.current = 0

    def push(self,event):
        self.canvas.delete(ALL)
        self.pos = [[event.x,event.y]]
        self.curve = BCurve()
        self.current = 0


    def move(self,event):
        if further(self.pos[-1],[event.x,event.y],self.dmax):            
            self.pos.append([event.x,event.y])
            end = len(self.pos)
            b = BCurve()
            b.from_lines(self.pos,self.current)
            while b.distance(self.pos[self.current:end]) > self.tolerance:
                end -= 1
                b.from_lines(self.pos[:end],self.current)
            if end < len(self.pos):
                self.curve.append(b)
                self.current = end - 1
            
            self.redraw()

    def release(self,event):
        if distance(self.pos[-1],[event.x,event.y]) > self.dend:
            self.canvas.create_line(self.pos[-1][0],self.pos[-1][1],event.x,event.y)
            self.pos.append([event.x,event.y])

        if self.current < len(self.pos)-1:
            b = BCurve()
            b.from_lines(self.pos,self.current)
            self.curve.append(b)
            self.current = len(self.pos) -1
        
        self.redraw()

    def redraw(self):
        self.canvas.delete(ALL)
        self.curve.draw(self.canvas)

        if self.current < len(self.pos)-1:
            b = BCurve()
            b.from_lines(self.pos,self.current)
            b.draw(self.canvas)
            
##        for i in range(self.current,len(self.pos)-1):
##            self.canvas.create_line(self.pos[i][0],self.pos[i][1],self.pos[i+1][0],self.pos[i+1][1])

main_window = Tk()
canvas = Canvas(main_window,bg='white',width=600,height=400)
pen = Pen(canvas)
canvas.bind('<ButtonPress-1>',pen.push)
canvas.bind('<B1-Motion>',pen.move)
canvas.bind('<ButtonRelease-1>',pen.release)
canvas.pack(side=LEFT)

quit_button = Button(main_window, text= 'Quitter',command = main_window.destroy)
quit_button.pack()

main_window.mainloop()
