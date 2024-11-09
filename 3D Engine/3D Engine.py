import pygame #Modules
import os
import sys
from math import*
import DATA.SCRIPTS.camera as camera
import DATA.SCRIPTS.objects as objects

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Color Constants
PEACOCK = (1, 103, 149)
DDBLUE = (4, 32, 46)
LBLUE = (36, 96, 110)
BLACK = (0, 0, 0)
GREY = (175, 175, 175)

pygame.init()
clock = pygame.time.Clock()
run = True

#Screen
size = (1000, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('3D Engine')
h = screen.get_height()
w = screen.get_width()

cam_speed = 3
turn_speed = 0.5
focal_length = 400

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

objects.initialize(screen)

cam_move_rot = [True, True, True]
cam = camera.Camera(0, 75, -10, focal_length, cam_move_rot)

ground = objects.Plane(-100, 0, 100, 200, 200)
shapes = [ground, objects.Cuboid(200, 50, 200, 100, 100, 100)]

while run: #Game loop
    keys = pygame.key.get_pressed()
    mos_rel = pygame.mouse.get_rel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.mouse.set_visible(not pygame.mouse.get_visible())
                pygame.event.set_grab(not pygame.event.get_grab())
            if event.key == pygame.K_ESCAPE:
                run = False

    if keys[pygame.K_w]:
        cam.move([0, 0, cam_speed])
    elif keys[pygame.K_s]:
        cam.move([0, 0, -cam_speed])
    if keys[pygame.K_a]:
        cam.move([-cam_speed, 0, 0])
    elif keys[pygame.K_d]:
        cam.move([cam_speed, 0, 0])
    
    if keys[pygame.K_SPACE]:
        pass

    cam.yaw(-turn_speed*mos_rel[0]/100)

    screen.fill(DDBLUE)

    for shape in shapes:
        shape.project(cam, False, True, False, GREY, BLACK, LBLUE)

    pygame.display.flip() #Update screen
    clock.tick(60)
pygame.quit()