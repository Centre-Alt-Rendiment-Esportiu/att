# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 21:27:23 2016
Càlcul de la distància entre els sensors i el bot de la bola
@author: Jordi
"""

import numpy as np
import pandas as pd

positions = np.array([[6, 6],
                      [6, 18],
                      [6, 30],
                      [6, 42],
                      [18, 6],
                      [18, 18],
                      [18, 30],
                      [18, 42],
                      [30, 6],
                      [30, 18],
                      [30, 30],
                      [30, 42],
                      [42, 6],
                      [42, 18],
                      [42, 30],
                      [42, 42],
                      [54, 6],
                      [54, 18],
                      [54, 30],
                      [54, 42]])

########### mesurar a la taula la posició exacta dels sensors                  
sensor_coord = np.array([[5.6, 6.2],
                         [30.5, 6.2],
                         [55.6, 5.48],
                         [17.2, 21.4],
                         [46.8, 22.2],
                         [6, 38.6],
                         [30.5, 38.6],
                         [55.6, 38.6]])


def dist_positions_sensor_coord(coord, sensor_coord):
    dist = np.zeros((sensor_coord.shape[0], 2))
    j = 0
    for i in sensor_coord:
        # print "aquest és", i
        dist[j, 0] = j
        dist[j, 1] = np.linalg.norm(i - coord)
        j = j + 1
    df_dist = pd.DataFrame(dist, columns=['sensor', 'distance'])
    return df_dist.sort(columns=['distance'])


def dist_order_all_positions(positions, sensor_coord):
    for i in positions:
        dist = dist_positions_sensor_coord(i, sensor_coord)
        print("Els sensors més propers a la posició", i, "són: \n", dist)


# print all order distance of positions to sensor_coord
dist_order_all_positions(positions, sensor_coord)
