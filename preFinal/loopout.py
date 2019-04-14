
# Takes in drone locations and returns next destination for each drone,
def flightPath(droneLocs):
    # expects 4 drones exactly
    print("Hi")
    print(len(droneLocs))
    for drone in droneLocs:
        if drone[2] <= 4.0:
            drone[2] += .2 
    return droneLocs
