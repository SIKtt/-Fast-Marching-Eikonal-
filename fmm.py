import numpy as np
from matplotlib import pyplot as plt

def getNeighbor(x, y):
    xleft, xright, ytop, ybottom = getBound(x,y)
    res = [
        [xleft, ytop], [x,ytop], [xright, ytop],
        [xleft, y], [xright,y],
        [xleft, ybottom], [x, ybottom], [xright, ybottom]
    ]
    # duplicate 
    list2 = []
    for l1 in res:
        if l1 not in list2:
            list2.append(l1)
    return list2


def lenTrival(state):
    count = 0
    for i in range(0,nx,1):
        for j in range(0,ny,1):
            if state[i][j] == 1: count+=1
    return count
    
def pointTrival(state):
    points = []
    for i in range(0,nx,1):
        for j in range(0,ny,1):
            if state[i][j] == 1: points.append([i,j])
    return points

def getMinTime(points):
    temp, resx, resy = 1000, 0, 0
    for point in points:
        x = point[0]
        y = point[1]
        if temp > time[x][y]: 
            temp = time[x][y]
            resx = x 
            resy = y
    return resx, resy

def getBound(x, y):
    leftBound = 0
    rightBound = nx-1
    topBound = 0
    bottomBound = ny-1

    xleft = x-1
    xright = x+1
    if x == leftBound:
        xleft = x
    if x == rightBound:
        xright = x

    ytop = y-1
    ybottom = y+1
    if y == topBound:
        ytop = y
    if y == bottomBound:
        ybottom = y
    return xleft, xright, ytop, ybottom



if __name__ == "__main__":
 
    nx = 50
    ny = 50
    s = []
    domain = np.zeros((nx,ny))
    state = np.zeros((nx,ny))
    time = np.zeros((nx,ny))
    vel = np.ones((nx,ny))
    h = 1
# Init T
    for i in range(0,nx,1):
        for j in range(0,ny,1):
            time[i][j] = 10000
    time[0][25] = 1
    s.append((0,25))

# Init Narrow Band
    for point in s:
        locx, locy = point[0], point[1]
        localNeighbor = getNeighbor(locx, locy)
        print(localNeighbor)
        for n in localNeighbor:
            pointx, pointy  = n[0], n[1]
            if not state[pointx][pointy] == 2:  # STATUS NOT Alive
                state[pointx][pointy] = 1 # STATUS to Trival
                time[pointx][pointy] = time[locx][locy] + h * vel[pointx][pointy]
        state[locx][locy] = 2
# Updating T
    count = 0
    while (not lenTrival(state) == 0):
        count +=1 
        print(lenTrival(state))
        trivalPoints = pointTrival(state)
        mx, my = getMinTime(trivalPoints)
        print(mx,my)
        state[mx][my] = 2 # 窄带中的最小T设为 Alive
        ms = getNeighbor(mx,my)
        for p in ms:
            pointx, pointy  = p[0], p[1]
            if state[pointx][pointy] == 2:
                continue
            xleft, xright, ytop, ybottom = getBound(pointx, pointy)
            if not state[pointx][pointy] == 2:
                T1 = min(time[xleft][pointy], time[xright][pointy])
                T2 = min(time[pointx][ytop], time[pointx][ybottom])
                locVel = vel[pointx][pointy]
                if abs(T1-T2) < h/locVel:
                    t = (T1+T2+np.sqrt(2*h*h/locVel - (T1 - T2)**2)) / 2
                else:
                    t = min(T1, T2) + h / locVel
                time[pointx][pointy] = min(time[pointx][pointy], t)
                state[pointx][pointy] = 1

    plt.imshow(time)
    plt.show()

