import random
import numpy as np
from numpy.linalg import inv
import math


from matplotlib import pyplot as plt
# (x-x_0)^2 + (y-y_0)^2 = r^2
data_file = open(’data.txt’, ’r’)
values = []
for line in data_file:
    values.append([float(line.split()[0]), float(line.split()[1])])

def get_circle_from_points(points):
    pt1, pt2, pt3 = points
    A  = np.array([[pt2[0] - pt1[0], pt2[1] - pt1[1]], [pt3[0] - pt2[0], pt3[1] - pt2[1]]])
    B = np.array([[pt2[0]**2 - pt1[0]**2 + pt2[1]**2 - pt1[1]**2], [pt3[0]**2 - pt2[0]**2 + pt3[1]**2 - pt2[1]**2]])
    inv_A = inv(A)
    c_x, c_y = np.dot(inv_A, B) / 2
    c_x, c_y = c_x[0], c_y[0]
    r = np.sqrt((c_x - pt1[0])**2 + (c_y - pt1[1])**2)
    return c_x, c_y, r

def get_distance_from_circle(x, y, r, point):
    x_1 = point[0]
    y_1 = point[1]
    x_0 = x
    y_0 = y
    distance_from_center = math.sqrt((x_1-x_0)**2 + (y_1-y_0)**2)
    return float(abs(distance_from_center - r))

def get_mean_error(x, y, r, inliners):
    error = 0.0
    for point in inliners:
    error += math.sqrt(get_distance_from_circle(x, y, r, point))
    return error/len(inliners)


max_iterations = 1000
acceptable_inliners = 380
result_file = open(’results.txt’, ’w’)
result_file.write(’Circle fitting with RANSAC’)
result_file.close()
best_circles = []
circles_error = []
for a in range(15):
    thresshold_distance = 1.0
    thresshold_inliners = 100
    min_error = float(’inf’)
    iteration = 0
    x_best = float(’inf’)
    y_best = float(’inf’)
    r_best = float(’inf’)
    while iteration < max_iterations:
        points = []
        for i in range(3):
            point = values[random.randint(0, len(values)- 1)]
            while point in points:
                point = values[random.randint(0, len(values)- 1)]
            points.append(point)

        x, y, r = get_circle_from_points(points)
        inlier_points = []
        for point in values:
            if get_distance_from_circle(x, y, r, point) < thresshold_distance:
                inlier_points.append(point)
        if (len(inlier_points) > thresshold_inliners ) and (get_mean_error(x, y, r, inlier_points) < min_error):   
            min_error = get_mean_error(x, y, r, inlier_points)
        x_best = x
        y_best = y
        r_best = r
        print(’Current best circle’, x, y, r)
        iteration += 1
        if len(inlier_points) > acceptable_inliners:
            break;
        best_circles.append([x_best, y_best, r_best])
        circles_error.append(min_error)
        plt.scatter(*zip(*values), zorder = 2, color = ’blue’)
        circle1 = plt.Circle((x_best,y_best), r_best, color = ’red’, zorder = 1)
        circle2 = plt.Circle((x_best,y_best), r_best, color = ’red’, zorder = 3, fill = False)

        fig = plt.gcf()
        ax = fig.gca()
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        ax.set_title(f’Iteration: {a+1} of 15’)
        fig.savefig(f’plots_{a+1}.png’)
        ax.clear()

        result_file = open(’results.txt’, ’a’)
        result_file.write(’\n’)
        result_file.write(’x: ’ + str(x_best) + ’ ’)
        result_file.write(’y: ’ +str(y_best) + ’ ’)
        result_file.write(’r: ’ + str(r_best) + ’ ’)
        result_file.write(’Iterations: ’ + str(iteration)+’ ’)
        result_file.write(’Inlier Points: ’ +str(len(inlier_points)) + ’ ’)
        result_file.write(’Mean Error’ + str(min_error) + ’ ’)
        result_file.close()
        print(f’Iteration {a+1} completed’)

min_error = float(’inf’)
no_circle = 0
for error in circles_error:
    if error < min_error:
        min_error = error
        no_circle = circles_error.index(error)
        result_file = open(’results.txt’, ’a’)
result_file.write(f’\nBest fitted Circle: {no_circle} Error: {min_error}
Coords: ({best_circles[no_circle+1][0]}, {best_circles[no_circle+1][1]})
Radius: {best_circles[no_circle+1][2]} ’)
result_file.close()