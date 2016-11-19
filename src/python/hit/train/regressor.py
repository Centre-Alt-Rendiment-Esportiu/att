# -*- coding: utf-8 -*-

import abc

from scipy import linalg
import numpy as np
import itertools

from sklearn.linear_model import  LinearRegression
from sklearn.tree import DecisionTreeRegressor

class HitRegressor(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def collect_train_hits_from_file(self, str_filename):
		pass
	
	@abc.abstractmethod
	def train(self, hits_training_values, Y):
		pass
	
	@abc.abstractmethod
	def predict(self, hit_reading):
		pass
	
class ATTSkLearnHitRegressor (HitRegressor):
	def __init__(self, hit_processor):
		self.hit_processor = hit_processor
		self.regressor = LinearRegression()
		#self.regressor = DecisionTreeRegressor()
		
	def collect_train_hits_from_file(self, str_filename):
		hits_training_values = []
		Y = []
		
		in_lines = [line.strip() for line in open(str_filename) ]
		for line in in_lines:

			# Parse timings
			values = [int(value) for value in (line.split(","))]
			train_values = np.array(values[2:]).astype(int)
			
			# FISTROOOO !!!!!
			#train_values = [train_values[i] for i in [0,2,5,7]]
			 
			point = np.array(values[0:2]).astype(int)
			
			hits_training_values.append(train_values)
			Y.append(point)
		
		
		(hits_training_values, Y) = self.build_train_mean(hits_training_values, Y) 
		
		return (hits_training_values, Y)
		
	def train(self, hits_training_values, Y):
		self.regressor.fit(hits_training_values, Y)
	
	def build_train_mean(self, hits_training_values, Y):
		
		import pandas as pd
		df1 = pd.DataFrame(hits_training_values)
		df2= pd.DataFrame(Y)
		df2.columns = ['8','9']
		df = pd.concat([df1, df2], axis=1)
		dfMean = df.groupby(['8','9']).mean()
		dfYs = df2.drop_duplicates()
	
		return (dfMean.values, dfYs.values)
		
	def predict(self, hit_reading):
		hit = self.hit_processor.parse_hit(hit_reading)
		return self.predictHit(hit)

	
	def predictHit(self, hit):
		timings = np.array(hit['sensor_timings']).astype(int)
		predicted_value = self.regressor.predict(timings)
		print(predicted_value)
		print("----------")
		return (predicted_value[0,0], predicted_value[0,1])


class ATTClassicHitRegressor (HitRegressor):
	def __init__(self, hit_processor):
		self.coeficients_x = []
		self.coeficients_y = []
		self.hit_processor = hit_processor

	
	def collect_train_hits_from_file(self, str_filename):
		hits_training_values = []
		Y = []
		
		in_lines = [line.strip() for line in open(str_filename) ]
		for line in in_lines:

			# Parse timings
			values = [int(value) for value in (line.split(","))]
			train_values = values[2:]
			
			# FISTROOOO !!!!!
			#train_values = [train_values[i] for i in [0,2,5,7]] 
			
			point = values[0:2]
			
			diffs = self.hit_processor.hit_diffs(train_values)
			hits_training_values.append(diffs)
			
			Y.append(point)
		
		return (hits_training_values, Y)
		
	def calc_matrices(self, train_values):
		Ms = []
		N_SENSORS = np.shape(train_values)[1]
		
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
				arr = list(range(len(current_arr_line)))
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
					
			_Y = np.matrix(Y)

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
		#return coefs
		
	def build_train_mean(self, hits_training_values, Y):
		
		import pandas as pd
		df1 = pd.DataFrame(hits_training_values)
		df2= pd.DataFrame(Y)
		df2.columns = ['8','9']
		df = pd.concat([df1, df2], axis=1)
		dfMean = df.groupby(['8','9']).mean()
		dfYs = df2.drop_duplicates()
	
		return (dfMean.values, dfYs.values)
		
	def predict(self, hit_reading):		
		hit = self.hit_processor.parse_hit(hit_reading)			
		return self.predictHit(hit)
	
	def predictHit(self, hit):
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


