"""
This module implements our linear programming model for the museum problem.
The set of variables is a square mesh here;

Please see DM_2_Exposition_Au_Musée.md for more details.

Use the command below to launch it:
python Local_Search_Museum.py <path_to_input>

It will produce an output.txt and an output.png in the current directory.
"""
import math
import sys

import matplotlib.pyplot as plot

from pyscipopt import Model, quicksum

def read_input():
    """
    read inputs

    :return small_radius (int),
    :return big_radius (int),
    :return small_price (int),
    :return big_price (int),
    :return locations (set of tuple): for ex: [(4, 8), (1, 2)],
    :return width (int),
    :return height (int)
    """
    with open(sys.argv[1], "r") as file:
        small_radius, big_radius = tuple(map(int, file.readline().split(",")))
        small_price, big_price = tuple(map(int, file.readline().split(",")))
        locations = set(tuple(map(int, row.split(","))) for row in file.read().split("\n"))

        width = max(x[0] for x in locations)
        height = max(x[1] for x in locations)
    return small_radius, big_radius, small_price, big_price, locations, width, height

def create_position_set(locations, small_radius, big_radius, width, height):
    """
    Create a square mesh of variables.
    The mesh size is 1 (ie there is a variable for every integer coordinates)

    We don't create the variables too far from the nearest location to lighten the model.
    """
    position_set = set()
    for loc_x, loc_y in locations:
        for i in range(max(0, loc_x-small_radius), min(height, loc_x+1+small_radius)):
            for j in range(max(0, loc_y-small_radius), min(width, loc_y+1+small_radius)):
                if (1, i, j) in position_set:
                    continue
                if (i-loc_x)**2 + (j-loc_y)**2 <= (small_radius**2):
                    position_set.add((1, i, j))
        
        for i in range(max(0, loc_x-big_radius), min(height, loc_x+1+big_radius)):
            for j in range(max(0, loc_y-big_radius), min(width, loc_y+1+big_radius)):
                if (2, i, j) in position_set:
                    continue
                if (i-loc_x)**2 + (j-loc_y)**2 <= (big_radius**2):
                    position_set.add((2, i, j))

    return position_set

def create_model(position_set, small_radius, big_radius, small_price, big_price, locations, width, height):
    """
    Create the model

    :param position_set (set of tuple): (cam_type, pos_index(int), x, y)
    :param small_radius (int),
    :param big_radius (int),
    :param small_price (int),
    :param big_price (int),
    :param locations (list of tuple): for ex: [(4, 8), (1, 2)],
    :param width (int),
    :param height (int)

    :return a model, ready to be solved.
    """
    model = Model()

    # Variables : a binary variable for every locations and camera types
    # For now, we get the half integer location
    x = {}

    for k, i, j in position_set:
        name = str(k)+','+str(i)+','+str(j)
        x[k, i, j] = model.addVar(name, vtype='B')
    print("Optimal position (ie variable number): ", len(position_set))

    # Constraints :
    # Each art piece is monitored, ie its distance from the nearest camera is less than the radius
    for loc_index, location in enumerate(locations):
        loc_i, loc_j = location
        pos_list = set()
        for i in range(max(0, loc_i-big_radius), min(height, loc_i+1+big_radius)):
            for j in range(max(0, loc_j-big_radius), min(width, loc_j+1+big_radius)):
                sd = (i-loc_i)**2 + (j-loc_j)**2
                if sd > (big_radius**2):
                    continue
                if sd <= big_radius**2: # distance < big_radius
                    pos_list.add((2, i, j))
                if sd <= small_radius**2: # distance < small_radius
                    pos_list.add((1, i, j))
        model.addCons(quicksum(x[k, i, j] for (k, i, j) in pos_list) >= 1)

        if loc_index % 200 == 0:
            print("creating constraints for: ", loc_index)

    # Cost function
    price = (0, small_price, big_price)
    model.setObjective(
        quicksum(x[k, i, j]*price[k] for k, i, j in position_set),
        "minimize")

    return model

if __name__ == '__main__':
    SMALL_RADIUS, BIG_RADIUS, SMALL_PRICE, BIG_PRICE, LOCATIONS, WIDTH, HEIGHT = read_input()

    print("Locations: ", len(LOCATIONS), ", Width: ", WIDTH, ", Height: ", HEIGHT)

    POSITION_SET = create_position_set(LOCATIONS, SMALL_RADIUS, BIG_RADIUS, WIDTH, HEIGHT)
    MODEL = create_model(POSITION_SET, SMALL_RADIUS, BIG_RADIUS, SMALL_PRICE, BIG_PRICE, LOCATIONS, WIDTH, HEIGHT)

    print("Model created. Let solve it.")
    MODEL.hideOutput()
    MODEL.optimize()

    # Print/Plot the result
    with open('LP_output.txt', 'w') as sol_file:
        for var in MODEL.getVars():
            if MODEL.getVal(var):
                sol_file.write(var.name+"\n")

    loc_circles = []
    for loc in LOCATIONS:
        loc_circles.append(plot.Circle(loc, 0.3, color='r'))

    cam_circles = []
    for var in MODEL.getVars():
        if MODEL.getVal(var):
            cam_type, x, y = var.name.split(",")
            cam_type = int(cam_type)
            x = float(x)
            y = float(y)
            if cam_type == 1:
                cam_circles.append(plot.Circle((x, y), 0.1, color='b'))
                cam_circles.append(plot.Circle((x, y), SMALL_RADIUS, color='b', fill=False))
            if cam_type == 2:
                cam_circles.append(plot.Circle((x, y), 0.1, color='g'))
                cam_circles.append(plot.Circle((x, y), BIG_RADIUS, color='g', fill=False))

    fig, ax = plot.subplots()
    ax.set_xlim(0, max(WIDTH, HEIGHT))
    ax.set_ylim(0, max(WIDTH, HEIGHT))
    for loc_circle in loc_circles:
        ax.add_artist(loc_circle)

    for cam_circle in cam_circles:
        ax.add_artist(cam_circle)

    plot.grid(True)
    fig.savefig('LP_output.png')
    print("Optimal value: %f" % MODEL.getObjVal())
    plot.show()
