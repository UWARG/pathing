PATH_LEN = 6
LOWER_COST_BOUND = 20
UPPER_COST_BOUND = 150

from math import sqrt
diction = {'Alpha': (305235.0624128715, 5377088.035714057, 19, 'U'), 'Bravo': (305619.21086691984, 5375897.965170957, 19, 'U'), 'Charlie': (305399.133780246, 5374350.079445223, 19, 'U'),
           'Delta': (305011.5687822767, 5376913.641636748, 19, 'U'), 'Echo': (302160.1467231245, 5375399.305667925, 19, 'U'), 'Foxtrot': (307674.8101010339, 5376132.983399677, 19, 'U'),
           'Golf': (304123.9229874889, 5376400.598248743, 19, 'U'), 'Hotel': (304844.4907522614, 5376692.14961019, 19, 'U'), 'India': (304823.836766151, 5376553.670725733, 19, 'U'),
           'Juliette': (306323.01822098804, 5377346.62496889, 19, 'U'), 'Kilo': (303739.1829577129, 5375113.708127872, 19, 'U'), 'Lima': (306079.3686079817, 5375425.233621444, 19, 'U'),
           'Mike': (302702.7550076075, 5377604.89003012, 19, 'U'), 'November': (304565.75828064117, 5376263.928149134, 19, 'U'), 'Oscar': (304164.8681432564, 5376461.313624037, 19, 'U'),
           'Papa': (305753.75923819246, 5375656.545439183, 19, 'U'), 'Quebec': (305487.4694038191, 5378143.11868374, 19, 'U'), 'Point 18': (302040.33535061247, 5376630.81826965, 19, 'U'),
           'Romeo': (304791.3419064635, 5375073.267806752, 19, 'U'), 'Sierra': (305669.7020149784, 5378092.563046114, 19, 'U'), 'Tango': (302336.3520290027, 5375297.904006002, 19, 'U'),
           'Uniform': (305775.0004421508, 5374514.055343358, 19, 'U'),'Victor': (306295.94501743524, 5376348.537793905, 19, 'U'), 'Whiskey': (306380.72439548356, 5376230.161961832, 19, 'U'),
           'Xray': (307678.2538374959, 5374807.109818785, 19, 'U'), 'Yankee': (305672.56018885074, 5376470.409588414, 19, 'U'), 'Zulu': (303004.2075648238, 5374563.14442507, 19, 'U')}

num2let = {1: 'Alpha', 2: 'Bravo', 3: 'Charlie', 4: 'Delta', 5: 'Echo', 6: 'Foxtrot', 7: 'Golf', 8: 'Hotel', 9: 'India', 10: 'Juliette',
           11: 'Kilo', 12: 'Lima', 13: 'Mike', 14: 'November', 15: 'Oscar', 16: 'Papa', 17: 'Quebec', 18: 'Point 18', 19: 'Romeo',
           20: 'Sierra', 21: 'Tango', 22: 'Uniform', 23: 'Victor', 24: 'Whiskey', 25: 'Xray', 26: 'Yankee', 27: 'Zulu'}
           
import numpy as np
from random import random

obj = np.array([i for i in range(1,28)])
k = 1000
permutations = [list(np.random.choice(obj, PATH_LEN, replace=False)) for _ in range(k)]
lefile = open("myfile.csv", "w")
lst = []

for i in permutations:
  templst = []
  for j in i:
    templst.append(num2let[j]+",")
  templst.append(str( LOWER_COST_BOUND + (UPPER_COST_BOUND*random())//5*5 )+"\n")
  lst.append(templst)

for i in lst: lefile.writelines(i)