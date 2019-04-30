
cycles = 0

# Takes in drone locations and returns next destination for each drone,
def flightPath(droneLocs):
    global cycles
    # expects 4 drones exactly

    print("Cycles: " + str(cycles))
    dronesReady = 0
    for drone in droneLocs:
        if cycles == 0:
            if drone[2] <= 4.0:
                drone[2] += .2
            else:
                dronesReady += 1
            if dronesReady >= len(droneLocs):
                cycles += 1
        elif cycles == 1:
            if drone[1] >= -2:
                drone[1] -= .2
            else:
                dronesReady += 1
            if dronesReady >= len(droneLocs):
                cycles += 1
        elif cycles == 2:
            if drone[2] >= 0:
                drone[2] -=.2
    return droneLocs
