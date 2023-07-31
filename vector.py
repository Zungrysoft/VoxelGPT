import math

def add(v1, v2):
    return (
        v1[0] + v2[0],
        v1[1] + v2[1],
        v1[2] + v2[2],
    )

def stot(s):
    try:
        spl = s.split(',')
        return (int(spl[0]), int(spl[1]), int(spl[2]))
    except:
        return (0, 0, 0)

def ttos(t):
    try:
        return f'{int(t[0])},{int(t[1])},{int(t[2])}'
    except:
        return '0,0,0'

# Gets the euclidean distance between two points
def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)
