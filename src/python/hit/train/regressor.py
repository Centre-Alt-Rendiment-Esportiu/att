# -*- coding: utf-8 -*-

import re
from numpy import *
from scipy import linalg
import numpy as np
import itertools

from sklearn.linear_model import  LinearRegression

class ATTSkLearnHitRegressor:
	def __init__(self, hit_processor):
		self.hit_processor = hit_processor
		self.regressor = LinearRegression()
		
	def collect_train_hits_from_file(self, str_filename):
		hits_training_values = []
		Y = []
		
		coords_pattern = "\((?P<x_coord>\d+)\,(?P<y_coord>\d+)\)"
		coords_re = re.compile(coords_pattern)

		in_lines = [line.strip() for line in open(str_filename) ]
		for line in in_lines:
			coord_X = -1
			coord_Y = -1

			# Split between timings and coords
			ar_aux = line.split(":")
			str_timings = ar_aux[0]
			str_coords = ar_aux[1]

			# Parse coords
			the_match = coords_re.match(str_coords)
			if the_match is not None:
				str_X = the_match.group("x_coord")
				str_Y = the_match.group("y_coord")
				coord_X = int(str_X)
				coord_Y = int(str_Y)
				
			# Parse timings
			values = [int(value) for value in (str_timings.split(","))]
			diffs = self.hit_processor.hit_diffs(values)
			hits_training_values.append(diffs)
			Y.append([coord_X, coord_Y])
		
		return (hits_training_values, Y)
		
	def train(self, hits_training_values, Y):
		self.regressor.fit(hits_training_values, Y)
	
	def predict(self, hit_reading):
		
		hit = self.hit_processor.parse_hit(hit_reading)

		diffs = self.hit_processor.hit_diffs(hit['sensor_timings'])	
		diffs = diffs.astype(float)
			
		predicted_value = self.regressor.predict(diffs.tolist())
		return (predicted_value[0,0], predicted_value[0,1])


class ATTClassicHitRegressor:
	def __init__(self, hit_processor):
		self.coeficients_x = []
		self.coeficients_y = []
		self.hit_processor = hit_processor
	
	def collect_train_hits_from_file(self, str_filename):
		hits_training_values = []
		Y = []
		
		coords_pattern = "\((?P<x_coord>\d+)\,(?P<y_coord>\d+)\)"
		coords_re = re.compile(coords_pattern)

		in_lines = [line.strip() for line in open(str_filename) ]
		for line in in_lines:
			coord_X = -1
			coord_Y = -1

			# Split between timings and coords
			ar_aux = line.split(":")
			str_timings = ar_aux[0]
			str_coords = ar_aux[1]

			# Parse coords
			the_match = coords_re.match(str_coords)
			if the_match is not None:
				str_X = the_match.group("x_coord")
				str_Y = the_match.group("y_coord")
				coord_X = int(str_X)
				coord_Y = int(str_Y)
				
			# Parse timings
			values = [int(value) for value in (str_timings.split(","))]
			diffs = self.hit_processor.hit_diffs(values)
			hits_training_values.append(diffs)
			Y.append([coord_X, coord_Y])
		
		return (hits_training_values, Y)
	
	def calc_matrices(self, train_values):
		Ms = []
		N_SENSORS = shape(train_values)[1]
		
		for j,mat_values in enumerate(train_values):
			for i in range(N_SENSORS): # for each row
				column = []
				
				# Remove the diagonal element. We wont use it, ignore it
				current_arr_line = np.delete(mat_values[i], i).tolist()
				
				# Quadratic first elements
				quadratics = np.power(current_arr_line, 2).tolist()
				for q in quadratics:
					column.append(q)
				
				# Product combination elements - AQUI POT ESTAR MALAMENT ...????
				arr = range(len(current_arr_line))
				indices_list = [ a for a in itertools.combinations(arr, 2) ]
				for indices in indices_list:
					the_value = current_arr_line[indices[0]]*current_arr_line[indices[1]]
					column.append(the_value)
				
				# Single elements
				for elems in current_arr_line:
					column.append(elems)
				
				# the idependent term 1			
				column.append(1)
				
				if (len(Ms)==i):
					Ms.append([column])
				else:
					Ms[i].append(column)
				
		return Ms
	
	def calc_coeficients(self, Ms, Y):
		
		MsInv = []
		self.coeficients_x = []
		self.coeficients_y = []
		for (i,M) in enumerate(Ms):

			MInv = linalg.pinv2(M)
			MsInv.append(MInv)
					
			_Y = matrix(Y)

			coef_x = MInv * _Y[:,0]
			coef_y = MInv * _Y[:,1]
			
			self.coeficients_x.append([])
			self.coeficients_y.append([])
			
			self.coeficients_x[i] = coef_x
			self.coeficients_y[i] = coef_y

		return [self.coeficients_x, self.coeficients_y]
		
	def train(self, train_values, Y):
		Ms = self.calc_matrices(train_values)
		coefs = self.calc_coeficients(Ms, Y)
		return coefs
		
	def predict(self, hit_reading):
		
		hit = self.hit_processor.parse_hit(hit_reading)			
		diffs = self.hit_processor.hit_diffs(hit['sensor_timings'])
		
		M = self.calc_matrices([diffs])
		
		xs = []
		ys = []
		for (i,M) in enumerate(M):
			
			x_aux = M*self.coeficients_x[i]
			y_aux = M*self.coeficients_y[i]
			
			xs.append(x_aux)
			ys.append(y_aux)

		x = np.mean(xs)
		y = np.mean(ys)

		return (x,y)


