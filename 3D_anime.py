import pygame
import pygame.locals as pygloc
import math

import OpenGL.GL as GL
import OpenGL.GLU as GLU
import OpenGL.GLUT as GLUT

DISPLAY = (800, 600)

def get_display_ratio():
    return DISPLAY[0] / DISPLAY[1]

def get_pendulum_angle(initial_angle, time, l = 10):
    current_angle = initial_angle * math.cos(math.sqrt(9.81/l) * time)
    return current_angle
    
def get_pendulum_centre(current_angle, l = 10):
    centre_x = l * math.sin(current_angle)
    centre_y = l * math.cos(current_angle)
    centre_vertex = (centre_x, l-centre_y, 0)
    return centre_vertex

def generate_pendulum(centre_vertex, l = 10):
    GL.glTranslatef(0, 0, -20)
    GL.glBegin(GL.GL_LINES)
    GL.glVertex3fv(centre_vertex)
    GL.glVertex3f(0,l,0)
    GL.glEnd()
    GL.glTranslatef(*centre_vertex)
    GLUT.glutSolidSphere(2, 50, 50)
    GL.glTranslatef(*(-c for c in centre_vertex))
    GL.glTranslatef(0, 0, 20)

def main():
    pygame.init()
    # tell pygame it will be using openGL
    pygame.display.set_mode(DISPLAY,
                            pygloc.DOUBLEBUF|pygloc.OPENGL)

    # set openGL perspective
    GLU.gluPerspective(
        45,  # degree of field-of-view
        get_display_ratio(),  # aspect ratio
        0.1,  # znear - near clipping plane
        50  # zfar - far clipping plane
    )

    light_position = (0.0, 5.0, -25.0, 0.0)
    GL.glClearColor (0.0, 0.0, 0.0, 0.0)
    GL.glShadeModel (GL.GL_SMOOTH)

    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, light_position)
    
    GL.glEnable(GL.GL_LIGHTING)
    GL.glEnable(GL.GL_LIGHT0)

    paintColor = (0.9, 0.2, 0.5, 1.0)
    shininess = (15.)
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, paintColor)
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_SHININESS, shininess)

    game_alive = True
    game_clock = pygame.time.Clock()
    time_elapsed = 0.0

    while game_alive:
        # event checks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_alive = False
                pygame.quit()
        initial_angle = (45/360) * 2*math.pi
        # initial_angle2 = (30/360) * 2*math.pi

        current_angle = get_pendulum_angle(initial_angle, time_elapsed)
        # current_angle2 = get_pendulum_angle(initial_angle2, time_elapsed, 20)
        centre_vertex = get_pendulum_centre(current_angle)
        # centre_vertex2 = get_pendulum_centre(current_angle2, 20)
       
        # clear the buffer/drawn before
        GL.glClear(
            GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT
        )

        simulation_speed = 1
        key_pressed = pygame.key.get_pressed() #the key is held, make the variable key_pressed, to get the pressed key below.
        if key_pressed [pygame.K_LEFT]: 
            simulation_speed /= 2
        if key_pressed [pygame.K_RIGHT]: 
            simulation_speed *= 2
    
        generate_pendulum(centre_vertex)
        # generate_pendulum(centre_vertex2, 20)
        # pygame displaying
        pygame.display.flip()
        game_clock.tick(60)
        time_elapsed += simulation_speed/60


if __name__ == "__main__":
    main()