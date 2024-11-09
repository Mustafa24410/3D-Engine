import pygame
from math import*

class Camera():
    def __init__(self, x, y, z, fov, cam_move_rot=[True, True, True], rota=[0, 0, 0]):
        self.pos = [x, y, z]
        self.rota = [0, 0, 0]
        self.angle = [0, 0, 0]
        self.fov = fov
        self.cam_move_rot = cam_move_rot
        self.rotate(rota)

    def move(self, trn):
        vec = pygame.Vector3(trn)
        if self.cam_move_rot[0]:
            vec = vec.rotate_x(-degrees(self.rota[0]))
        if self.cam_move_rot[1]:
            vec = vec.rotate_y(-degrees(self.rota[1]))
        if self.cam_move_rot[2]:
            vec = vec.rotate_z(degrees(self.rota[2]))
        self.pos[0] += vec.x
        self.pos[1] += vec.y
        self.pos[2] += vec.z

    def pitch(self, angle):
        self.rota[0] += angle

    def yaw(self, angle):
        self.rota[1] += angle

    def roll(self, angle):
        self.rota[2] += angle

    def rotate(self, rotate):
        self.pitch(rotate[0])
        self.yaw(rotate[1])
        self.roll(rotate[2])