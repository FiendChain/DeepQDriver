import pygame

class MapRenderer:
    def __init__(self):
        self.wall_colour = (0,0,0)
        self.start_gate_colour = (255,0,0)
        self.gate_colour = (0,255,0)


    def render(self, surface, M):
        # draw map
        def draw_walls(points):
            if len(points) > 1:
                pygame.draw.lines(surface, self.wall_colour, True, points)
        
        draw_walls(M.outer)
        draw_walls(M.inner)
        draw_walls(M.path)

        for i, gate in enumerate(M.gates):
            color = self.start_gate_colour if i == 0 else self.gate_colour
            pygame.draw.polygon(surface, color, gate)