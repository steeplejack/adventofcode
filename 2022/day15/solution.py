import re
import sys
from collections import defaultdict

def parse_line(line):
    rgx = re.compile(r'Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)')
    search = rgx.search(line)
    if search:
        return tuple(int(x) for x in search.groups())

def mhd(sx, sy, bx, by):
    return abs(sx - bx) + abs(sy - by)

def exclude(sx, sy, bx, by):
    s = set()
    d = mhd(sx, sy, bx, by)
    for y in range(sy - d, sy + 1 + d):
        for x in range(sx - (d-abs(y-sy)), sx + 1 + (d-abs(y-sy))):
            if x != bx or y != by:
                s.add((x, y))
    return s

def exclude_specific_y(sx,sy,bx,by,y):
    s = set()
    d = mhd(sx,sy,bx,by)
    for x in range(sx - (d-abs(y-sy)), sx + 1 + (d-abs(y-sy))):
        if x != bx or y != by:
            s.add((x, y))
    return s

def check_in_range(x, y, sensors):
    for (sensor_x, sensor_y), d in sensors.items():
        if mhd(sensor_x, sensor_y, x, y) <= d:
            return True
    return False

def xspan(y, sx, sy, d):
    w = max(0, d - abs(y - sy))
    if abs(y - sy) > d:
        return None
    return sx - w, sx + 1 + w

def merge(spans):
    l = []
    spans.sort()
    m = list(spans[0])
    for span in spans[1:]:
        if span[0] <= m[1] and span[1] > m[1]:
            m[1] = span[1]
        if m[1] < span[0]:
            l.append(m)
            m = list(span)
    l.append(m)
    return l


def perimeter(sx, sy, d):
    yield (sx - d, sy)
    yield (sx + d, sy)
    for x in range(sx - d + 1, sx + d):
        rem = d - abs(sx-x)
        yield (x, sy+rem)
        yield (x, sy-rem)

def rotate(p):
    x, y = p
    return (x-y, x+y)

def unrotate(p):
    x, y = p
    return (x+y) / 2, (y-x) / 2

def sensor_to_bb(sx, sy, d):
    a = rotate((sx-d, sy))
    b = rotate((sx+d, sy))
    return a, b

def isct(sq1, sq2):
    pass


if __name__ == '__main__':
    filename = 'input.txt'
    y = 10 if filename == "example.txt" else 2000000
    sensors = dict()
    beacons = set()

    with open(filename) as fl:
        for line in fl:
            sx, sy, bx, by = parse_line(line)
            beacons.add((bx,by))
            sensors[(sx,sy)] = mhd(sx, sy, bx, by)

    spans = [span for (sx, sy), d in sensors.items()
             if (span := xspan(y, sx, sy, d)) is not None]
    merged = merge(spans)
    nbeacons = sum(1 for _ in filter(lambda x: x[1] == y, beacons))
    nexcluded = sum(y-x for (x, y) in merged)
    print(f'Part 1: {nexcluded - nbeacons}')
    
    ### OLD SLOW SOLUTION 1
    # s = set()
    # sensors = dict()
    # beacons = set()
    # xs = []
    # ys = []

    # y = 10 if filename == "example.txt" else 2000000
    # with open(filename) as fl:
    #     for line in fl:
    #         sx, sy, bx, by = parse_line(line)
    #         xs.append(sx); xs.append(bx)
    #         ys.append(sy); ys.append(by)
    #         beacons.add((bx,by))
    #         sensors[(sx,sy)] = mhd(sx, sy, bx, by)
    #         excl = exclude_specific_y(sx,sy,bx,by,y)
    #         s.update(excl)

    # print(f'Part 1: {len(s)}')
    # sys.exit()


    import time

    start = time.monotonic_ns()

    cache = defaultdict(int) 
    for (sx, sy), d in sensors.items():
        for x, y in perimeter(sx, sy, d+1):
            if x >= 0 and x <= 4000000:
                if y >= 0 and y <= 4000000:
                    cache[(x, y)] += 1
                    if cache[(x, y)] == 4:
                        print(f'Part 2: {x*4000000+y}')
                        end = time.monotonic_ns()
                        print(f'{(end - start)/1000000}ms')
                        sys.exit()

    # to_check = set(sensors)
    # checking = True
    # while len(to_check) > 0:
    #     sx, sy = to_check.pop()
    #     d = sensors[(sx, sy)]
    #     for x, y in perimeter(sx, sy, d+1):
    #         if x >= 0 and x <= 4000000:
    #             if y >= 0 and y <= 4000000:
    #                 out_of_range = True
    #                 for sx2, sy2 in to_check:
    #                     d2 = sensors[(sx2, sy2)]
    #                     if abs(x - sx2) + abs(y - sy2) <= d2:
    #                         out_of_range = False
    #                 if out_of_range:
    #                     print(f'Part2: {x*4000000+y}')
    #                     end = time.monotonic_ns()
    #                     print(f'{(end - start)/1000000}ms')
    #                     sys.exit()



    # for y in range(4000000):
    #     #if y % 100000 == 0: print(f'y = {y}')
    #     spans = []
    #     for (sx, sy), d in sensors.items():
    #         span = xspan(y, sx, sy, d)
    #         if span is not None:
    #             spans.append(span)
    #     spans.sort()
    #     m = merge(spans)

    #     if not len(m) == 1:
    #         #print("0", y, m)
    #         soln = (m[0][1], y)
    #         break
    #     elif m[0][0] > 0:
    #         print("1", y, m)
    #     elif m[0][1] < 4000000:
    #         print("2", y, m)
    # print(f'Part 2: {soln[0]*4000000+soln[1]}')

    # end = time.monotonic_ns()
    # print(f'{(end - start)/1000000000}s')




