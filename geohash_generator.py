# Copyright 2019
# Antonio Nappa - Inigo Querejeta Azurmendi 

import Geohash as gh
import sys
import itertools
import json


# Function to calculate hamming distance  
def ihd(n1, n2) :
    x = n1 ^ n2
    setBits = 0
    while (x > 0) :
        setBits += x & 1
        x >>= 1
    return setBits
# Generate geohash
if __name__ == '__main__':
    lat = []
    lon = []
    res = []
    with open(sys.argv[1]) as f:
        for l in f.readlines():
            lat_e, lon_e = l.strip().split(',')
            lat.append(lat_e)
            lon.append(lon_e)
    for i in range(len(lat)):
        res.append(gh.encode(float(lat[i]), float(lon[i]), 12))
    res_n = []
    for h in res:
        bh = ''.join(format(ord(x), 'b') for x in h)
        res_n.append(int(''.join(format(ord(x), 'b') for x in h), base=2))
    i = 0
    output = []
    while i < len(res_n) - i:
        output.append([ihd(res_n[i], res_n[i+1]), res_n[i], res_n[i+1]])
        i+=1
    with open("geohash_points.json", "w") as f:
        json.dump(output, f)
