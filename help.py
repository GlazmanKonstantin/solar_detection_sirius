from datetime import datetime
import os
import glob
from constants import PATH
from constants import BASE_URL

def make_intervals():
    os.chdir(PATH)
    names = list(glob.glob("*"))
    #print(names)
    lls = [datetime.strptime(i[:17], "%Y-%m-%dT%H%M%S") for i in names];
    
    
    ls = [[lls[i], i] for i in range(len(lls))]
    
    ls = sorted(ls)
    
    ans = []
    
    cnt = 0
    for i in range(len(ls) - 10):
        if (ls[i + 9][0] - ls[i][0]).seconds <= 3601:
            ans.append([i, i + 9])
    
    
    return ans
    

if __name__ == "__main__":
    make_intervals()
