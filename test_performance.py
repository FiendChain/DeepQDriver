from src.Environment import *
import pickle

import time
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("map_file")

    args = parser.parse_args()

    with open(args.map_file, "rb") as fp:
        M = pickle.load(fp)


    car = Car()
    sensor = Sensor(200, total=16)

    env = Environment(car, sensor, M)

    last_frame = time.perf_counter()

    total_reads = 0
    avg_tps = 0

    action = [1,0,0]

    try:
        while True:
            env.step(action, 1)

            curr_frame = time.perf_counter()
            dt = curr_frame-last_frame
            tps = 1/dt
            print(f"tps: {int(tps):5d}\r", end='')
            last_frame = curr_frame

            if total_reads == 0:
                avg_tps = tps
            else:
                N = total_reads
                avg_tps = (avg_tps*N + tps)/(N+1)
            
            total_reads += 1
    except KeyboardInterrupt:
        pass
    finally:
        print(f"\navg tps: {int(avg_tps)}")
    
    env.on_exit()

if __name__ == '__main__':
    main()