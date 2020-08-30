from .Vec2D import Vec2D
import math
from .physics import\
    intersect_line_to_line,\
    check_body_gate_collision, check_body_wall_collision,\
    project_ray

class BakedMap:
    def __init__(self, M):
        self._map = M

        wall_segments = []
        wall_segments.extend(list(zip(M.outer[:-1], M.outer[1:])))
        wall_segments.append((M.outer[0], M.outer[-1]))
        wall_segments.extend(list(zip(M.inner[:-1], M.inner[1:])))
        wall_segments.append((M.inner[0], M.inner[-1]))

        wall_segments = [(Vec2D.from_tuple(p1), Vec2D.from_tuple(p2)) for p1, p2 in wall_segments]
        self.wall_segments = wall_segments

        all_gate_segments = []
        for gate in self._map.gates:
            gate_segments = []
            gate_segments.extend(list(zip(gate[:-1], gate[1:])))
            gate_segments.append((gate[0], gate[-1]))

            gate_segments = [(Vec2D.from_tuple(p1), Vec2D.from_tuple(p2)) for p1, p2 in gate_segments]

            all_gate_segments.append(gate_segments)
        
        self.all_gate_segments = all_gate_segments

    @property 
    def total_gates(self):
        return len(self._map.gates)

    def get_spawn(self):
        pos = Vec2D.from_tuple(self._map.path[0])
        nxt = Vec2D.from_tuple(self._map.path[1])
        diff_vec = nxt-pos

        if diff_vec.y < 0:
            dir_angle = math.pi+math.atan(diff_vec.x/-diff_vec.y)
        else:
            dir_angle = math.atan(diff_vec.x/-diff_vec.y)

        return pos, dir_angle
    
    def summary(self):
        print(f"gates={self.total_gates}")
        print(f"walls={len(self.wall_segments)}")
    
    def check_wall_collision(self, body_segments):
        return check_body_wall_collision(body_segments, self.wall_segments)
    
    def project_ray(self, start, end):
        return project_ray(start, end, self.wall_segments)
    
    def check_gate_collision(self, body_segments):
        return check_body_gate_collision(body_segments, self.all_gate_segments)

    def on_exit(self):
        pass
