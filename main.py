from threading import Thread
from time import time
from my_config import colors, ROWS, COLUMNS, POINTS, N_THREADS
from voronoi_tools import get_random_points, set_random_points
from voronoi_tools import set_work_thread, print_voronoi

# create the matrix
voronoi = []
for x in range(ROWS):
    voronoi.append([-1 for n in range(COLUMNS)])

r_points = get_random_points()
set_random_points(voronoi, r_points)

start_time = time()
threads = list()
for i in range(N_THREADS):
    # create the thread and give a work
    new_thread = Thread(target=set_work_thread(
        voronoi, r_points, i
    ))
    new_thread.name = i
    threads.append(new_thread)
    new_thread.start()

# join the threads
for thread in threads:
    thread.join()

end_time = time()-start_time

print("Time: {0} with {1} thread\n".format(end_time, N_THREADS))

print_voronoi(voronoi)
