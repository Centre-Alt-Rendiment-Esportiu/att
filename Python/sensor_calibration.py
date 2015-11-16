import serial
import re
from math import fabs
import random as python_random

from numpy import *
from scipy import linalg

import pygame

class SensorCalibrationState:
	DEBUG_INPUT = 'hitdata'
	FILE_OUTPUT = 'coefficients'

	INIT 			= 'init'
	CHOOSE_SIDE 	= 'select_side'
	COLLECT_INIT 	= 'collect_init'
	COLLECT 		= 'collect'
	COLLECT_PROMPT 	= 'collect_prompt'
	MATRICES 		= 'matrices'
	TRAIN 			= 'train'
	PROMPT 			= 'prompt'
	WRITE 			= 'write'
	state = INIT

	arduino_serial = None

	positions = None
	REPETITIONS = 5

	repeated_positions = array([
		[6, 6], [6, 6], [6, 6], [6, 6], [6, 6], 
		[6, 18], [6, 18], [6, 18], [6, 18], [6, 18], 
		[6, 30], [6, 30], [6, 30], [6, 30], [6, 30], 
		[6, 42], [6, 42], [6, 42], [6, 42], [6, 42], 
		[18, 6], [18, 6], [18, 6], [18, 6], [18, 6], 
		[18, 18], [18, 18], [18, 18], [18, 18], [18, 18], 
		[18, 30], [18, 30], [18, 30], [18, 30], [18, 30], 
		[18, 42], [18, 42], [18, 42], [18, 42], [18, 42], 
		[30, 6], [30, 6], [30, 6], [30, 6], [30, 6],
		[30, 18], [30, 18], [30, 18], [30, 18], [30, 18], 
		[30, 30], [30, 30], [30, 30], [30, 30], [30, 30], 
		[30, 42], [30, 42], [30, 42], [30, 42], [30, 42], 
		[42, 6], [42, 6], [42, 6], [42, 6], [42, 6], 
		[42, 18], [42, 18], [42, 18], [42, 18], [42, 18], 
		[42, 30], [42, 30], [42, 30], [42, 30], [42, 30], 
		[42, 42], [42, 42], [42, 42], [42, 42], [42, 42], 
		[54, 6], [54, 6], [54, 6], [54, 6], [54, 6], 
		[54, 18], [54, 18], [54, 18], [54, 18], [54, 18], 
		[54, 30], [54, 30], [54, 30], [54, 30], [54, 30], 
		[54, 42], [54, 42], [54, 42], [54, 42], [54, 42]])
	                
	x = matrix(repeated_positions[:,0]).transpose()
	y = matrix(repeated_positions[:,1]).transpose()

	xCoeff1 = xCoeff2 = xCoeff3 = xCoeff4 = xCoeff5 = xCoeff6 = xCoeff7 = None
	yCoeff1 = yCoeff2 = yCoeff3 = yCoeff4 = yCoeff5 = yCoeff6 = yCoeff7 = None

	TABLE_WIDTH = 60
	TABLE_HEIGHT = 54
	SCREEN_MULITPLIER = 14.6

	font = None

	side = None
	is_right_side = None
	curSpot = None
	repetition = 0

	repetitions = []
	hit_strings = []
	training_values = []
	training_hits = None

	filename = "hitdata"

	def __init__(self, arduino_serial, positions, pygame):
		self.arduino_serial = arduino_serial
		self.positions = positions

		screen = pygame.display.get_surface()

		# Fill background
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((250, 250, 250))

		# Display some text
		self.font = pygame.font.Font(None, 36)

	def read_hit(self, arduino_serial):
		""" Gets a hit from the Arduino serial connection """

		while True:
			line = arduino_serial.readline()

			if line == None or line == "":
				continue
			else:
				return line

	def parse_hit(self, line):
		hit_re = re.match("hit: {(?P<sensor_one>\d+):(?P<volume_one>\d+) (?P<sensor_two>\d+):(?P<volume_two>\d+) (?P<sensor_three>\d+):(?P<volume_three>\d+) (?P<sensor_four>\d+):(?P<volume_four>\d+) (?P<sensor_five>\d+):(?P<volume_five>\d+) (?P<sensor_six>\d+):(?P<volume_six>\d+) (?P<sensor_seven>\d+):(?P<volume_seven>\d+) (?P<sensor_eight>\d+):(?P<volume_eight>\d+) (?P<side>[lr])}", line)
		if hit_re is None:
			print "none"
			return None
		else:
			hit = {
				"one": int(hit_re.group("sensor_one")),
				"two": int(hit_re.group("sensor_two")),
				"three": int(hit_re.group("sensor_three")),
				"four": int(hit_re.group("sensor_four")),
				"five": int(hit_re.group("sensor_five")),
				"six": int(hit_re.group("sensor_six")),
				"seven": int(hit_re.group("sensor_seven"))
			}
			print hit
			return self.generate_diffs(hit)

	def generate_diffs(self, hit):
		""" Takes a hit location and returns diffs like ONE_TWO: upper left to upper right """
		first_sensor = None
		for key in hit.keys():
			if hit[key] == 0:
				first_sensor = key
				break

		diffs = {
			"ONE_TWO" : (hit["one"] - hit["two"]),
			"ONE_THREE" : (hit["one"] - hit["three"]),
			"ONE_FOUR" : (hit["one"] - hit["four"]),
			"ONE_FIVE" : (hit["one"] - hit["five"]),
			"ONE_SIX" : (hit["one"] - hit["six"]),
			"ONE_SEVEN" : (hit["one"] - hit["seven"]),
			"TWO_THREE" : (hit["two"] - hit["three"]),
			"TWO_FOUR" : (hit["two"] - hit["four"]),
			"TWO_FIVE" : (hit["two"] - hit["five"]),
			"TWO_SIX" : (hit["two"] - hit["six"]),
			"TWO_SEVEN" : (hit["two"] - hit["seven"]),
			"THREE_FOUR" : (hit["three"] - hit["four"]),
			"THREE_FIVE" : (hit["three"] - hit["five"]),
			"THREE_SIX" : (hit["three"] - hit["six"]),
			"THREE_SEVEN" : (hit["three"] - hit["seven"]),
			"FOUR_FIVE" : (hit["four"] - hit["five"]),
			"FOUR_SIX" : (hit["four"] - hit["six"]),
			"FOUR_SEVEN" : (hit["four"] - hit["seven"]),
			"FIVE_SIX" : (hit["five"] - hit["six"]),
			"FIVE_SEVEN" : (hit["five"] - hit["seven"]),
			"SIX_SEVEN" : (hit["six"] - hit["seven"]),
			"first_sensor": first_sensor}
		return diffs

	def get_hits_from_file(self, is_right_side):
		filename = self.DEBUG_INPUT
		if is_right_side:
			filename += "-right.txt"
		else:
			filename += "-left.txt"

		reader = open(filename, 'r')
		lines = reader.readlines()
		lines = filter(lambda line: (line != "\n" and line[0] != "#"), lines)
		print lines
		return lines

	def average_repetitions(self, repetitions):
		""" Averages all the timing values for the repeated trainings """
		averages = {
			"ONE_TWO" : sum([diff["ONE_TWO"] for diff in repetitions]) / len(repetitions),
			"ONE_THREE" : sum([diff["ONE_THREE"] for diff in repetitions]) / len(repetitions),
			"ONE_FOUR" : sum([diff["ONE_FOUR"] for diff in repetitions]) / len(repetitions),
			"ONE_FIVE" : sum([diff["ONE_FIVE"] for diff in repetitions]) / len(repetitions),
			"ONE_SIX" : sum([diff["ONE_SIX"] for diff in repetitions]) / len(repetitions),
			"ONE_SEVEN" : sum([diff["ONE_SEVEN"] for diff in repetitions]) / len(repetitions),
			"TWO_THREE" : sum([diff["TWO_THREE"] for diff in repetitions]) / len(repetitions),
			"TWO_FOUR" : sum([diff["TWO_FOUR"] for diff in repetitions]) / len(repetitions),
			"TWO_FIVE" : sum([diff["TWO_FIVE"] for diff in repetitions]) / len(repetitions),
			"TWO_SIX" : sum([diff["TWO_SIX"] for diff in repetitions]) / len(repetitions),
			"TWO_SEVEN" : sum([diff["TWO_SEVEN"] for diff in repetitions]) / len(repetitions),
			"THREE_FOUR" : sum([diff["THREE_FOUR"] for diff in repetitions]) / len(repetitions),
			"THREE_FIVE" : sum([diff["THREE_FIVE"] for diff in repetitions]) / len(repetitions),
			"THREE_SIX" : sum([diff["THREE_SIX"] for diff in repetitions]) / len(repetitions),
			"THREE_SEVEN" : sum([diff["THREE_SEVEN"] for diff in repetitions]) / len(repetitions),
			"FOUR_FIVE" : sum([diff["FOUR_FIVE"] for diff in repetitions]) / len(repetitions),
			"FOUR_SIX" : sum([diff["FOUR_SIX"] for diff in repetitions]) / len(repetitions),
			"FOUR_SEVEN" : sum([diff["FOUR_SEVEN"] for diff in repetitions]) / len(repetitions),   
			"FIVE_SIX" : sum([diff["FIVE_SIX"] for diff in repetitions]) / len(repetitions),
			"FIVE_SEVEN" : sum([diff["FIVE_SEVEN"] for diff in repetitions]) / len(repetitions),
			"SIX_SEVEN" : sum([diff["SIX_SEVEN"] for diff in repetitions]) / len(repetitions),
			"first_sensor": repetitions[0]['first_sensor']}
		return averages

	def populate_matrices(self, training_values):
		M1 = []
		M2 = []
		M3 = []
		M4 = []
		M5 = []
		M6 = []
		M7 = []

		for average in training_values:
			t12 = average['ONE_TWO']
			t13 = average['ONE_THREE']
			t14 = average['ONE_FOUR']
			t15 = average['ONE_FIVE']
			t16 = average['ONE_SIX']
			t17 = average['ONE_SEVEN']
			t23 = average['TWO_THREE']
			t24 = average['TWO_FOUR']
			t25 = average['TWO_FIVE']
			t26 = average['TWO_SIX']
			t27 = average['TWO_SEVEN']
			t34 = average['THREE_FOUR']
			t35 = average['THREE_FIVE']
			t36 = average['THREE_SIX']
			t37 = average['THREE_SEVEN']
			t45 = average['FOUR_FIVE']
			t46 = average['FOUR_SIX']
			t47 = average['FOUR_SEVEN']
			t56 = average['FIVE_SIX']
			t57 = average['FIVE_SEVEN']
			t67 = average['SIX_SEVEN']
			first_ul = int(average['first_sensor'] == 'one')
			first_ur = int(average['first_sensor'] == 'two')
			first_ll = int(average['first_sensor'] == 'four')
			first_lr = int(average['first_sensor'] == 'three')
			first_cl = int(average['first_sensor'] == 'five')
			first_cu = int(average['first_sensor'] == 'six')
			first_cr = int(average['first_sensor'] == 'seven')

			# don't need first_lr because the other three 0/1 dummy variables take care of it, when they're all 0, the lin_reg knows this one is 1
			# http://dss.princeton.edu/online_help/analysis/dummy_variables.htm
			M1.append([t12**2, t13**2, t14**2, t15**2, t16**2, t17**2, t12*t13, t12*t14, t12*t15, t12*t16, t12*t17, t13*t14, t13*t15, t13*t16, t13*t17, t14*t15, t14*t16, t14*t17, t15*t16, t15*t17, t16*t17, t12, t13, t14, t15, t16, t17, 1])#, first_ul, first_ur, first_lr, first_ll, first_cl, first_cu, 1]
			M2.append([t12**2, t23**2, t24**2, t25**2, t26**2, t27**2, t12*t23, t12*t24, t12*t25, t12*t26, t12*t27, t23*t24, t23*t25, t23*t26, t23*t27, t24*t25, t24*t26, t24*t27, t25*t26, t25*t27, t26*t27, t12, t23, t24, t25, t26, t27, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
			M3.append([t13**2, t23**2, t34**2, t35**2, t36**2, t37**2, t13*t23, t13*t34, t13*t35, t13*t36, t13*t37, t23*t34, t23*t35, t23*t36, t23*t37, t34*t35, t34*t36, t34*t37, t35*t36, t35*t37, t36*t37, t13, t23, t34, t35, t36, t37, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])       
			M4.append([t14**2, t24**2, t34**2, t45**2, t46**2, t47**2, t14*t24, t14*t34, t14*t45, t14*t46, t14*t47, t24*t34, t24*t45, t24*t46, t24*t47, t34*t45, t34*t46, t34*t47, t45*t46, t45*t47, t46*t47, t14, t24, t34, t45, t46, t47, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])        
			M5.append([t15**2, t25**2, t35**2, t45**2, t56**2, t57**2, t15*t25, t15*t35, t15*t45, t15*t56, t15*t57, t25*t35, t25*t45, t25*t56, t25*t57, t35*t45, t35*t56, t35*t57, t45*t56, t45*t57, t56*t57, t15, t25, t35, t45, t56, t57, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
			M6.append([t16**2, t26**2, t36**2, t46**2, t56**2, t67**2, t16*t26, t16*t36, t16*t46, t16*t56, t16*t67, t26*t36, t26*t46, t26*t56, t26*t67, t36*t46, t36*t56, t36*t67, t46*t56, t46*t67, t56*t67, t16, t26, t36, t46, t56, t67, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
			M7.append([t17**2, t27**2, t37**2, t47**2, t57**2, t67**2, t17*t27, t17*t37, t17*t47, t17*t57, t17*t67, t27*t37, t27*t47, t27*t57, t27*t67, t37*t47, t37*t57, t37*t67, t47*t57, t47*t67, t57*t67, t17, t27, t37, t47, t57, t67, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])

		return [M1, M2, M3, M4, M5, M6, M7]

	def write_vector(self, vector, output):
		for num in vector.flat:
			output.write("%.20f\n" % (num))

	def write(self, is_right_side, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7):
		# File format:
		# X1_1
		# X1_2
		# ...
		# X1_28
		# X2_1
		# ...
		# X2_28
		# ...
		# ...
		# X7_28
		# Y1_1
		# ...
		# ...
		# Y7_28

		filename = self.FILE_OUTPUT
		if is_right_side:
			filename += "-right.txt"
		else:
			filename += "-left.txt"

		output = open(filename, 'w')
		self.write_vector(xCoeff1, output)
		self.write_vector(xCoeff2, output)
		self.write_vector(xCoeff3, output)
		self.write_vector(xCoeff4, output)
		self.write_vector(xCoeff5, output)
		self.write_vector(xCoeff6, output)
		self.write_vector(xCoeff7, output)
		self.write_vector(yCoeff1, output)
		self.write_vector(yCoeff2, output)
		self.write_vector(yCoeff3, output)
		self.write_vector(yCoeff4, output)
		self.write_vector(yCoeff5, output)
		self.write_vector(yCoeff6, output)
		self.write_vector(yCoeff7, output)    
		output.close()

	def error(self, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7, is_right_side, lines, positions):  
		distances = []
		x_distances = []
		y_distances = []
		for point in range(len(lines)):
			hit_string = lines[point]
			diffs = self.parse_hit(hit_string)
			average = self.average_repetitions([diffs])
			[predicted_x, predicted_y] = self.predict(average, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7)
			true_x = positions[point][0]
			true_y = positions[point][1]
			predicted = array( (predicted_x, predicted_y) )
			true = array( ( true_x, true_y) )
			print "Predicted: " + str(predicted)
			print "True: " + str(true)
			distance = linalg.norm(predicted - true)
			print "Distance: " + str(distance)
			distances.append(distance)

			x_distances.append( fabs(true_x - predicted_x) )
			y_distances.append( fabs(true_y - predicted_y) )

		print sort(distances)

		print "Median distance: " + str(median(distances))
		print "Median X distance: " + str(median(x_distances))
		print "Median Y distance: " + str(median(y_distances))

	def predict(self, average, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7):
		t12 = average['ONE_TWO']
		t13 = average['ONE_THREE']
		t14 = average['ONE_FOUR']
		t15 = average['ONE_FIVE']
		t16 = average['ONE_SIX']
		t17 = average['ONE_SEVEN']
		t23 = average['TWO_THREE']
		t24 = average['TWO_FOUR']
		t25 = average['TWO_FIVE']
		t26 = average['TWO_SIX']
		t27 = average['TWO_SEVEN']
		t34 = average['THREE_FOUR']
		t35 = average['THREE_FIVE']
		t36 = average['THREE_SIX']
		t37 = average['THREE_SEVEN']
		t45 = average['FOUR_FIVE']
		t46 = average['FOUR_SIX']
		t47 = average['FOUR_SEVEN']
		t56 = average['FIVE_SIX']
		t57 = average['FIVE_SEVEN']
		t67 = average['SIX_SEVEN']

		first_ul = int(average['first_sensor'] == 'one')
		first_ur = int(average['first_sensor'] == 'two')
		first_ll = int(average['first_sensor'] == 'four')
		first_lr = int(average['first_sensor'] == 'three')
		first_cl = int(average['first_sensor'] == 'five')
		first_cu = int(average['first_sensor'] == 'six')
		first_cr = int(average['first_sensor'] == 'seven')

		Poly1 = matrix([t12**2, t13**2, t14**2, t15**2, t16**2, t17**2, t12*t13, t12*t14, t12*t15, t12*t16, t12*t17, t13*t14, t13*t15, t13*t16, t13*t17, t14*t15, t14*t16, t14*t17, t15*t16, t15*t17, t16*t17, t12, t13, t14, t15, t16, t17, 1])#, first_ul, first_ur, first_lr, first_ll, first_cl, first_cu, 1]
		Poly2 = matrix([t12**2, t23**2, t24**2, t25**2, t26**2, t27**2, t12*t23, t12*t24, t12*t25, t12*t26, t12*t27, t23*t24, t23*t25, t23*t26, t23*t27, t24*t25, t24*t26, t24*t27, t25*t26, t25*t27, t26*t27, t12, t23, t24, t25, t26, t27, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
		Poly3 = matrix([t13**2, t23**2, t34**2, t35**2, t36**2, t37**2, t13*t23, t13*t34, t13*t35, t13*t36, t13*t37, t23*t34, t23*t35, t23*t36, t23*t37, t34*t35, t34*t36, t34*t37, t35*t36, t35*t37, t36*t37, t13, t23, t34, t35, t36, t37, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])       
		Poly4 = matrix([t14**2, t24**2, t34**2, t45**2, t46**2, t47**2, t14*t24, t14*t34, t14*t45, t14*t46, t14*t47, t24*t34, t24*t45, t24*t46, t24*t47, t34*t45, t34*t46, t34*t47, t45*t46, t45*t47, t46*t47, t14, t24, t34, t45, t46, t47, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])        
		Poly5 = matrix([t15**2, t25**2, t35**2, t45**2, t56**2, t57**2, t15*t25, t15*t35, t15*t45, t15*t56, t15*t57, t25*t35, t25*t45, t25*t56, t25*t57, t35*t45, t35*t56, t35*t57, t45*t56, t45*t57, t56*t57, t15, t25, t35, t45, t56, t57, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
		Poly6 = matrix([t16**2, t26**2, t36**2, t46**2, t56**2, t67**2, t16*t26, t16*t36, t16*t46, t16*t56, t16*t67, t26*t36, t26*t46, t26*t56, t26*t67, t36*t46, t36*t56, t36*t67, t46*t56, t46*t67, t56*t67, t16, t26, t36, t46, t56, t67, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
		Poly7 = matrix([t17**2, t27**2, t37**2, t47**2, t57**2, t67**2, t17*t27, t17*t37, t17*t47, t17*t57, t17*t67, t27*t37, t27*t47, t27*t57, t27*t67, t37*t47, t37*t57, t37*t67, t47*t57, t47*t67, t57*t67, t17, t27, t37, t47, t57, t67, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])

		x = zeros(7)
		y = zeros(7)

		print(Poly1.shape)
		print(xCoeff1.shape)
		print xCoeff1
		x[0] = Poly1*xCoeff1   
		x[1] = Poly2*xCoeff2
		x[2] = Poly3*xCoeff3
		x[3] = Poly4*xCoeff4
		x[4] = Poly5*xCoeff5
		x[5] = Poly6*xCoeff6
		x[6] = Poly7*xCoeff7

		y[0] = Poly1*yCoeff1   
		y[1] = Poly2*yCoeff2
		y[2] = Poly3*yCoeff3
		y[3] = Poly4*yCoeff4
		y[4] = Poly5*yCoeff5
		y[5] = Poly6*yCoeff6
		y[6] = Poly7*yCoeff7

		avgx = (x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6])/7
		avgy = (y[0] + y[1] + y[2] + y[3] + y[4] + y[5] + y[6])/7
		return [avgx, avgy]

	def update(self, setState, isPressed, pygame):
		curMsg = ''
		screen = pygame.display.get_surface()

		# Display reference dots
		for point in range(len(self.positions)):
			pygame.draw.circle(
				screen,
				(200, 200, 200),
				(self.positions[point][1] * self.SCREEN_MULITPLIER,
				self.positions[point][0] * self.SCREEN_MULITPLIER),
				0.5 * self.SCREEN_MULITPLIER)
			pygame.draw.circle(
				screen,
				(200, 200, 200),
				((self.TABLE_WIDTH + self.positions[point][1]) * self.SCREEN_MULITPLIER,
				self.positions[point][0] * self.SCREEN_MULITPLIER),
				0.5 * self.SCREEN_MULITPLIER)

		# Return to main menu
		if isPressed(pygame.K_ESCAPE):
			setState(0)

		# State machine
		if self.state == self.INIT:
			self.state = self.CHOOSE_SIDE

		#    ________  ______  ____  _____ ______   _____ ________  ______
		#   / ____/ / / / __ \/ __ \/ ___// ____/  / ___//  _/ __ \/ ____/
		#  / /   / /_/ / / / / / / /\__ \/ __/     \__ \ / // / / / __/   
		# / /___/ __  / /_/ / /_/ /___/ / /___    ___/ // // /_/ / /___   
		# \____/_/ /_/\____/\____//____/_____/   /____/___/_____/_____/   
		                                                                    
		# Choose which side to calibrate
		if self.state == self.CHOOSE_SIDE:
			curMsg = 'Which side do you wish to calibrate?'

			if isPressed(pygame.K_LEFT):
				self.is_right_side = False
				self.side = 'l'
				self.state = self.COLLECT_INIT
			if isPressed(pygame.K_RIGHT):
				self.is_right_side = True
				self.side = 'r'
				self.state = self.COLLECT_INIT
		#    __________  __    __    __________________   _____   ____________
		#   / ____/ __ \/ /   / /   / ____/ ____/_  __/  /  _/ | / /  _/_  __/
		#  / /   / / / / /   / /   / __/ / /     / /     / //  |/ // /  / /   
		# / /___/ /_/ / /___/ /___/ /___/ /___  / /    _/ // /|  // /  / /    
		# \____/\____/_____/_____/_____/\____/ /_/    /___/_/ |_/___/ /_/     
		                                                                    
		# Initialise all variables for calibration
		if self.state == self.COLLECT_INIT:
			filename = self.DEBUG_INPUT
			if self.is_right_side:
				filename += "-right.txt"
			else:
				filename += "-left.txt"
			self.training_hits = open(filename, 'w')

			self.repetition = 0
			self.curSpot = 0

			self.repetitions = []
			self.hit_strings = []
			self.training_values = []

			self.state = self.COLLECT
		#    __________  __    __    __________________
		#   / ____/ __ \/ /   / /   / ____/ ____/_  __/
		#  / /   / / / / /   / /   / __/ / /     / /   
		# / /___/ /_/ / /___/ /___/ /___/ /___  / /    
		# \____/\____/_____/_____/_____/\____/ /_/     
		                                                                      
		# For the current calibration point, read input for a given number of repititions
		if self.state == self.COLLECT:
			if self.is_right_side:
				side_msg = "Right side, "
			else:
				side_msg = "Left side, "
			curMsg = side_msg + "drop the ball at the spot, %i/5" % (self.repetition)

			pygame.draw.circle(
				screen, 
				(200, 0, 0), 
				(self.positions[self.curSpot][1] * self.SCREEN_MULITPLIER, 
				self.positions[self.curSpot][0] * self.SCREEN_MULITPLIER), 
				0.5 * self.SCREEN_MULITPLIER)

			self.hit_string = self.read_hit(self.arduino_serial)
			diffs = self.parse_hit(self.hit_string)

			if diffs is not None:
				self.repetitions.append(diffs)
				self.hit_strings.append(self.hit_string)

			self.repetition = self.repetition + 1

			if self.repetition == self.REPETITIONS:
				self.state = self.PROMPT

		#     ____  ____  ____  __  _______  ______
		#    / __ \/ __ \/ __ \/  |/  / __ \/_  __/
		#   / /_/ / /_/ / / / / /|_/ / /_/ / / /   
		#  / ____/ _, _/ /_/ / /  / / ____/ / /    
		# /_/   /_/ |_|\____/_/  /_/_/     /_/     
		                                         
		# Ask wether the calibration inputs for the current reference point seemed OK
		if self.state == self.PROMPT:
			curMsg = "Were the drops ok?"

			pygame.draw.circle(screen, 
				(150, 0, 0), 
				(self.positions[self.curSpot][1] * self.SCREEN_MULITPLIER, 
				self.positions[self.curSpot][0] * self.SCREEN_MULITPLIER), 
				0.8 * self.SCREEN_MULITPLIER)

			if isPressed(pygame.K_RETURN):
				for r in self.repetitions:
					self.average = self.average_repetitions([r])
					self.training_values.append(self.average)
				self.training_hits.write(''.join(self.hit_strings))
				self.training_hits.flush()

				self.curSpot = self.curSpot + 1
				self.repetition = 0
				self.repetitions = []
				self.hit_strings = []
				self.state = self.COLLECT

			if(self.curSpot == len(self.positions)):
				self.training_hits.close()
				self.state = self.TRAIN

			self.arduino_serial.flushInput()
		#   __________  ___    _____   __
		#  /_  __/ __ \/   |  /  _/ | / /
		#   / / / /_/ / /| |  / //  |/ / 
		#  / / / _, _/ ___ |_/ // /|  /  
		# /_/ /_/ |_/_/  |_/___/_/ |_/   
		                               
		# Once all points have been collected, calculate matrices
		if self.state == self.TRAIN:
			# training_values = collect_points(arduino_serial, is_right_side)
			[M1, M2, M3, M4, M5, M6, M7] = self.populate_matrices(self.training_values)

			# find inverses using singular value decomposition
			M1inv = linalg.pinv2(M1)
			M2inv = linalg.pinv2(M2)
			M3inv = linalg.pinv2(M3)
			M4inv = linalg.pinv2(M4)
			M5inv = linalg.pinv2(M5)
			M6inv = linalg.pinv2(M6)
			M7inv = linalg.pinv2(M7)

			print M1inv.shape
			print self.x.shape

			# find coefficients
			self.xCoeff1 = M1inv * self.x
			self.xCoeff2 = M2inv * self.x
			self.xCoeff3 = M3inv * self.x
			self.xCoeff4 = M4inv * self.x
			self.xCoeff5 = M5inv * self.x
			self.xCoeff6 = M6inv * self.x
			self.xCoeff7 = M7inv * self.x
			print self.xCoeff1

			self.yCoeff1 = M1inv * self.y
			self.yCoeff2 = M2inv * self.y
			self.yCoeff3 = M3inv * self.y
			self.yCoeff4 = M4inv * self.y
			self.yCoeff5 = M5inv * self.y
			self.yCoeff6 = M6inv * self.y
			self.yCoeff7 = M7inv * self.y
			print self.yCoeff1

			self.state = self.WRITE
		#  _       ______  ________________
		# | |     / / __ \/  _/_  __/ ____/
		# | | /| / / /_/ // /  / / / __/   
		# | |/ |/ / _, _// /  / / / /___   
		# |__/|__/_/ |_/___/ /_/ /_____/   
		                                 
		# Once matrices have been calculated, save the calibration to file and display estimated deviation
		if self.state == self.WRITE:
			self.write(
				self.is_right_side,
				self.xCoeff1, self.xCoeff2, self.xCoeff3, self.xCoeff4, self.xCoeff5, self.xCoeff6, self.xCoeff7,
				self.yCoeff1, self.yCoeff2, self.yCoeff3, self.yCoeff4, self.yCoeff5, self.yCoeff6, self.yCoeff7)

			self.error(
				self.xCoeff1, self.xCoeff2, self.xCoeff3, self.xCoeff4, self.xCoeff5, self.xCoeff6, self.xCoeff7,
				self.yCoeff1, self.yCoeff2, self.yCoeff3, self.yCoeff4, self.yCoeff5, self.yCoeff6, self.yCoeff7,
				self.is_right_side,
				self.get_hits_from_file(self.is_right_side),
				self.repeated_positions)

			# if self.side == 'l' or self.side == 'b':
			# 	self.write(
			# 		False,
			# 		self.xCoeff1, self.xCoeff2, self.xCoeff3, self.xCoeff4, self.xCoeff5, self.xCoeff6, self.xCoeff7,
			# 		self.yCoeff1, self.yCoeff2, self.yCoeff3, self.yCoeff4, self.yCoeff5, self.yCoeff6, self.yCoeff7)

			# 	self.error(
			# 		self.xCoeff1, self.xCoeff2, self.xCoeff3, self.xCoeff4, self.xCoeff5, self.xCoeff6, self.xCoeff7,
			# 		self.yCoeff1, self.yCoeff2, self.yCoeff3, self.yCoeff4, self.yCoeff5, self.yCoeff6, self.yCoeff7,
			# 		False, self.get_hits_from_file(False), self.repeated_positions)
			# if self.side == 'r' or self.side == 'b':
			# 	self.write(
			# 		True,
			# 		self.xCoeff1, self.xCoeff2, self.xCoeff3, self.xCoeff4, self.xCoeff5, self.xCoeff6, self.xCoeff7,
			# 		self.yCoeff1, self.yCoeff2, self.yCoeff3, self.yCoeff4, self.yCoeff5, self.yCoeff6, self.yCoeff7)

			# 	self.error(
			# 		self.xCoeff1, self.xCoeff2, self.xCoeff3, self.xCoeff4, self.xCoeff5, self.xCoeff6, self.xCoeff7,
			# 		self.yCoeff1, self.yCoeff2, self.yCoeff3, self.yCoeff4, self.yCoeff5, self.yCoeff6, self.yCoeff7,
			# 		True, self.get_hits_from_file(True), self.repeated_positions)

			self.state = self.CHOOSE_SIDE

		text = self.font.render(curMsg, 1, (0, 0, 0))
		screen.blit(text, (5, 10))
