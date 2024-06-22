import csv

import pandas



set_1 = [[1,2,3],[4,5], [6], [7,8], [9, 10, 11], [12, 13, 14], [15, 16, 17, 18, 19, 20, 21]]
set_2 = [[1,3],[2,4,5,6], [7,8,9,10,11,12,13,14], [15, 16], [17], [18, 19, 20], [21]]


list_results = []
           
for c_1 in set_1:
        for c_2 in set_2:
            store_count = len(set(c_1) & set(c_2))
            cluster_length = len(c_1)
            
            if store_count > 0:
                percentsim = round(float(store_count)/float(cluster_length) * 100, 2)
                list_results.append([str(c_1),str(c_2), store_count, percentsim])


for row in list_results:                                
        print(row)
