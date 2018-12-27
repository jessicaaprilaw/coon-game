import pygame
import pygame.locals as pygloc #to tell pygame to use openGL

import OpenGL.GL as GL
import OpenGL.GLU as GLU

pygame.init()
screen = pygame.display.set_mode((400,800) , pygloc.DOUBLEBUF | pygloc.OPENGL)
done = False
game_clock = pygame.time.Clock()

square_vertices = ((1, 1) , (-1, 1) , (-1, -1) , (1, -1))

x=0
y=21

def grid_form():
    GL.glBegin(GL.GL_LINES)
    for x in range(-11, 12):
        GL.glVertex3fv((x, 22,0))
        GL.glVertex3fv((x, -22,0))

    for y in range(-22, 23):
        GL.glVertex3fv((-11, y, 0))
        GL.glVertex3fv((11, y,0))
    GL.glEnd()


def square_form(centre, colour):
    new_vertices = [(vertex[0] + centre[0], 
    vertex[1] + centre[1] , 0) 
    for vertex in square_vertices]

    GL.glBegin(GL.GL_QUADS)
    GL.glColor3fv(colour)
    for v in new_vertices:
        GL.glVertex3fv(v)
    GL.glEnd()

GLU.gluPerspective(45, 0.5, 0.1, 50)
GL.glTranslatef(0, 0, -50)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
            if event.key == pygame.K_RIGHT:
                x += 1
    if y>-20:
        y -= 1/30

    GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
    
    centre = (x,y//1) #hard divide jd semacem di round down
    colour = (0.0,0.4,0.75)
    grid_form()
    square_form(centre, colour)

    pygame.display.flip()
    game_clock.tick(60)