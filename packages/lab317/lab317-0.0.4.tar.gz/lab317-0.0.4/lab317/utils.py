from datetime import datetime as D

def chunkify(lst,n):
    return [lst[i::n].copy() for i in range(n)]

def get_months(start, end):
    s = start.split('_')
    e = end.split('_')
    sy, sm = int(s[0]), int(s[1])
    ey, em = int(e[0]), int(e[1])

    if sy == ey:
        if sm > em:
            return [] 
        if sm == em:
            return [start]
    if ey < sy:
        return []

    dates = []

    while sy < ey:
        if sm < 10:
            dates.append(str(sy) + '_0' + str(sm))
        else:
            dates.append(str(sy) + '_' + str(sm))

        if sm == 12:
            sm = 1
            sy += 1
        else:
            sm += 1


    while sm <= em:
        if sm < 10:
            dates.append(str(sy) + '_0' + str(sm))
        else:
            dates.append(str(sy) + '_' + str(sm))
        sm += 1

    return dates
