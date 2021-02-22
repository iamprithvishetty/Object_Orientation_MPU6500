from serial import Serial
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time

cube_vertices = ((2,0.5,1),#0
                 (2,0.5,-1),#1
                 (-2,0.5,-1),#2
                 (-2,0.5,1),#3
                 (2,-0.5,1),
                 (2,-0.5,-1),
                 (-2,-0.5,-1),
                 (-2,-0.5,1)
                 )

cube_edge = ((0,1),
             (0,3),
             (0,4),
             (2,1),
             (2,3),
             (2,6),
             (5,4),
             (5,6),
             (5,1),
             (7,6),
             (7,4),
             (7,3))

cube_face = ((0,1,2,3),
             (0,1,5,4),
             (0,3,7,4),
             (6,7,4,5),
             (6,7,3,2),
             (6,5,1,2))

color = (0.957,0.898,0.257)

def Cube():
    glBegin(GL_QUADS)
    for faces in cube_face:
        glColor3fv(color) #1st iteration (0,1,2,3)
        for vertex in faces:
            glVertex3fv(cube_vertices[vertex])
    glEnd()
    glBegin(GL_LINES)
    glColor3fv((1,1,1))
    for edges in cube_edge:
        for vertex in edges:
            glVertex3fv(cube_vertices[vertex])
    glEnd()


data = Serial("COM3",115200)
def IMU_Data(axis):
    try:
        orientation_data = data.readline().decode('UTF-8')
        #print(orientation_data)
        orientation_list = orientation_data.split('~') #[25,0,30]
        value = int(orientation_list[axis])
        #print(value)
        return value
    except:
        return 0

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display,DOUBLEBUF|OPENGL)

    gluPerspective(75 , (display[0]/display[1]),0.1,50.0 )
    glTranslatef(0,0,-5)
    glRotatef(90,1,0,0)
    value_pre_x = IMU_Data(0)
    value_pre_y = IMU_Data(1)
    value_pre_z = IMU_Data(2)
    offset_x = value_pre_x
    offset_y = value_pre_y
    offset_z = value_pre_z
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        '''value_now_x = IMU_Data(0)
        value_move = int(value_now_x-value_pre_x)
        glRotatef(value_move, 0, 1, 0)
        value_pre_x = value_now_x
        glRotatef(0, 0, 1, 0)
        value_now_y = IMU_Data(1)
        value_move = int(value_now_y - value_pre_y)
        glRotatef(value_move, 1, 0, 0)
        value_pre_y = value_now_y
        value_now_z = IMU_Data(2)
        value_move = int(value_now_z-value_pre_z)
        glRotatef(value_move, 0, 0, 1)
        value_pre_z = value_now_z'''

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        #glRotatef(1, 1, 0, 0);
        pygame.display.flip()
        pygame.time.wait(1)

main()
