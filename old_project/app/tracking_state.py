import serial
import re
from math import fabs
import random as python_random

import pygame

class TrackingState:
	TABLE_WIDTH = 60
	TABLE_HEIGHT = 54
	SCREEN_MULITPLIER = 14.6

	font = None
	arduino_serial = None

	mc1_l = mc2_l = mc3_l = mc4_l = mc5_l = mc6_l = mc7_l = None
	mc1_r = mc2_r = mc3_r = mc4_r = mc5_r = mc6_r = mc7_r = None

	lastHit = [0, 0]

	def __init__(self, arduino_serial, positions, pygame):
		screen = pygame.display.get_surface()
		
		self.arduino_serial = arduino_serial

		self.importCoeffs("../../coefficients-left.txt", False)
		self.importCoeffs("../../coefficients-right.txt", True)

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
				diffs = self.parse_hit(line)
				return self.get_hit(diffs)
				# return self.parse_hit(line)

	def parse_hit(self, line):
		hit_re = re.match(
			"hit: {" +
			"(?P<sensor_one>\d+):(?P<volume_one>\d+) " +
			"(?P<sensor_two>\d+):(?P<volume_two>\d+) " +
			"(?P<sensor_three>\d+):(?P<volume_three>\d+) " +
			"(?P<sensor_four>\d+):(?P<volume_four>\d+) " +
			"(?P<sensor_five>\d+):(?P<volume_five>\d+) " +
			"(?P<sensor_six>\d+):(?P<volume_six>\d+) " +
			"(?P<sensor_seven>\d+):(?P<volume_seven>\d+) " +
			"(?P<sensor_eight>\d+):(?P<volume_eight>\d+) " +
			"(?P<side>[lr])}", line)
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
				"seven": int(hit_re.group("sensor_seven")),
				"side": string(hit_re.group("side"))
			}
			print hit
			return hit#self.generate_diffs(hit)

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

	def loadStrings(coefficientFile):
		return None

	def importCoeffs(coefficiantFile, isRightSide):
		with open(coefficiantFile) as f:
			content = f.readlines()

		coeffs = loadStrings(coefficientFile)

		# coeffs1 = [2][28]
		# coeffs2 = new float[2][28];
		# coeffs3 = new float[2][28];
		# float[][] coeffs4 = new float[2][28];
		# float[][] coeffs5 = new float[2][28];
		# float[][] coeffs6 = new float[2][28];
		# float[][] coeffs7 = new float[2][28];

		for i in range(28):
			coeffs1[0][i] = coeffs[i]
			coeffs2[0][i] = coeffs[28  + i]
			coeffs3[0][i] = coeffs[56  + i]
			coeffs4[0][i] = coeffs[84  + i]
			coeffs5[0][i] = coeffs[112 + i]
			coeffs6[0][i] = coeffs[140 + i]
			coeffs7[0][i] = coeffs[168 + i]

			coeffs1[1][i] = coeffs[196 + i]
			coeffs2[1][i] = coeffs[224 + i]
			coeffs3[1][i] = coeffs[252 + i]
			coeffs4[1][i] = coeffs[280 + i]
			coeffs5[1][i] = coeffs[308 + i]
			coeffs6[1][i] = coeffs[336 + i]
			coeffs7[1][i] = coeffs[364 + i]

		# for (int i = 0; i < 28; i++) {
		# 	coeffs1[0][i] = float(coeffs[i]);
		# 	coeffs2[0][i] = float(coeffs[28+i]);
		# 	coeffs3[0][i] = float(coeffs[56+i]);
		# 	coeffs4[0][i] = float(coeffs[84+i]);
		# 	coeffs5[0][i] = float(coeffs[112+i]);
		# 	coeffs6[0][i] = float(coeffs[140+i]);
		# 	coeffs7[0][i] = float(coeffs[168+i]);

		# 	coeffs1[1][i] = float(coeffs[196+i]); 
		# 	coeffs2[1][i] = float(coeffs[224+i]);
		# 	coeffs3[1][i] = float(coeffs[252+i]);
		# 	coeffs4[1][i] = float(coeffs[280+i]);
		# 	coeffs5[1][i] = float(coeffs[308+i]);
		# 	coeffs6[1][i] = float(coeffs[336+i]);
		# 	coeffs7[1][i] = float(coeffs[364+i]);
		# }

		if isRightSide:
			self.mc1_r = coeffs1
			self.mc2_r = coeffs2
			self.mc3_r = coeffs3
			self.mc4_r = coeffs4
			self.mc5_r = coeffs5
			self.mc6_r = coeffs6
			self.mc7_r = coeffs7
		else:
			self.mc1_l = coeffs1
			self.mc2_l = coeffs2
			self.mc3_l = coeffs3
			self.mc4_l = coeffs4
			self.mc5_l = coeffs5
			self.mc6_l = coeffs6
			self.mc7_l = coeffs7

		# if (isRightSide) { 
		# 	mc1_r = new matrixMath(coeffs1); 
		# 	mc2_r = new matrixMath(coeffs2);
		# 	mc3_r = new matrixMath(coeffs3);
		# 	mc4_r = new matrixMath(coeffs4);
		# 	mc5_r = new matrixMath(coeffs5);
		# 	mc6_r = new matrixMath(coeffs6);
		# 	mc7_r = new matrixMath(coeffs7);
		# }
		# else {
		# 	mc1_l = new matrixMath(coeffs1);
		# 	mc2_l = new matrixMath(coeffs2);
		# 	mc3_l = new matrixMath(coeffs3);
		# 	mc4_l = new matrixMath(coeffs4);
		# 	mc5_l = new matrixMath(coeffs5);
		# 	mc6_l = new matrixMath(coeffs6);
		# 	mc7_l = new matrixMath(coeffs7);
		# }

		# }

	

	def getHit(self, side, diffs):
		# String[] values = split(serialData, "{");
		# String[] timings = split(values[1], " ");

		# float t12 = float(timings[0])-float(timings[1]);
		# float t13 = float(timings[0])-float(timings[2]);
		# float t14 = float(timings[0])-float(timings[3]);
		# float t15 = float(timings[0])-float(timings[4]);
		# float t16 = float(timings[0])-float(timings[5]);
		# float t17 = float(timings[0])-float(timings[6]);
		# float t23 = float(timings[1])-float(timings[2]);
		# float t24 = float(timings[1])-float(timings[3]);
		# float t25 = float(timings[1])-float(timings[4]);
		# float t26 = float(timings[1])-float(timings[5]);
		# float t27 = float(timings[1])-float(timings[6]);
		# float t34 = float(timings[2])-float(timings[3]);
		# float t35 = float(timings[2])-float(timings[4]);
		# float t36 = float(timings[2])-float(timings[5]);
		# float t37 = float(timings[2])-float(timings[6]);
		# float t45 = float(timings[3])-float(timings[4]);
		# float t46 = float(timings[3])-float(timings[5]);
		# float t47 = float(timings[3])-float(timings[6]);
		# float t56 = float(timings[4])-float(timings[5]);
		# float t57 = float(timings[4])-float(timings[6]);
		# float t67 = float(timings[5])-float(timings[6]);

		M1 = []
		M2 = []
		M3 = []
		M4 = []
		M5 = []
		M6 = []
		M7 = []

		M1.append([t12**2, t13**2, t14**2, t15**2, t16**2, t17**2, 
			t12*t13, t12*t14, t12*t15, t12*t16, t12*t17, t13*t14, t13*t15, t13*t16, 
			t13*t17, t14*t15, t14*t16, t14*t17, t15*t16, t15*t17, t16*t17, 
			t12, t13, t14, t15, t16, t17, 1])#, first_ul, first_ur, first_lr, first_ll, first_cl, first_cr, 1]
		M2.append([t12**2, t23**2, t24**2, t25**2, t26**2, t27**2, 
			t12*t23, t12*t24, t12*t25, t12*t26, t12*t27, t23*t24, t23*t25, t23*t26, 
			t23*t27, t24*t25, t24*t26, t24*t27, t25*t26, t25*t27, t26*t27, 
			t12, t23, t24, t25, t26, t27, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
		M3.append([t13**2, t23**2, t34**2, t35**2, t36**2, t37**2, 
			t13*t23, t13*t34, t13*t35, t13*t36, t13*t37, t23*t34, t23*t35, t23*t36, 
			t23*t37, t34*t35, t34*t36, t34*t37, t35*t36, t35*t37, t36*t37, 
			t13, t23, t34, t35, t36, t37, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])       
		M4.append([t14**2, t24**2, t34**2, t45**2, t46**2, t47**2, 
			t14*t24, t14*t34, t14*t45, t14*t46, t14*t47, t24*t34, t24*t45, t24*t46, 
			t24*t47, t34*t45, t34*t46, t34*t47, t45*t46, t45*t47, t46*t47, 
			t14, t24, t34, t45, t46, t47, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])        
		M5.append([t15**2, t25**2, t35**2, t45**2, t56**2, t57**2, 
			t15*t25, t15*t35, t15*t45, t15*t56, t15*t57, t25*t35, t25*t45, t25*t56, 
			t25*t57, t35*t45, t35*t56, t35*t57, t45*t56, t45*t57, t56*t57, 
			t15, t25, t35, t45, t56, t57, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
		M6.append([t16**2, t26**2, t36**2, t46**2, t56**2, t67**2, 
			t16*t26, t16*t36, t16*t46, t16*t56, t16*t67, t26*t36, t26*t46, t26*t56, 
			t26*t67, t36*t46, t36*t56, t36*t67, t46*t56, t46*t67, t56*t67, 
			t16, t26, t36, t46, t56, t67, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
		M7.append([t17**2, t27**2, t37**2, t47**2, t57**2, t67**2, 
			t17*t27, t17*t37, t17*t47, t17*t57, t17*t67, t27*t37, t27*t47, t27*t57, 
			t27*t67, t37*t47, t37*t57, t37*t67, t47*t57, t47*t67, t57*t67, 
			t17, t27, t37, t47, t57, t67, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])

		# float[] timings1 = {
		#   pow(t12,2), pow(t13,2), pow(t14,2), pow(t15,2), pow(t16,2), pow(t17,2),
		#   t12*t13, t12*t14, t12*t15, t12*t16, t12*t17, t13*t14, t13*t15, t13*t16, 
		# 	t13*t17, t14*t15, t14*t16, t14*t17, t15*t16, t15*t17, t16*t17, 
		# 	t12, t13, t14, t15, t16, t17, 1};
		# float[] timings2 = {
		#   pow(t12,2), pow(t23,2), pow(t24,2), pow(t25,2), pow(t26,2), pow(t27,2), 
		#   t12*t23, t12*t24, t12*t25, t12*t26, t12*t27, t23*t24, t23*t25, t23*t26, 
		# 	t23*t27, t24*t25, t24*t26, t24*t27, t25*t26, t25*t27, t26*t27, 
		# 	t12, t23, t24, t25, t26, t27, 1};
		# float[] timings3 = {
		#   pow(t13,2), pow(t23,2), pow(t34,2), pow(t35,2), pow(t36,2), pow(t37,2), 
		#   t13*t23, t13*t34, t13*t35, t13*t36, t13*t37, t23*t34, t23*t35, t23*t36, 
		# 	t23*t37, t34*t35, t34*t36, t34*t37, t35*t36, t35*t37, t36*t37, 
		# 	t13, t23, t34, t35, t36, t37, 1};
		# float[] timings4 = {
		#   pow(t14,2), pow(t24,2), pow(t34,2), pow(t45,2), pow(t46,2), pow(t47,2),
		#   t14*t24, t14*t34, t14*t45, t14*t46, t14*t47, t24*t34, t24*t45, t24*t46, 
		# 	t24*t47, t34*t45, t34*t46, t34*t47, t45*t46, t45*t47, t46*t47, 
		# 	t14, t24, t34, t45, t46, t47, 1};
		# float[] timings5 = {
		#   pow(t15,2), pow(t25,2), pow(t35,2), pow(t45,2), pow(t56,2), pow(t57,2),
		#   t15*t25, t15*t35, t15*t45, t15*t56, t15*t57, t25*t35, t25*t45, t25*t56,
		# 	t25*t57, t35*t45, t35*t56, t35*t57, t45*t56, t45*t57, t56*t57, 
		# 	t15, t25, t35, t45, t56, t57, 1};  
		# float[] timings6 = {
		#   pow(t16,2), pow(t26,2), pow(t36,2), pow(t46,2), pow(t56,2), pow(t67,2),
		#   t16*t26, t16*t36, t16*t46, t16*t56, t16*t67, t26*t36, t26*t46, t26*t56, 
		# 	t26*t67, t36*t46, t36*t56, t36*t67, t46*t56, t46*t67, t56*t67, 
		#	t16, t26, t36, t46, t56, t67, 1};
		# float[] timings7 = {
		#   pow(t17,2), pow(t27,2), pow(t37,2), pow(t47,2), pow(t57,2), pow(t67,2),
		#   t17*t27, t17*t37, t17*t47, t17*t57, t17*t67, t27*t37, t27*t47, t27*t57, 
		# 	t27*t67, t37*t47, t37*t57, t37*t67, t47*t57, t47*t67, t57*t67, 
		# 	t17, t27, t37, t47, t57, t67, 1};
		    
		# PVector guess1 = null;
		# PVector guess2 = null;
		# PVector guess3 = null;
		# PVector guess4 = null;
		# PVector guess5 = null;
		# PVector guess6 = null;
		# PVector guess7 = null;

		guess1 = None
		guess2 = None
		guess3 = None
		guess4 = None
		guess5 = None
		guess6 = None
		guess7 = None

		isRightSide = side == "r"

		if(isRightSide):
			guess1 = calcXY(diffs[0], M1)
			guess2 = calcXY(diffs[1], M1)
			guess3 = calcXY(diffs[2], M1)
			guess4 = calcXY(diffs[3], M1)
			guess5 = calcXY(diffs[4], M1)
			guess6 = calcXY(diffs[5], M1)
			guess7 = calcXY(diffs[6], M1)
		else:
			guess1 = calcXY(diffs[0], M1)
			guess2 = calcXY(diffs[1], M1)
			guess3 = calcXY(diffs[2], M1)
			guess4 = calcXY(diffs[3], M1)
			guess5 = calcXY(diffs[4], M1)
			guess6 = calcXY(diffs[5], M1)
			guess7 = calcXY(diffs[6], M1)

		# boolean isRightSide = false;
		# if (serialData.contains("r}")) {
		# 	isRightSide = true; 
		# 	guess1 = calcXY(timings1, mc1_r);
		# 	guess2 = calcXY(timings2, mc2_r);
		# 	guess3 = calcXY(timings3, mc3_r);
		# 	guess4 = calcXY(timings4, mc4_r);
		# 	guess5 = calcXY(timings5, mc5_r);
		# 	guess6 = calcXY(timings6, mc6_r);
		# 	guess7 = calcXY(timings7, mc7_r);
		# } else if (serialData.contains("l}")) {
		# 	guess1 = calcXY(timings1, mc1_l);
		# 	guess2 = calcXY(timings2, mc2_l);
		# 	guess3 = calcXY(timings3, mc3_l);
		# 	guess4 = calcXY(timings4, mc4_l);
		# 	guess5 = calcXY(timings5, mc5_l);
		# 	guess6 = calcXY(timings6, mc6_l);
		# 	guess7 = calcXY(timings7, mc7_l);
		# 	isRightSide = false;
		# }

		# println("guess 1: " + guess1.x + ", " + guess1.y);
		# println("guess 2: " + guess2.x + ", " + guess2.y);
		# println("guess 3: " + guess3.x + ", " + guess3.y);
		# println("guess 4: " + guess4.x + ", " + guess4.y);
		# println("guess 5: " + guess5.x + ", " + guess5.y);
		# println("guess 6: " + guess6.x + ", " + guess6.y);
		# println("guess 7: " + guess7.x + ", " + guess7.y);

		x_inches = (guess1.x + guess2.x + guess3.x + guess4.x + guess5.x + guess6.x + guess7.x) / 7
		y_inches = (guess1.y + guess2.y + guess3.y + guess4.y + guess5.y + guess6.y + guess7.y) / 7
		print(x_inches + ", " + y_inches)

		return [x_inches, y_inches, isRightSide, self.TABLE_WIDTH, self.TABLE_HEIGHT]

		# float x_inches = (guess1.x+guess2.x+guess3.x+guess4.x+guess5.x+guess6.x+guess7.x)/7;
		# float y_inches = (guess1.y + guess2.y + guess3.y + guess4.y + guess5.y + guess6.y + guess7.y)/7;
		# println(x_inches + ", " + y_inches);

		# return new Hit(x_inches, y_inches, isRightSide, TABLE_WIDTH, TABLE_HEIGHT);



	def update(self, setState, isPressed, pygame):
		screen = pygame.display.get_surface()

		if isPressed(pygame.K_ESCAPE):
			setState(0)

		hit_string = self.read_hit(self.arduino_serial)
		parse = self.parse_hit(hit_string)
		side = parse["side"]
		diffs = self.generate_diffs(parse)
		hit = getHit(side, diffs)

		lastHit = get_hit()
		pygame.draw.circle(
			screen, 
			(150, 0, 0), 
			(self.lastHit[0] * self.SCREEN_MULITPLIER, 
			self.lastHit[1] * self.SCREEN_MULITPLIER), 
			0.8 * self.SCREEN_MULITPLIER)

		text = self.font.render("Tracking State...", 1, (0, 0, 0))
		screen.blit(text, (5, 10))

 #	 void importCoeffs(String coefficientFile, boolean isRightSide) {
 #    String[] coeffs = loadStrings(coefficientFile);

 #    float[][] coeffs1 = new float[2][28];
 #    float[][] coeffs2 = new float[2][28];
 #    float[][] coeffs3 = new float[2][28];
 #    float[][] coeffs4 = new float[2][28];
 #    float[][] coeffs5 = new float[2][28];
 #    float[][] coeffs6 = new float[2][28];
 #    float[][] coeffs7 = new float[2][28];
 #    for (int i = 0; i < 28; i++) {
 #      coeffs1[0][i] = float(coeffs[i]);2
 #      coeffs2[0][i] = float(coeffs[28+i]);
 #      coeffs3[0][i] = float(coeffs[56+i]);
 #      coeffs4[0][i] = float(coeffs[84+i]);
 #      coeffs5[0][i] = float(coeffs[112+i]);
 #      coeffs6[0][i] = float(coeffs[140+i]);
 #      coeffs7[0][i] = float(coeffs[168+i]);
      
 #      coeffs1[1][i] = float(coeffs[196+i]); 
 #      coeffs2[1][i] = float(coeffs[224+i]);
 #      coeffs3[1][i] = float(coeffs[252+i]);
 #      coeffs4[1][i] = float(coeffs[280+i]);
 #      coeffs5[1][i] = float(coeffs[308+i]);
 #      coeffs6[1][i] = float(coeffs[336+i]);
 #      coeffs7[1][i] = float(coeffs[364+i]);
 #    }
 #    if (isRightSide) { 
 #      mc1_r = new matrixMath(coeffs1); 
 #      mc2_r = new matrixMath(coeffs2);
 #      mc3_r = new matrixMath(coeffs3);
 #      mc4_r = new matrixMath(coeffs4);
 #      mc5_r = new matrixMath(coeffs5);
 #      mc6_r = new matrixMath(coeffs6);
 #      mc7_r = new matrixMath(coeffs7);
 #    }
 #    else {
 #      mc1_l = new matrixMath(coeffs1);
 #      mc2_l = new matrixMath(coeffs2);
 #      mc3_l = new matrixMath(coeffs3);
 #      mc4_l = new matrixMath(coeffs4);
 #      mc5_l = new matrixMath(coeffs5);
 #      mc6_l = new matrixMath(coeffs6);
 #      mc7_l = new matrixMath(coeffs7);
 #    }
 #  }

 #  Hit readHit() {
 #     String serialData = null;
 #     if (debug) {
 #       if (random(100) <= 1) {
 #         serialData = "hit: {1908 1120 0 2004 1700 98 200 r}";
 #       } else if (random(100) <= 1) {
 #         serialData = "hit: {1544 668 0 1288 1700 569 1200 r}";
 #       }
 #       else {
 #         serialData = null;
 #       }
 #     } else if (arduinoSerial.available() > 0) {
 #       serialData = arduinoSerial.readStringUntil(10);  //10 is character for linefeed
 #     }  


 #    if (serialData == null) {
 #      return null;
 #    }
 #    else {
 #      println(serialData);
 #      Hit hit = getHit(serialData);
 #      // 54 x 60
 #      //println("(" + position.x + ", " + position.y + ")");
 #      return hit;
 #    }
 #  }

 #  private Hit getHit(String serialData) {
 #    String[] values = split(serialData, "{");
 #    String[] timings = split(values[1], " ");

 #    float t12 = float(timings[0])-float(timings[1]);
 #    float t13 = float(timings[0])-float(timings[2]);
 #    float t14 = float(timings[0])-float(timings[3]);
 #    float t15 = float(timings[0])-float(timings[4]);
 #    float t16 = float(timings[0])-float(timings[5]);
 #    float t17 = float(timings[0])-float(timings[6]);
 #    float t23 = float(timings[1])-float(timings[2]);
 #    float t24 = float(timings[1])-float(timings[3]);
 #    float t25 = float(timings[1])-float(timings[4]);
 #    float t26 = float(timings[1])-float(timings[5]);
 #    float t27 = float(timings[1])-float(timings[6]);
 #    float t34 = float(timings[2])-float(timings[3]);
 #    float t35 = float(timings[2])-float(timings[4]);
 #    float t36 = float(timings[2])-float(timings[5]);
 #    float t37 = float(timings[2])-float(timings[6]);
 #    float t45 = float(timings[3])-float(timings[4]);
 #    float t46 = float(timings[3])-float(timings[5]);
 #    float t47 = float(timings[3])-float(timings[6]);
 #    float t56 = float(timings[4])-float(timings[5]);
 #    float t57 = float(timings[4])-float(timings[6]);
 #    float t67 = float(timings[5])-float(timings[6]);
 #    /*int first_one = 0;
 #    int first_two = 0; 
 #    int first_four = 0;
 #    if (int(timings[0]) == 0) {
 #      first_one = 1;
 #    } else if (int(timings[1]) == 0) {
 #      first_two = 1;
 #    } else if (int(timings[3]) == 0) {
 #      first_four = 1;
 #    }*/

 #    float[] timings1 = {
 #      pow(t12,2), pow(t13,2), pow(t14,2), pow(t15,2), pow(t16,2), pow(t17,2),
 #      t12*t13, t12*t14, t12*t15, t12*t16, t12*t17, t13*t14, t13*t15, t13*t16, t13*t17, t14*t15, t14*t16, t14*t17, t15*t16, t15*t17, t16*t17, t12, t13, t14, t15, t16, t17, 1};
 #    float[] timings2 = {
 #      pow(t12,2), pow(t23,2), pow(t24,2), pow(t25,2), pow(t26,2), pow(t27,2), 
 #      t12*t23, t12*t24, t12*t25, t12*t26, t12*t27, t23*t24, t23*t25, t23*t26, t23*t27, t24*t25, t24*t26, t24*t27, t25*t26, t25*t27, t26*t27, t12, t23, t24, t25, t26, t27, 1};
 #    float[] timings3 = {
 #      pow(t13,2), pow(t23,2), pow(t34,2), pow(t35,2), pow(t36,2), pow(t37,2), 
 #      t13*t23, t13*t34, t13*t35, t13*t36, t13*t37, t23*t34, t23*t35, t23*t36, t23*t37, t34*t35, t34*t36, t34*t37, t35*t36, t35*t37, t36*t37, t13, t23, t34, t35, t36, t37, 1};
 #    float[] timings4 = {
 #      pow(t14,2), pow(t24,2), pow(t34,2), pow(t45,2), pow(t46,2), pow(t47,2),
 #      t14*t24, t14*t34, t14*t45, t14*t46, t14*t47, t24*t34, t24*t45, t24*t46, t24*t47, t34*t45, t34*t46, t34*t47, t45*t46, t45*t47, t46*t47, t14, t24, t34, t45, t46, t47, 1};
 #    float[] timings5 = {
 #      pow(t15,2), pow(t25,2), pow(t35,2), pow(t45,2), pow(t56,2), pow(t57,2),
 #      t15*t25, t15*t35, t15*t45, t15*t56, t15*t57, t25*t35, t25*t45, t25*t56, t25*t57, t35*t45, t35*t56, t35*t57, t45*t56, t45*t57, t56*t57, t15, t25, t35, t45, t56, t57, 1};  
 #    float[] timings6 = {
 #      pow(t16,2), pow(t26,2), pow(t36,2), pow(t46,2), pow(t56,2), pow(t67,2),
 #      t16*t26, t16*t36, t16*t46, t16*t56, t16*t67, t26*t36, t26*t46, t26*t56, t26*t67, t36*t46, t36*t56, t36*t67, t46*t56, t46*t67, t56*t67, t16, t26, t36, t46, t56, t67, 1};
 #    float[] timings7 = {
 #      pow(t17,2), pow(t27,2), pow(t37,2), pow(t47,2), pow(t57,2), pow(t67,2),
 #      t17*t27, t17*t37, t17*t47, t17*t57, t17*t67, t27*t37, t27*t47, t27*t57, t27*t67, t37*t47, t37*t57, t37*t67, t47*t57, t47*t67, t57*t67, t17, t27, t37, t47, t57, t67, 1};
        
 #    PVector guess1 = null;
 #    PVector guess2 = null;
 #    PVector guess3 = null;
 #    PVector guess4 = null;
 #    PVector guess5 = null;
 #    PVector guess6 = null;
 #    PVector guess7 = null;
   
 #    boolean isRightSide = false;
 #    if (serialData.contains("r}")) {
 #      isRightSide = true; 
 #      guess1 = calcXY(timings1, mc1_r);
 #      guess2 = calcXY(timings2, mc2_r);
 #      guess3 = calcXY(timings3, mc3_r);
 #      guess4 = calcXY(timings4, mc4_r);
 #      guess5 = calcXY(timings5, mc5_r);
 #      guess6 = calcXY(timings6, mc6_r);
 #      guess7 = calcXY(timings7, mc7_r);
 #    } else if (serialData.contains("l}")) {
 #      guess1 = calcXY(timings1, mc1_l);
 #      guess2 = calcXY(timings2, mc2_l);
 #      guess3 = calcXY(timings3, mc3_l);
 #      guess4 = calcXY(timings4, mc4_l);
 #      guess5 = calcXY(timings5, mc5_l);
 #      guess6 = calcXY(timings6, mc6_l);
 #      guess7 = calcXY(timings7, mc7_l);
 #      isRightSide = false;
 #    }
    
 #    println("guess 1: " + guess1.x + ", " + guess1.y);
 #    println("guess 2: " + guess2.x + ", " + guess2.y);
 #    println("guess 3: " + guess3.x + ", " + guess3.y);
 #    println("guess 4: " + guess4.x + ", " + guess4.y);
 #    println("guess 5: " + guess5.x + ", " + guess5.y);
 #    println("guess 6: " + guess6.x + ", " + guess6.y);
 #    println("guess 7: " + guess7.x + ", " + guess7.y);
    
 #    float x_inches = (guess1.x+guess2.x+guess3.x+guess4.x+guess5.x+guess6.x+guess7.x)/7;
 #    float y_inches = (guess1.y + guess2.y + guess3.y + guess4.y + guess5.y + guess6.y + guess7.y)/7;
 #    println(x_inches + ", " + y_inches);

 #    return new Hit(x_inches, y_inches, isRightSide, TABLE_WIDTH, TABLE_HEIGHT);
 #  }

 #  PVector calcXY(float[] timings, matrixMath mc) {
 #    matrixMath result = matrixMath.columnMultiplyMatrix(timings, mc);    
 #    float x = Math.max(0, Math.min(TABLE_WIDTH, result.getNumber(0, 0)));
 #    float y = Math.max(0, Math.min(TABLE_HEIGHT, result.getNumber(0, 1)));
 #    return new PVector(x, y);
 #  }
