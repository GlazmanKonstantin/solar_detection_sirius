from datetime import datetime
import os
import glob
import pathlib

def make_intervals(path, n=5, batch_size=10):
    os.chdir(path)
    names = list(glob.glob("*"))
    dates = [datetime.strptime(i.split("_")[0], "%Y-%m-%dT%H%M%SZ") for i in names]
    
    pairs = [[dates[i], i] for i in range(len(dates))]

    groups = [[] for _ in range(30)]

    for i in range(len(pairs) - batch_size):
        ind = names[pairs[i][1]].split("_")[1].split(".png")[0]
        groups[int(ind)].append(pairs[i])

    for i in range(len(groups)):
        groups[i] = sorted(groups[i])
        
    ans = []

    for g in groups:
        last = -100000
        for i in range(len(g) - batch_size):
            if (g[i + batch_size - 1][0] - g[i][0]).seconds <= 361 * batch_size and i - last >= n:
                ans.append([names[g[j][1]] for j in range(i, i + batch_size)])
                last = i
    return ans
