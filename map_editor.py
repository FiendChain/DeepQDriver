import pygame
import math
from src import Vec2D, Map
import pickle
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("in_file")
parser.add_argument("out_file")
parser.add_argument("--override", action="store_true")
args = parser.parse_args()

if os.path.isfile(args.out_file) and not args.override:
    print(f"Cannot override output {args.out_file}")
    exit()

pygame.init()

screen = pygame.display.set_mode([1500, 900])
running = True

try:
    with open(args.in_file, "rb") as fp:
        M = pickle.load(fp)
except IOError:
    M = Map()

def t2v(t):
    return Vec2D(t[0], t[1])

def point_rot(p, angle):
    sin, cos = math.sin(angle), math.cos(angle)

    x = cos*p.x - sin*p.y
    y = sin*p.x + cos*p.y
    return Vec2D(x, y)

def calculate_edges(M):
    inner = []
    outer = []
    gates = []

    path = M.path

    if len(path) <= 3:
        M.inner = inner
        M.outer = outer
        M.gates = gates
        return

    last_gate_pos = None

    for i in range(0, len(path)):
        prev = t2v(path[(i-1) % len(path)])
        curr = t2v(path[i])
        nxt = t2v(path[(i+1) % len(path)])

        p1 = prev-curr
        p2 = nxt-curr

        norm = p1.norm() + p2.norm()

        norm = norm / norm.length()

        width = 50
        offset = norm*width

        left = curr + offset
        right = curr - offset

        # swap if wrong order
        if i >= 1:
            k1 = (left-inner[-1]).length()
            k2 = (left-outer[-1]).length()
            if k1 > k2:
                tmp = right
                right = left
                left = tmp

        inner.append(left)
        outer.append(right)

        if last_gate_pos is not None and (last_gate_pos-curr).length() < 200:
            continue

        gate_horizontal = (left-right).norm()
        gate_vertical = point_rot(gate_horizontal, math.pi/2)

        gate_size = 10
        offset = gate_size*gate_vertical

        p1 = left+offset
        p2 = right+offset
        p3 = right-offset
        p4 = left-offset

        last_gate_pos = curr 
        gates.append((p1,p2,p3,p4))
    
    inner = [p.cast_tuple(int) for p in inner]
    outer = [p.cast_tuple(int) for p in outer]
    gates = [[ p.cast_tuple(int) for p in gate ] for gate in gates]

    M.inner = inner
    M.outer = outer
    M.gates = gates

def extend_path(pos):
    M.path.append(ev.pos)
    calculate_edges(M)

def pop_path():
    if len(M.path) >= 1:
        M.path.pop()
    calculate_edges(M)

while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1:
                extend_path(ev.pos)
            elif ev.button == 3:
                pop_path()
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_r:
                calculate_edges(M)

    screen.fill((255,255,255))

    def draw_buf(points, colour):
        if not points:
            return

        if len(points) > 1:
            pygame.draw.lines(screen, (0,0,0), True, points)

        for point in points:
            pygame.draw.circle(screen, colour, point, 10)
        
    for gate in M.gates:
        pygame.draw.polygon(screen, (0,255,0), gate)

    draw_buf(M.inner, (0,0,255)) 
    draw_buf(M.outer, (255,0,0)) 
    draw_buf(M.path, (0,255,255))


    pygame.display.flip()

with open(args.out_file, "wb") as fp:
    pickle.dump(M, fp)

pygame.quit()