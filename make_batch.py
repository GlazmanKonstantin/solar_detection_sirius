from datetime import datetime
import os
import glob
from constants import PATH
from constants import BASE_URL

def make_intervals(path, n=5):

    os.chdir(path)
    names = list(glob.glob("*"))
    dates = [datetime.strptime(i[:17], "%Y-%m-%dT%H%M%S") for i in names]
    
    pairs = [[dates[i], i] for i in range(len(dates))]
    
    pairs = sorted(pairs)

    groups = [[], [], [], [], [], []]

    for i in range(len(pairs) - 10):
        ind = names[pairs[i][1]][19]
        groups[int(ind)].append(pairs[i])

    ans = []
    
    cnt = 0
    last = [-1000 for i in range(30)]
    for g in groups:
        last = -10000
        for i in range(len(g) - 10):
            ind1 = pairs[i][1]
            ind2 = pairs[i + 9][1]
            typ = int(names[ind1][19])
            if (pairs[i + 9][0] - pairs[i][0]).seconds <= 3610 and i - last >= n:
                ans.append([pairs[j][1] for j in range(i, i + 10)])
                last = i
    return ans

if __name__ == "__main__":
    make_intervals(PATH)
