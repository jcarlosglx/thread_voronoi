from random import randint
from sys import stdout
from my_config import colors, ROWS, COLUMNS, POINTS, N_THREADS, CLS


def is_border(voronoi, x, y):
    """check is the point is a border with other voronoi area

    Args:
        voronoi (List): A List of Lists
        x (Integer): X position
        y (Integer): Y position

    Returns:
        Bool: True if a point border with other voronoi area otherwise False
    """
    start_i = max(0, x-1)
    end_i = min(ROWS, x+1)
    start_j = max(0, y-1)
    end_j = min(COLUMNS, y+1)

    zone_type = voronoi[x][y]

    for x in range(start_i, end_i):
        for y in range(start_j, end_j):
            if(zone_type != voronoi[x][y]):
                return True
    return False


def print_voronoi(voronoi):
    """Print the voronoi matrix with colors. Note the screen should be
    big enogh to see the map without divisions.

    Args:
        voronoi (List): A List of Lists
    """
    list_colors = list(colors.keys())
    n_keys = len(list_colors)
    for x in range(ROWS):
        for y in range(COLUMNS):
            if is_border(voronoi, x, y):
                stdout.write(CLS)
                print(" {}".format(CLS), end="")
            else:
                number = voronoi[x][y] % n_keys
                key_color = list_colors[number]
                stdout.write(colors[key_color])
                print(" {}".format(colors[key_color]), end="")
        stdout.write(CLS)
        print()


def point_belongs_to(points_coor, point_x, point_y):
    """Given a List of points of voronoi and a coordinate in the matrix,
    return where the coordinate belogs to.

    Args:
        points_coor (List): A list of coordinates in the form:
        [[x1, y1], [x2, y2], ...]
        point_x (Integer): X position
        point_y (Integer): Y position

    Returns:
        Integer: The number of the area of voronoi
    """
    lowest_value = COLUMNS * ROWS
    for num, coor in enumerate(points_coor):
        x, y = coor
        current_value = (((x-point_x)**2) + ((y-point_y)**2))**1/2
        if (lowest_value > current_value):
            lowest_value = current_value
            index = num
    return index


def get_random_points():
    """Return a list of random coordinates

    Returns:
        List: A list of coordinates in the form:
        [[x1, y1], [x2, y2], ...]
    """
    random_x = [n for n in range(ROWS)]
    random_y = [n for n in range(COLUMNS)]
    random_points = []
    for point in range(POINTS):
        x = random_x.pop(randint(0, len(random_x)-1))
        y = random_y.pop(randint(0, len(random_y)-1))
        random_points.append((x, y))
    return random_points


def set_random_points(voronoi, points):
    """Set a id (integer, starting from 0 to N) for each voronoi area using
    the coordintes of the points given

    Args:
        voronoi (List): A List of Lists
        points (List): A list of coordinates in the form:
        [[x1, y1], [x2, y2], ...]
    """
    for point, coor in enumerate(points):
        x, y = coor
        voronoi[x][y] = point


def set_work_thread(voronoi, points, id_thread):
    """Given a voronoi matrix, the list of points of voronoi and the
    id_thread: The thread will full the rows according to
    (id, id+N_THREADS, id+2*N_THREADS, ...) until there is no row in the
    voronoi matrix with the index
    Note: N_THREADS can be change in the file "my_config"

    Args:
        voronoi (List): A List of Lists
        points (List): A list of coordinates in the form:
        [[x1, y1], [x2, y2], ...]
        id_thread (Integer): The id of the thread
    """
    x = id_thread
    while(x < ROWS):
        for y in range(COLUMNS):
            voronoi[x][y] = point_belongs_to(points, x, y)
        x += N_THREADS