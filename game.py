import pygame
import pygame.locals as pygloc #to tell pygame to use openGL
import random

import OpenGL.GL as GL
import OpenGL.GLU as GLU

display=(405, 800)
def display_ratio():
    return display[0]/display[1]

pygame.init()
screen = pygame.display.set_mode(display , pygloc.DOUBLEBUF | pygloc.OPENGL)
done = False
game_clock = pygame.time.Clock()

square_vertices = ((0.5, 0.5) , (-0.5, 0.5) , (-0.5, -0.5) , (0.5, -0.5))

x=0
y=16

def grid_form(colour):
    GL.glBegin(GL.GL_LINES)
    GL.glColor3fv(colour)
    for x in range(-11, 12):
        GL.glVertex3fv((x-0.5, 22, 0))
        GL.glVertex3fv((x-0.5, -22, 0))

    for y in range(-22, 23):
        GL.glVertex3fv((-11, y-0.5, 0))
        GL.glVertex3fv((11, y-0.5, 0))
    GL.glEnd()

shapes = {
  "T1": ((-1, 1), (0, 1), (1, 1), (0, 0)), 
  "T2": ((0, 0), (0, 1), (0, 2), (-1, 1)),
  "T3": ((-1, 0), (0, 0), (1, 0), (0, 1)),
  "T4": ((0, 0), (0, 1), (0, 2), (1, 1)),
  "I1": ((0, 0), (0, 1), (0, 2), (0, 3)),
  "I2": ((0, 0), (1, 0), (2, 0), (3, 0)),
  "L1": ((0, 0), (1, 0), (0, 1), (0, 2)),
  "L2": ((0, 0), (0, 1), (1, 1), (2, 1)),
  "L3": ((0,0), (0, 1), (0, 2), (-1, 2)),
  "L4": ((0, 0), (1, 0), (2, 0), (2, 1)),
  "O": ((0, 0), (1, 0), (0, 1), (1, 1)),
  "S1": ((0, 0), (1, 0), (1, 1), (2, 1)),
  "S2": ((0, 0), (0, 1), (-1, 1), (-1, 2)),
  "Z1": ((0, 0), (0, 1), (-1, 1), (1, 0)),
  "Z2": ((0, 0), (0, 1), (1, 1), (1, 2)),
  "J1": ((0, 0), (1, 0), (1, 1), (1, 2)),
  "J2": ((0, 0), (0, 1), (1, 0), (2, 0)),
  "J3": ((0, 0), (0, 1), (0, 2), (1, 2)),
  "J4": ((0, 0), (0, 1), (-1, 1), (-2, 1))
}

def square_form(centre, colour):
    new_vertices = [(vertex[0] + centre[0], 
    vertex[1] + centre[1] , 0) 
    for vertex in square_vertices]

    GL.glBegin(GL.GL_QUADS)
    GL.glColor3fv(colour)
    for v in new_vertices:
        GL.glVertex3fv(v)
    GL.glEnd()
    
def draw_shape(shape, centre, colour):
    print (shape)
    for piece in shape:
        new_piece = (piece[0] + centre[0], 
    piece[1] + centre[1])
        square_form(new_piece, colour)

GLU.gluPerspective(45, display_ratio(), 0.1, 50)
GL.glTranslatef(0, 0, -35)

occupied = []

def can_go_down(shape, centre):
    if centre[1] < -13:
        return False
    for piece in shape:
        new_piece = (piece[0] + centre[0], piece[1] + centre[1] - 1)
        if new_piece in occupied:
            return False
    return True

def add_to_occupied(shape, centre):
    max_y = None
    for piece in shape:
        new_piece = (piece[0] + centre[0], piece[1] + centre[1])
        occupied.append(new_piece)
        if max_y is None:
            max_y = new_piece[1]
        elif new_piece[1]>max_y:
            max_y=new_piece[1]
    return int(max_y)
        
    
def can_go_left(shape, centre):
    min_x = None
    for piece in shape:
        new_piece = (piece[0] + centre[0]-1, piece[1] + centre[1])
        if min_x is None:
            min_x = new_piece[0]
        elif new_piece[0] < min_x:
            min_x= new_piece[0]
        if new_piece in occupied:
            return False
    if min_x<-7:
        return False    
    return True

def can_go_right(shape, centre):
    max_x = None
    for piece in shape:
        new_piece = (piece[0] + centre[0]+1, piece[1] + centre[1])
        if max_x is None:
            max_x = new_piece[0]
        elif new_piece[0]>max_x:
            max_x = new_piece[0]
        if new_piece in occupied:
            return False
    if max_x>7:
        return False
    return True    

def shape_generator():
    shape_letter = random.choice(list(shapes.keys()))
    shape = shapes[shape_letter]
    print(shape_letter, shape)
    return shape_letter, shape

def drawText(position, textString):     
    font = pygame.font.Font (None, 64)
    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    GL.glRasterPos3d(*position)     
    GL.glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, textData)

def line_clear(max_row, occupied):
    for row in range(-14, max_row+1):
        row_pieces = [piece for piece in occupied if piece[1] == row]
        if len(row_pieces) >= 15:
            occupied = [piece for piece in occupied if piece[1] < row] \
            + [(piece[0], piece[1]-1) for piece in occupied if piece[1]>row]
    return occupied

def rotate(current_letter):
    letter_mapping = {
        "T1": "T2",
        "T2": "T3",
        "T3": "T4",
        "T4": "T1",
        "I1": "I2",
        "I2": "I1",
        "L1": "L2",
        "L2": "L3",
        "L3": "L4",
        "L4": "L1",
        "O": "O",
        "S1": "S2",
        "S2": "S1",
        "Z1": "Z2",
        "Z2": "Z1",
        "J1": "J2",
        "J2": "J3",
        "J3": "J4",
        "J4": "J1",
    }
    next_letter = letter_mapping[current_letter]
    next_shape = shapes[next_letter]
    return next_letter, next_shape

current_letter, current_shape = shape_generator()
centre = (x, y)
game_over = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and can_go_left(current_shape, centre):
                x -= 1
                x = round(x)
            if event.key == pygame.K_RIGHT and can_go_right(current_shape, centre):
                x += 1
                x = round(x)
            if event.key == pygame.K_UP:
                current_letter, current_shape = rotate(current_letter)

    key_pressed = pygame.key.get_pressed()
    if key_pressed [pygame.K_LEFT] and can_go_left(current_shape, centre): x-=1/15
    if key_pressed [pygame.K_RIGHT] and can_go_right(current_shape, centre): x+=1/15
    
    if can_go_down(current_shape, centre):
        if key_pressed [pygame.K_SPACE]: y -= 1/2
        else: y -= 1/30
    else:
        if centre[1]>=16:
            game_over = True
        max_y = add_to_occupied(current_shape, centre)
        occupied = line_clear(max_y, occupied)
        current_letter, current_shape = shape_generator()
        x=0
        y=16

    GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
    
    centre = (round(x),y//1) #hard divide jd semacem di round down
    colour = (0.0, 0.4, 0.75)
    colour_o = (0.9, 0.0, 0.4)
    colour_g = (0.2, 0.2, 0.2)
    grid_form(colour_g)
    #square_form(centre, colour)
    
    draw_shape(current_shape, centre, colour)
    draw_shape(occupied, (0,0), colour_o)

    if game_over:
        drawText((-4.8,0,0), "GAME OVER")
    pygame.display.flip()
    game_clock.tick(60)