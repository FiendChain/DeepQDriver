import multiprocessing
from .BakedMap import BakedMap
import math

from .physics import\
    intersect_line_to_line,\
    check_body_gate_collision, check_body_wall_collision,\
    project_ray

def split(a, n):
    k, m = divmod(len(a), n)
    return [a[i*k+min(i,m):(i+1)*k+min(i+1,m)] for i in range(n)]

class ThreadedWallCollider(multiprocessing.Process):
    TASK_BODY_WALL_COLLISON = 1
    TASK_PROJECT_RAY = 2
    TASK_BODY_GATE_COLLISON = 3

    def __init__(self, task_queue, result_queue, wall_segments):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.wall_segments = wall_segments

    def run(self):
        while True:
            args = self.task_queue.get()
            # Poison pill means shutdown
            if args is None:
                self.task_queue.task_done()
                return

            _id, *args = args
            rv = None
            if _id == ThreadedWallCollider.TASK_BODY_WALL_COLLISON:
                rv = check_body_wall_collision(*args, self.wall_segments)
            elif _id == ThreadedWallCollider.TASK_PROJECT_RAY:
                rv = project_ray(*args, self.wall_segments)

            self.task_queue.task_done()
            self.result_queue.put(rv)

class ThreadedBakedMap(BakedMap):
    def __init__(self, M):
        super().__init__(M)

        N = multiprocessing.cpu_count()//2
        wall_batches = split(self.wall_segments, N) 

        self.tasks = multiprocessing.JoinableQueue()
        self.results = multiprocessing.Queue()

        self.workers = [ThreadedWallCollider(self.tasks, self.results, batch) for batch in wall_batches]
        self.nb_workers = len(self.workers)
        for worker in self.workers:
            worker.start()

        print(f"Baking map with {N} processes")

    def check_wall_collision(self, body_segments):
        for _ in range(self.nb_workers):
            self.tasks.put((ThreadedWallCollider.TASK_BODY_WALL_COLLISON, body_segments)) 
        self.tasks.join()
        collisions = [self.results.get() for _ in range(self.nb_workers)]
        return bool(sum(collisions))

        # return super().check_wall_collision(body_segments)
    
    def project_ray(self, start, end):
        # too much overhead
        # for _ in range(self.nb_workers):
        #     self.tasks.put((ThreadedWallCollider.TASK_PROJECT_RAY, start, end)) 

        # self.tasks.join()
        
        # dists = [self.results.get() for _ in range(self.nb_workers)]
        # return min(dists)

        return super().project_ray(start, end)
    
    def check_gate_collision(self, body_segments):
        return check_body_gate_collision(body_segments, self.all_gate_segments)

    def on_exit(self):
        for _ in range(self.nb_workers):
            self.tasks.put(None)
        self.tasks.join()
    