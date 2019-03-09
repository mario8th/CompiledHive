from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
import random

SHAPE_COLOR = 'red'
DRONE_COLOR = 'grey'
SENSOR_COLOR = 'blue'
OPATH_COLOR = 'lime'

DISPLAY_FULL_SHAPES = True

def update_plot(i):
    # Clear plot
    ax.clear()

    # Set up plot again
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    # Get next point
    # Change get_points to change method of getting points
    newpoints = get_points(i)

    toapx = []
    toapy = []
    toapz = []

    # Place points into array for graphing
    for point in newpoints:
        toapx.append(point[0])
        toapy.append(point[1])
        toapz.append(point[2])

    # Save point locations for later use
    allx.append(toapx)
    ally.append(toapy)
    allz.append(toapz)

    # Plot drone points in grey with a v marker
    ax.scatter(toapx, toapy, toapz, c=DRONE_COLOR, marker='v', alpha = 1)

    # "Sensor" locations to be plotted in blue with triangles
    # Replace with getting sensor locations in function, sensor locs may be static in final
    sens_locs = get_sensors()

    # Plot sensor locations
    ax.scatter(sens_locs[0], sens_locs[1], sens_locs[2], c=SENSOR_COLOR, marker='^')

    # Plot line segments from allx,y,x
    # Loop through number of drones based on number of values in first element of allx
    for count, path in enumerate(allx[0]):
        # Reset path lists
        xs = []
        ys = []
        zs = []
        # Loop through all points taking only relevant drone location and appending to be plotted
        for count2, point in enumerate(allx):
            xs.append(allx[count2][count])
            ys.append(ally[count2][count])
            zs.append(allz[count2][count])

        # Plot relevant drone
        ax.plot(xs, ys, zs, c=OPATH_COLOR, label='Flight Path', linewidth = 0.75)

    # Create rect prism points
    # Replace with reading from config
    rects =[[[1,4,0],[3,2,2]], [[4,0,5],[0,1,7]]]

    for sh in rects:
        # Loop one face
        shpx = [sh[0][0],sh[0][0],sh[0][0],sh[0][0],sh[0][0]]
        shpy = [sh[0][1],sh[0][1],sh[1][1],sh[1][1],sh[0][1]]
        shpz = [sh[1][2],sh[0][2],sh[0][2],sh[1][2],sh[1][2]]

        # Loop opposite face, at each point jump to matching point on previous face
        shpx.extend([sh[1][0],sh[1][0],sh[0][0],sh[1][0],sh[1][0],sh[0][0],sh[1][0],sh[1][0] ,sh[0][0],sh[1][0],sh[1][0]])
        shpy.extend([sh[0][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[1][1],sh[0][1] ,sh[0][1],sh[0][1],sh[0][1]])
        shpz.extend([sh[1][2],sh[1][2],sh[1][2],sh[1][2],sh[0][2],sh[0][2],sh[0][2],sh[0][2] ,sh[0][2],sh[0][2],sh[1][2]])

        ax.plot(shpx, shpy, shpz, c=SHAPE_COLOR, alpha = 0.8, linewidth = 0.9)




def get_point_random():
    x = random.random() * 8 -4
    y = random.random() * 8 -4
    z = random.random() * 8

    return [x, y, z]



def get_point(num):
    try:
        point = points[num]
    except:
        point = [0,0,4]

    return point

def get_points(num):
    try:
        point = []
        for i in points:
            point.append(i[num])
    except:
        point = [[0,0,4], [0,0,2], [0,0,0]]

    return point

def get_sensors():
    return [[-4, -4, 4, 4, -4, -4, 4, 4],
            [4, -4, 4, -4, 4, -4, 4, -4],
            [0, 0, 0, 0, 8, 8, 8, 8]]

# Generate list of points
points = []
subpoints = []
for z in range(8):
    subpoints.append([ 3, 3, z])
    subpoints.append([ 3,-3, z])
    subpoints.append([-3,-3, z])
    subpoints.append([-3, 3, z])

points.append(subpoints)
subpoints = []

for z in range(8):
    subpoints.append([ 2, 2, z])
    subpoints.append([ 2,-2, z])
    subpoints.append([-2,-2, z])
    subpoints.append([-2, 2, z])

points.append(subpoints)
subpoints = []

for z in range(8):
    subpoints.append([ 1, 1, z])
    subpoints.append([ 1,-1, z])
    subpoints.append([-1,-1, z])
    subpoints.append([-1, 1, z])

points.append(subpoints)
#End point generation


# Set up plot
fig = plt.figure()
#fig.canvas.set_window_title('Drone Visualization')
ax = fig.add_subplot(111, projection='3d')

allx = []
ally = []
allz = []

# Start animation
ani = animation.FuncAnimation(fig, update_plot, interval=100)

plt.show()

























# i want space
