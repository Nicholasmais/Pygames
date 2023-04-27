from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
global windowWidth,windowHeight,x1,y1,rsize,xstep,ystep
global tempo4
tempo = 0
x1 = 0.0
x2 = 0.5
y1 = 0.0
y2 = 3.0
xxx2 = 0
yyy2 = 0
rsize = 10                                                 
from math import *    
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
xstep = .1
ystep = .1

def DesenhaMouse():
    global windowWidth,windowHeight,x1,y1,rsize,xstep,ystep, xxx2, yyy2
    glClear(GL_COLOR_BUFFER_BIT)    

    if (wo <= ho):
        windowHeight = 250.0*ho/wo
        windowWidth = 250.0
    else:
        windowWidth = 250.0*wo/ho
        windowHeight = 250.0        

    glViewport(0, 0, int(wo), ho);
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluOrtho2D(-10, 10, -10 ,10)
    DesenhaLinha(x2, y2)
    Desenha(x2, y2, 0, 0, 255)
    DesenhaLua(x2, y2, 255, 255, 255, xxx2, yyy2)
    Desenha(3.5, 0, 255, 255, 0)


    glutSwapBuffers();

def Inicializa():
    glClearColor(0.0, 0.0, 0.0, 1.0)# Define a cor de fundo da janela de visualização como preta

def DesenhaLinha(x, y):
  global windowWidth,windowHeight,x1,y1,rsize,xstep,ystep, x2, y2
  glColor3f(.25,.25,.25)
  glPointSize(5.0)
  glBegin(GL_LINES)
  glVertex2f(3.5, 0.0)
  glVertex2f(x, y) 
  glEnd()

def Desenha(xx2, yy2, r, g, b):
    global windowWidth,windowHeight,x1,y1,rsize,xstep,ystep, x2, y2
    #Desenha um quadrado preenchido com a cor corrente
    glColor3f(r,g,b)

    sides = 32
    if b > 0 : 
      radius = 0.25   
    else:
      radius = 0.5
    glBegin(GL_POLYGON)    
    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + xx2
        sine  = 1.5*radius * sin(i*2*pi/sides) + yy2
        glVertex2f(cosine,sine)
    glEnd()

def DesenhaLua(xx2, yy2, r, g, b, d, e):
    global windowWidth,windowHeight,x1,y1,rsize,xstep,ystep, x2, y2
    glColor3f(r,g,b)

    sides = 32
    if b > 0 : 
      radius = 0.0625   
    else:
      radius = 0.5
    glBegin(GL_POLYGON)
    for i in range(100):
        cosine= radius * cos(i*2*pi/sides) + xx2  + d + 0.015
        sine  = 1.5*radius * sin(i*2*pi/sides) + yy2  + e
        glVertex2f(cosine,sine)
    glEnd()

def GerenciaTeclado(key,x,y):
    global xf, yf, win, view_w, windowHeight,wo,ho, x2, y1

    if(key==b'W' or key ==b'w'):
        y1 += ystep
    elif (key==b'A' or key ==b'a'):
        x1 -= xstep
    elif (key==b'S' or key ==b's'):
        y1 -= xstep
    elif (key==b'D' or key ==b'd'):
        x1 += xstep
   
    glutPostRedisplay()

def GerenciaMouse(button, state, x, y):
    global x1, y1, win, windowWidth, windowHeight
    if (button == GLUT_LEFT_BUTTON):
         if (state == GLUT_DOWN):
                  # Troca o tamanho do retângulo, que vai do centro da 
                  # janela até a posição onde o usuário clicou com o mouse
                  escalax=40/wo
                  x1 = (x*escalax) - 10
                  escalay=20/ho
                  y1 = ((ho-y)*escalay) - 10
    glutPostRedisplay()
    
def AlteraTamanhoJanela(w, h):
    global wo,ho, windowHeight, windowWidth
    if(h == 0): h = 1
    wo=w;
    ho=h;       

def Timer(value):
   global windowWidth,windowHeight, x2, y2,rsize,xstep,ystep, tempo
   distancia = ((x2-3)**2+y2**2)**0.5
 
   if distancia < 2.5:
    tempo += .09
   elif distancia < 3:
    tempo += 0.085
   elif distancia < 3.5:
    tempo += 0.08
   elif distancia < 4.5:
    tempo += 0.075
   elif distancia < 5.5:
    tempo += 0.07
   elif distancia < 5.75:
    tempo += 0.06
   elif distancia < 6.25:
    tempo += 0.05
   elif distancia < 6.5:
    tempo += 0.045
   elif distancia < 7.5:
    tempo += 0.040
   elif distancia < 7.75:
    tempo += 0.035
   elif distancia < 7.95:
    tempo += 0.03
   else:
    tempo += 0.025
   
  
   x2 = 5*math.cos(tempo)
   y2 = 5*math.sin(tempo)

   glutPostRedisplay()
   t = glutGet(GLUT_ELAPSED_TIME)

   glutTimerFunc(25,Timer, t)

def TimerLua(value):
   global windowWidth,windowHeight, x2, y2,rsize,xstep,ystep, tempo, xxx2, yyy2
   
   xxx2 = 0.5*math.cos(value/100)
   yyy2 = 0.75*math.sin(value/100) 
   glutPostRedisplay()
   t = glutGet(GLUT_ELAPSED_TIME)

   glutTimerFunc(1,TimerLua, t)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(screensize[0]+100,screensize[1])
    glutInitWindowPosition(-100,0)
    glutCreateWindow(b'Primeiro Programa');
    glutDisplayFunc(DesenhaMouse);
    glutReshapeFunc(AlteraTamanhoJanela)
    glutMouseFunc(GerenciaMouse)
    t = glutGet(GLUT_ELAPSED_TIME)
    glutTimerFunc(25, Timer, t);
    glutTimerFunc(1, TimerLua, t);
    Inicializa()
    glutMainLoop();

main()
