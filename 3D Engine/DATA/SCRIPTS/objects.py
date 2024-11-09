import pygame
from math import*

screen = None
h = 0
w = 0

def initialize(scrn):
    global screen, h, w
    screen = scrn
    h = screen.get_height()
    w = screen.get_width()

class Object():
    def __init__(self, nodes, edges):
        self.points = nodes
        self.lines = edges

    def draw_point(self, color, pos):
        pygame.draw.circle(screen, color, [pos[0], pos[1]], 7)

    def draw_edge(self, color, pos1, pos2): 
        pygame.draw.line(screen, color, pos1, pos2, 7)
    
    def draw_face(self, color, pos1, pos2, pos3): 
        pygame.draw.polygon(screen, color, [pos1, pos2, pos3])

    def pitch(self, pos, angle):
        y = pos[1]
        z = pos[2]
        pos[1] = y*cos(angle) - z*sin(angle)
        pos[2] = y*sin(angle) + z*cos(angle)

    def yaw(self, pos, angle):
        x = pos[0]
        z = pos[2]
        pos[0] = x*cos(angle) + z*sin(angle)
        pos[2] = z*cos(angle) - x*sin(angle)

    def roll(self, pos, angle):
        x = pos[0]
        y = pos[1]
        pos[0] = x*cos(angle) - y*sin(angle)
        pos[1] = x*sin(angle) + y*cos(angle)
    
    def rotate_pos(self, pos, rota):
        self.pitch(pos, rota[0])
        self.yaw(pos, rota[1])
        self.roll(pos, rota[2])

    def rotate(self, rota):
        for i in self.points:
            self.rotate_pos(i, rota)

    def project(self, camera, draw_nodes, draw_edges, draw_faces, node_color, edge_color, face_color):
        pos_prj = []
        rot_points = []
        for i in self.points:
            point = i.copy()
            point[0] -= camera.pos[0]
            point[1] -= camera.pos[1]
            point[2] -= camera.pos[2]
            self.rotate_pos(point, camera.rota)
            point[0] += camera.pos[0]
            point[1] += camera.pos[1]
            point[2] += camera.pos[2]
            rot_points.append(point)

        for i in rot_points:
            x = i[0] - camera.pos[0]
            y = i[1] - camera.pos[1]
            z = i[2] - camera.pos[2]
            if z > 0:
                try:
                    x_prj = (x*camera.fov)/z+w/2
                    y_prj = -(y*camera.fov)/z+h/2
                except:
                    x_prj = x
                    y_prj = -y
                if draw_nodes:
                    self.draw_point(node_color, [x_prj, y_prj])
                pos_prj.append([x_prj, y_prj])
            else:
                pos_prj.append(False)
        if draw_edges:
            for i in self.lines:
                if pos_prj[i[0]] and pos_prj[i[1]]:
                    self.draw_edge(edge_color, pos_prj[i[0]], pos_prj[i[1]])
        if draw_faces:
            for i in self.faces:
                if pos_prj[i[0]] and pos_prj[i[1]] and pos_prj[i[2]]:
                    self.draw_face(face_color, pos_prj[i[0]], pos_prj[i[1]], pos_prj[i[2]])

class Plane(Object):
    def __init__(self, x, y, z, w, l, rota=(0, 0, 0)):
        self.points = [[x,   y,   z  ],
                       [x,   y,   z+l],
                       [x+w, y,   z+l],
                       [x+w, y,   z  ]]
        self.lines = [[0, 1],
                      [1, 2],
                      [2, 3],
                      [3, 0],
                      [3, 1]]
        self.faces = [[0, 1, 3],
                      [1, 2, 3]]
        self.rotate(rota)

class Cuboid(Object):
    def __init__(self, x, y, z, w, h, d, rota=(0, 0, 0)):
        self.points = [[x,   y,   z  ],
                       [x,   y,   z+d],
                       [x,   y+h, z  ],
                       [x,   y+h, z+d],
                       [x+w, y,   z  ],
                       [x+w, y,   z+d],
                       [x+w, y+h, z  ],
                       [x+w, y+h, z+d]]
        self.lines = [[0, 1],
                      [1, 3],
                      [3, 2],
                      [2, 0],
                      [4, 5],
                      [5, 7],
                      [7, 6],
                      [6, 4],
                      [0, 4],
                      [1, 5],
                      [2, 6],
                      [3, 7],
                      [0, 3],
                      [2, 7],
                      [0, 6],
                      [3, 5],
                      [6, 5],
                      [4, 1]]
        self.faces = [[0, 1, 3],
                      [0, 3, 2],
                      [2, 3, 7],
                      [2, 7, 6],
                      [0, 2, 6],
                      [0, 6, 4],
                      [3, 1, 5],
                      [3, 5, 7],
                      [6, 7, 5],
                      [6, 5, 4],
                      [4, 5, 1],
                      [4, 1, 0]]
        self.rotate(rota)