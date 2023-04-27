from unittest.util import three_way_cmp
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import numpy as np
global x,y,width,height

width = 400
height = 400
x = 0
x0 = 0
y = 0
y0 = 0
rsize = 100

def Desenha():
    glClear(GL_COLOR_BUFFER_BIT)
    glViewport(0,0,width,height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluOrtho2D(0,2*rsize,0,2*rsize)
  
    
    DesenhaQuadrado()

    glutSwapBuffers()

def Inicializa():
    glClearColor(0,0,0,1)

def DesenhaQuadrado():
    global x,y
    
    glColor3f(0,0,255)
    glBegin(GL_QUADS)
    glVertex(x, y)
    glVertex(x, 20 + y)
    glVertex(10 + x, 20 + y)
    glVertex(10 + x, y )
    glEnd()

def Teclado(key, a, b):
    global y, x
    if (key==b"t" or key==b"T") and y + 1 < 90:
        y += 1
    if (key==b"l" or key==b"L") and x -1 > -90:
        x -= 1
    if (key==b"r" or key==b"R") and x + 1< 90:
        x += 1
    if (key==b"b" or key==b"B") and y - 1> -90:
        y -= 1
    glutPostRedisplay()

def Timer(val):
  global x, y, width, height, xx, yy, v, vx, vy, cont, breakPoint, cont, theta, menorValor, x0, y0, g, t
  print(breakPoint, cont, t)
  print(y)
  
  if cont <= 2*t:
    if cont > 1 and vy*cont - 0.5*cont**2 >= 10 :
      if x < xx:
        x = x0 + vx*cont
      elif x > xx:
        x = x0 - vx*cont
      
    if vy*cont - 0.5*cont**2 >= 0:

     y = vy*cont - 0.5*cont**2
     cont += 1


    glutPostRedisplay()
    glutTimerFunc(val,Timer,val)
  
  else:
    x0 = x
    y = 0
    glutPostRedisplay()
    

def Mouse(button, state, xMouse, yMouse):
    global x, y, width, height, xx, yy, vx, vy , breakPoint, cont, theta, menorValor, v, g, t
    if button==GLUT_LEFT_BUTTON:
        if state==GLUT_DOWN:            
            xx = xMouse/(2)
            yy = -.5*yMouse +2*rsize
            deltaX = abs(xx-x)
            deltaY = abs(yy-y)                  

            theta = np.arctan(deltaY / deltaX) if xx != x else np.pi / 2   
            distancia = np.sqrt((deltaX**2 + deltaY**2))
            v = 0.05555*distancia + 8.88888
            
            vy = v*np.sin(theta)

            breakPoint = np.sqrt(deltaX**2 + deltaY**2) / v
            t = vy
            cont = 1            
            vx = deltaX / (2*t)

            glutTimerFunc(50,Timer,50)
    
def AlteraTamanho(w2, h2):
    global width, height
    width = w2
    height = h2
    glutPostRedisplay()
    
def Main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width,height)
    glutInitWindowPosition(0,0)
    glutCreateWindow("Questao 3")
    glutDisplayFunc(Desenha)
    glutReshapeFunc(AlteraTamanho)
    glutKeyboardFunc(Teclado)
    glutMouseFunc(Mouse)
    Inicializa()
    glutMainLoop()

Main()
