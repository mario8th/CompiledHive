

def flightPath(droneLocs):
    cycles = 0
    droneDests = []
    for drone in droneLocs:
        droneDests.append([0,0,cycles])
        cycles += 1
    return droneDests
