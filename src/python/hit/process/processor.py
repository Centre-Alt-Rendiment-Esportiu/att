# -*- coding: utf-8 -*-

import re

import numpy as np
import time
import itertools

class ATTMatrixHitProcessor:
	def __init__(self):
		hit_pattern = "-?\d+:-?\d+|[lr]"
		self.hit_re = re.compile(hit_pattern)

	def parse_hit(self, line):
		groups = self.hit_re.findall(line)
		if groups is None:
			return None
		else:
			the_timings = [x.split(":")[0] for x in groups[:-1]]
			
			# FISTROOOO !!!!!
			#the_timings = [the_timings[i] for i in [0,2,5,7]] 

			the_values = [x.split(":")[1] for x in groups[:-1]]
			hit = {
				"side": groups[-1],
				"sensor_timings": the_timings,
				"sensor_values": the_values,
				"tstamp": time.time(),
				"raw": line
			}
			return hit
		
	def hit_diffs(self, hit_values):
		
		N_SENSORS = len(hit_values)
		mat = np.zeros([N_SENSORS,N_SENSORS])
		
		arr = range(N_SENSORS)
		for a in itertools.combinations(arr, 2):			
			diff_value = float(hit_values[a[0]])-float(hit_values[a[1]])
			mat[a[0], a[1]] = diff_value
			mat[a[1], a[0]] = diff_value
		
		return mat

class ATTPlainHitProcessor:
	def __init__(self):
		hit_pattern = "-?\d+:-?\d+|[lr]"
		self.hit_re = re.compile(hit_pattern)

	def parse_hit(self, line):
		groups = self.hit_re.findall(line)
		if groups is None:
			return None
		else:
			the_timings = [x.split(":")[0] for x in groups[:-1]]
			
			# FISTROOOO !!!!!
			#the_timings = [the_timings[i] for i in [0,2,5,7]] 

			the_values = [x.split(":")[1] for x in groups[:-1]]
			hit = {
				"side": groups[-1],
				"sensor_timings": the_timings,
				"sensor_values": the_values,
				"tstamp": time.time(),
				"raw": line
			}
			return hit

	def hit_diffs(self, hit_values):
		N_SENSORS = len(hit_values)
		
		vect = np.zeros([N_SENSORS*(N_SENSORS-1)/2])
		arr = range(N_SENSORS)
		for i,a in enumerate(itertools.combinations(arr, 2)):
			diff_value = float(hit_values[a[0]])-float(hit_values[a[1]])
			vect[i] = diff_value

		return vect















