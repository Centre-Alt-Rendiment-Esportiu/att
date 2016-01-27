import serial
import re
from math import fabs
import random as python_random

from numpy import *
from scipy import linalg

import pygame
#from graphics import *
 #                       PROJECTOR 
 #                           ^
 #                          / \
 #                         /   \
 #
 #                   y
 # (0,0)    |---------------------------------|
 # on right |        1 UL     |     10        |
 # side     |                 |               |  5,12 CENTER right, 6,13 CENTER up, 7,14 CENTER left
 #         x|  4 LL       2 UR| 9          11 |
 #          |                 |               |
 #          |       3 LR      |      8        |
 #          |---------------------------------| (0,0) on left side 
 #                                              (left as your back is to the projector -- e.g., screen's left)


DEBUG = False
DEBUG_INPUT = 'hitdata'
FILE_OUTPUT = 'coefficients'

BAUD = 115200
PORT = 2#5    # PORT = 5 means COM6. FOR WINDOWS
#PORT = '/dev/tty.usbserial-A9005d9p' # FOR MAC
SERIAL_TIMEOUT = .1 # in seconds

# the true positions of all the training points
# here, we use inches
positions = array([[6, 6],
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
REPETITIONS = 5

repeated_positions = array([[6, 6], [6, 6], [6, 6], [6, 6], [6, 6], 
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

TABLE_WIDTH = 60
TABLE_HEIGHT = 54
SCREEN_MULITPLIER = 14.6

#pt = Point(0, 0)
#curCir = Circle(pt, 0.25 * SCREEN_MULITPLIER)
#curCir.setOutline('red')
#curCir.setFill('red')

#label = Text(Point(TABLE_WIDTH / 2 * SCREEN_MULITPLIER, TABLE_HEIGHT * SCREEN_MULITPLIER), 'Loading...')




def open_serial(port, baud):
    """ Initializes the Arduino serial connection """
    arduino_serial = serial.Serial(port, baudrate=baud, timeout=SERIAL_TIMEOUT)
    return arduino_serial

def read_hit(arduino_serial):
    """ Gets a hit from the Arduino serial connection """
    
    while True:
        line = arduino_serial.readline()

        #print line
        
        if line == None or line == "":
            continue
        else:
            return line

def parse_hit(line):
    # print(line)
    hit_re = re.match("hit: {(?P<sensor_one>\d+):(?P<volume_one>\d+) (?P<sensor_two>\d+):(?P<volume_two>\d+) (?P<sensor_three>\d+):(?P<volume_three>\d+) (?P<sensor_four>\d+):(?P<volume_four>\d+) (?P<sensor_five>\d+):(?P<volume_five>\d+) (?P<sensor_six>\d+):(?P<volume_six>\d+) (?P<sensor_seven>\d+):(?P<volume_seven>\d+) (?P<sensor_eight>\d+):(?P<volume_eight>\d+) (?P<side>[lr])}", line)
    # hit_re = re.match("hit: {(?P<sensor_one>\d+) (?P<sensor_two>\d+) (?P<sensor_three>\d+) (?P<sensor_four>\d+) (?P<sensor_five>\d+) (?P<sensor_six>\d+) (?P<sensor_seven>\d+) (?P<sensor_eight>\d+) (?P<side>[lr])}", line)
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
        
        return generate_diffs(hit)
            
            
def generate_diffs(hit):
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
             "first_sensor": first_sensor
             }
    return diffs

# def generate_random_hit():
#     """ For DEBUG mode, generates hits without the arduino attached"""

#     hits = ["hit: {1404 1268 0 440 500 1200 81 r}", "hit: {2328 1240 0 1516 1700 600 200 l}", "hit: {1376 1944 1484 0 1700 98 400 l}"]
#     hit = python_random.choice(hits)
    
#     return parse_hit(hit)

def get_hits_from_file(is_right_side):
    filename = DEBUG_INPUT
    if is_right_side:
        filename += "-right.txt"
    else:
        filename += "-left.txt"
    
    reader = open(filename, 'r')
    lines = reader.readlines()
    lines = filter(lambda line: (line != "\n" and line[0] != "#"), lines)
    print lines
    return lines
    
def average_repetitions(repetitions):
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
         "first_sensor": repetitions[0]['first_sensor']
    }
    return averages
    


# def prompt_if_OK():
#     while(True):
#         user_response = raw_input("Were all the tests OK? Press enter if OK, or enter 'r' to redo: ")
#         if user_response == 'r':
#             return False
#         elif user_response == '':
#             return True
#         else:
#             print "Not a valid response. Please press enter or 'r', then enter."

    
def populate_matrices(training_values):
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
    
def write_vector(vector, output):
    for num in vector.flat:
        output.write("%.20f\n" % (num))

def train(arduino_serial, is_right_side):        
    training_values = collect_points(arduino_serial, is_right_side)
    [M1, M2, M3, M4, M5, M6, M7] = populate_matrices(training_values)
    
    # find inverses using singular value decomposition
    M1inv = linalg.pinv2(M1)
    M2inv = linalg.pinv2(M2)
    M3inv = linalg.pinv2(M3)
    M4inv = linalg.pinv2(M4)
    M5inv = linalg.pinv2(M5)
    M6inv = linalg.pinv2(M6)
    M7inv = linalg.pinv2(M7)
    
    print M1inv.shape
    print x.shape

    # find coefficients
    xCoeff1 = M1inv * x
    xCoeff2 = M2inv * x
    xCoeff3 = M3inv * x
    xCoeff4 = M4inv * x
    xCoeff5 = M5inv * x
    xCoeff6 = M6inv * x
    xCoeff7 = M7inv * x
    print xCoeff1

    yCoeff1 = M1inv * y
    yCoeff2 = M2inv * y
    yCoeff3 = M3inv * y
    yCoeff4 = M4inv * y
    yCoeff5 = M5inv * y
    yCoeff6 = M6inv * y
    yCoeff7 = M7inv * y
    print yCoeff1    
    return [xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7]

def write(is_right_side, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7):
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
    
    filename = FILE_OUTPUT
    if is_right_side:
        filename += "-right.txt"
    else:
        filename += "-left.txt"
    
    output = open(filename, 'w')
    write_vector(xCoeff1, output)
    write_vector(xCoeff2, output)
    write_vector(xCoeff3, output)
    write_vector(xCoeff4, output)
    write_vector(xCoeff5, output)
    write_vector(xCoeff6, output)
    write_vector(xCoeff7, output)
    write_vector(yCoeff1, output)
    write_vector(yCoeff2, output)
    write_vector(yCoeff3, output)
    write_vector(yCoeff4, output)
    write_vector(yCoeff5, output)
    write_vector(yCoeff6, output)
    write_vector(yCoeff7, output)    
    output.close()    


def error(xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7, is_right_side, lines, positions):  
    distances = []
    x_distances = []
    y_distances = []
    for point in range(len(lines)):
        hit_string = lines[point]
        diffs = parse_hit(hit_string)
        average = average_repetitions([diffs])
        [predicted_x, predicted_y] = predict(average, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7)
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
        
def test(xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7, is_right_side):
    ###############
    #    TEST     #
    ###############
    # test some points
    training_hits = None
    
    if not DEBUG:
        filename = DEBUG_INPUT
        if is_right_side:
            filename += "-right.txt"
        else:
            filename += "-left.txt"
        training_hits = open(filename, 'a')
    
    for i in range(20):
        print "TEST: hit the table somewhere"
        if DEBUG:
            diffs = generate_random_hit()
        else:
            diffs = read_hit(arduino_serial, training_hits)
            
        average = average_repetitions([ diffs ])
        [avgx, avgy] = predict(average, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7)

        print str(avgx) + " ," + str(avgy)

    if training_hits is not None:
        training_hits.close()

def predict(average, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7):
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

def collect_points(arduino_serial, is_right_side):
    training_values = []
    training_hits = None
    
    if DEBUG:
        lines = get_hits_from_file(is_right_side)
    else:
        filename = DEBUG_INPUT
        if is_right_side:
            filename += "-right.txt"
        else:
            filename += "-left.txt"
        training_hits = open(filename, 'w')
    
    for point in range(len(positions)): 
        #curCir.move(positions[point][1] * SCREEN_MULITPLIER, positions[point][0] * SCREEN_MULITPLIER)
        while(True):
            repetitions = []
            hit_strings = []
            for repetition in range(REPETITIONS):
              if is_right_side:
                side = "Right side, "
              else:
                side = "Left side, "
                print(side + "drop the ping pong ball at (%d,%d): repetition %d" % (positions[point][0], positions[point][1], repetition+1))
                
                if DEBUG:
                    hit_string = lines.pop(0)
                    diffs = parse_hit(hit_string)
                else:
                    hit_string = read_hit(arduino_serial)
                    diffs = parse_hit(hit_string)
                if diffs is not None:
                    repetitions.append(diffs)
                    hit_strings.append(hit_string)

            if not DEBUG:
                is_OK = prompt_if_OK()
                arduino_serial.flushInput()
            else:
                is_OK = True
                
            if (is_OK):
                for repetition in repetitions:
                    average = average_repetitions([ repetition ])
                    training_values.append(average)
                if not DEBUG:
                    training_hits.write(''.join(hit_strings))
                    training_hits.flush()
                break

    if training_hits is not None:
        training_hits.close()
    return training_values

INIT            = 'init'
CHOOSE_SIDE     = 'select_side'
COLLECT_INIT    = 'collect_init'
COLLECT         = 'collect'
COLLECT_PROMPT  = 'collect_prompt'
MATRICES        = 'matrices'

        
#pygame stuff
def main():
  # Init
  pygame.init()
  screen = pygame.display.set_mode((int(round(2 * 54 * SCREEN_MULITPLIER)), int(round(60 * SCREEN_MULITPLIER))))
  done = False

  state = INIT

  clock = pygame.time.Clock()

  if not DEBUG:
    arduino_serial = open_serial(PORT, BAUD)
  else:
    arduino_serial = None

  # Fill background
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((250, 250, 250))

  # Display some text
  font = pygame.font.Font(None, 36)
  text = font.render("Hello There", 1, (10, 10, 10))
  textpos = text.get_rect()
  textpos.centerx = background.get_rect().centerx
  background.blit(text, textpos)

  

  messages = array(
    ['Which side do you wish to calibrate?',
    'Drop the ball at the spot: {0}/5',
    'Would you like to proceed?'])

  curMsg = messages[0]
  is_right_side = False
  repetition = 0
  curSpot = 0

  isButtonUp = True

  repetitions = []
  hit_strings = []
  training_values = []
  training_hits = None

  filename = "hitdata"

  # filename = DEBUG_INPUT
  # if is_right_side:
  #     filename += "-right.txt"
  # else:
  #     filename += "-left.txt"
  # training_hits = open(filename, 'w')

  # Loop
  while not done:
    screen.fill((250, 250, 250))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        done = True
    
    pressed = pygame.key.get_pressed()

    # Display dots
    for point in range(len(positions)):
      # print point
      pygame.draw.circle(screen, (200, 200, 200), (positions[point][1] * SCREEN_MULITPLIER, positions[point][0] * SCREEN_MULITPLIER), 0.5 * SCREEN_MULITPLIER)
      pygame.draw.circle(screen, (200, 200, 200), ((TABLE_WIDTH + positions[point][1]) * SCREEN_MULITPLIER, positions[point][0] * SCREEN_MULITPLIER), 0.5 * SCREEN_MULITPLIER)

    # Listen for no button pressed
    if not(pressed[pygame.K_LEFT]) and not(pressed[pygame.K_RIGHT]):
      isButtonUp = True;

    # State machine
    if state == INIT:
      state = CHOOSE_SIDE

#    ________  ______  ____  _____ ______   _____ ________  ______
#   / ____/ / / / __ \/ __ \/ ___// ____/  / ___//  _/ __ \/ ____/
#  / /   / /_/ / / / / / / /\__ \/ __/     \__ \ / // / / / __/   
# / /___/ __  / /_/ / /_/ /___/ / /___    ___/ // // /_/ / /___   
# \____/_/ /_/\____/\____//____/_____/   /____/___/_____/_____/                                                         
    if state == CHOOSE_SIDE:
      curMsg = 'Which side do you wish to calibrate?'
      if pressed[pygame.K_LEFT] and isButtonUp:
        is_right_side = False
        state = COLLECT_INIT
        isButtonUp = False
      if pressed[pygame.K_RIGHT] and isButtonUp:
        is_right_side = True
        state = COLLECT_INIT
        isButtonUp = False
#    __________  __    __    __________________   _____   ____________
#   / ____/ __ \/ /   / /   / ____/ ____/_  __/  /  _/ | / /  _/_  __/
#  / /   / / / / /   / /   / __/ / /     / /     / //  |/ // /  / /   
# / /___/ /_/ / /___/ /___/ /___/ /___  / /    _/ // /|  // /  / /    
# \____/\____/_____/_____/_____/\____/ /_/    /___/_/ |_/___/ /_/     
    if state == COLLECT_INIT:
      repetition = 0

      training_values = []
      training_hits = None

      filename = DEBUG_INPUT
      if is_right_side:
          filename += "-right.txt"
      else:
          filename += "-left.txt"
      training_hits = open(filename, 'w')

      state = COLLECT
#    __________  __    __    __________________
#   / ____/ __ \/ /   / /   / ____/ ____/_  __/
#  / /   / / / / /   / /   / __/ / /     / /   
# / /___/ /_/ / /___/ /___/ /___/ /___  / /    
# \____/\____/_____/_____/_____/\____/ /_/     
    if state == COLLECT:
      # if is_right_side:
      #   side = "Right side, "
      # else:
      #   side = "Left side, "
      # curMsg = side + "drop the ball at the spot, %i/5" % (repetition)
      # # pygame.draw.circle(screen, (200, 20, 20), (positions[curSpot][1] * SCREEN_MULITPLIER, positions[curSpot][0] * SCREEN_MULITPLIER), 0.5 * SCREEN_MULITPLIER)

      # hit_string = read_hit(arduino_serial)
      # diffs = parse_hit(hit_string)

      # if diffs is not None:
      #   repetitions.append(diffs)
      #   hit_strings.append(hit_string)

      # repetition = repetition + 1

      # if repetition == REPETITIONS:
      #   state = COLLECT_PROMPT

      #OLD VERSION
      # training_values = []
      # training_hits = None
      
      # filename = DEBUG_INPUT
      # if is_right_side:
      #     filename += "-right.txt"
      # else:
      #     filename += "-left.txt"
      # training_hits = open(filename, 'w')
      
      for point in range(len(positions)): 
          #curCir.move(positions[point][1] * SCREEN_MULITPLIER, positions[point][0] * SCREEN_MULITPLIER)
          while(True):
              repetitions = []
              hit_strings = []
              for repetition in range(REPETITIONS):
                if is_right_side:
                  side = "Right side, "
                else:
                  side = "Left side, "
                  print(side + "drop the ping pong ball at (%d,%d): repetition %d" % (positions[point][0], positions[point][1], repetition+1))
                  

                  hit_string = read_hit(arduino_serial)
                  diffs = parse_hit(hit_string)

                  if diffs is not None:
                      repetitions.append(diffs)
                      hit_strings.append(hit_string)

              is_OK = prompt_if_OK()
              arduino_serial.flushInput()
                  
              if (is_OK):
                  for repetition in repetitions:
                      average = average_repetitions([ repetition ])
                      training_values.append(average)
                  training_hits.write(''.join(hit_strings))
                  training_hits.flush()
                  break

      if training_hits is not None:
          training_hits.close()
      # return training_values
      state = COLLECT_PROMPT
#    __________  __    __    __________________   ____  ____  ____  __  _______  ______
#   / ____/ __ \/ /   / /   / ____/ ____/_  __/  / __ \/ __ \/ __ \/  |/  / __ \/_  __/
#  / /   / / / / /   / /   / __/ / /     / /    / /_/ / /_/ / / / / /|_/ / /_/ / / /   
# / /___/ /_/ / /___/ /___/ /___/ /___  / /    / ____/ _, _/ /_/ / /  / / ____/ / /    
# \____/\____/_____/_____/_____/\____/ /_/    /_/   /_/ |_|\____/_/  /_/_/     /_/     
    if state == COLLECT_PROMPT:
        curMsg = "Where the drops ok?"
        #if(curSpot < len(positions)):
        # print curSpot
        pygame.draw.circle(screen, (150, 0, 0), (positions[curSpot][1] * SCREEN_MULITPLIER, positions[curSpot][0] * SCREEN_MULITPLIER), 0.8 * SCREEN_MULITPLIER)

        # if not DEBUG:
        # training_hits.write(''.join(hit_strings))
        # training_hits.flush()

        # curSpot = curSpot + 1
        # state = 'drop_left_init'

        if pressed[pygame.K_RIGHT] and isButtonUp:
            for r in repetitions:
                average = average_repetitions([r])
                training_values.append(average)
            training_hits.write(''.join(hit_strings))
            training_hits.flush()
            isButtonUp = False

            curSpot = curSpot + 1
            repetition = 0;
            arduino_serial.flushInput()
            state = COLLECT

            # training_hits.write(''.join(hit_strings))
            # training_hits.flush()

            # for repetition in repetitions:
#                     average = average_repetitions([ repetition ])
#                     training_values.append(average)
#                 if not DEBUG:
#                     training_hits.write(''.join(hit_strings))
#                     training_hits.flush()

        if(curSpot == len(positions)):
            if training_hits is not None:
                training_hits.close()
            state = MATRICES

            # return training_values
            # curSpot = curSpot + 1
            
        # else:
#     __  ______  __________  _____________________
#    /  |/  /   |/_  __/ __ \/  _/ ____/ ____/ ___/
#   / /|_/ / /| | / / / /_/ // // /   / __/  \__ \ 
#  / /  / / ___ |/ / / _, _// // /___/ /___ ___/ / 
# /_/  /_/_/  |_/_/ /_/ |_/___/\____/_____//____/  
    if state == MATRICES:     
        # if training_hits is not None:
        #     training_hits.close()
        #def train(arduino_serial, is_right_side):        
        #training_values = collect_points(arduino_serial, is_right_side)
        # print training_values
        [M1, M2, M3, M4, M5, M6, M7] = populate_matrices(training_values)

        # find inverses using singular value decomposition
        M1inv = linalg.pinv2(M1)
        M2inv = linalg.pinv2(M2)
        M3inv = linalg.pinv2(M3)
        M4inv = linalg.pinv2(M4)
        M5inv = linalg.pinv2(M5)
        M6inv = linalg.pinv2(M6)
        M7inv = linalg.pinv2(M7)

        print M1inv.shape
        print x.shape

        # find coefficients
        xCoeff1 = M1inv * x
        xCoeff2 = M2inv * x
        xCoeff3 = M3inv * x
        xCoeff4 = M4inv * x
        xCoeff5 = M5inv * x
        xCoeff6 = M6inv * x
        xCoeff7 = M7inv * x
        print xCoeff1

        yCoeff1 = M1inv * y
        yCoeff2 = M2inv * y
        yCoeff3 = M3inv * y
        yCoeff4 = M4inv * y
        yCoeff5 = M5inv * y
        yCoeff6 = M6inv * y
        yCoeff7 = M7inv * y
        print yCoeff1
        #return [xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7]

        # [xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7] = [xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7]
        write(False, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7)
        error(xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7, False, get_hits_from_file(False), repeated_positions)




# if side == 'l' or side == 'b':
    #    [xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7]
        # = train(arduino_serial, False)
    #    write(False, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7)
    #    error(xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7, False, get_hits_from_file(False), repeated_positions)



# def train(arduino_serial, is_right_side):        
#     training_values = collect_points(arduino_serial, is_right_side)
#     [M1, M2, M3, M4, M5, M6, M7] = populate_matrices(training_values)
    
#     # find inverses using singular value decomposition
#     M1inv = linalg.pinv2(M1)
#     M2inv = linalg.pinv2(M2)
#     M3inv = linalg.pinv2(M3)
#     M4inv = linalg.pinv2(M4)
#     M5inv = linalg.pinv2(M5)
#     M6inv = linalg.pinv2(M6)
#     M7inv = linalg.pinv2(M7)
    
#     print M1inv.shape
#     print x.shape

#     # find coefficients
#     xCoeff1 = M1inv * x
#     xCoeff2 = M2inv * x
#     xCoeff3 = M3inv * x
#     xCoeff4 = M4inv * x
#     xCoeff5 = M5inv * x
#     xCoeff6 = M6inv * x
#     xCoeff7 = M7inv * x
#     print xCoeff1

#     yCoeff1 = M1inv * y
#     yCoeff2 = M2inv * y
#     yCoeff3 = M3inv * y
#     yCoeff4 = M4inv * y
#     yCoeff5 = M5inv * y
#     yCoeff6 = M6inv * y
#     yCoeff7 = M7inv * y
#     print yCoeff1    
#     return [xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7]

# def collect_points(arduino_serial, is_right_side):
#     training_values = []
#     training_hits = None
    
#     if DEBUG:
#         lines = get_hits_from_file(is_right_side)
#     else:
#         filename = DEBUG_INPUT
#         if is_right_side:
#             filename += "-right.txt"
#         else:
#             filename += "-left.txt"
#         training_hits = open(filename, 'w')
    
#     for point in range(len(positions)): 
#         while(True):
#             repetitions = []
#             hit_strings = []
#             for repetition in range(REPETITIONS):
#               if is_right_side:
#                   side = "Right side, "
#               else:
#                   side = "Left side, "
#                 print(side + "drop the ping pong ball at (%d,%d): repetition %d" % (positions[point][0], positions[point][1], repetition+1))
                
#                 if DEBUG:
#                     hit_string = lines.pop(0)
#                     diffs = parse_hit(hit_string)
#                 else:
#                     hit_string = read_hit(arduino_serial)
#                     diffs = parse_hit(hit_string)
#                 if diffs is not None:
#                     repetitions.append(diffs)
#                     hit_strings.append(hit_string)

#             if not DEBUG:
#                 is_OK = prompt_if_OK()
#                 arduino_serial.flushInput()
#             else:
#                 is_OK = True
                
#             if (is_OK):
#                 for repetition in repetitions:
#                     average = average_repetitions([ repetition ])
#                     training_values.append(average)
#                 if not DEBUG:
#                     training_hits.write(''.join(hit_strings))
#                     training_hits.flush()
#                 break

#     if training_hits is not None:
#         training_hits.close()
#     return training_values

# def prompt_if_OK():
#     while(True):
#         user_response = raw_input("Were all the tests OK? Press enter if OK, or enter 'r' to redo: ")
#         if user_response == 'r':
#             return False
#         elif user_response == '':
#             return True
#         else:
#             print "Not a valid response. Please press enter or 'r', then enter."

# def populate_matrices(training_values):
#     M1 = []
#     M2 = []
#     M3 = []
#     M4 = []
#     M5 = []
#     M6 = []
#     M7 = []
    
#     for average in training_values:
#         t12 = average['ONE_TWO']
#         t13 = average['ONE_THREE']
#         t14 = average['ONE_FOUR']
#         t15 = average['ONE_FIVE']
#         t16 = average['ONE_SIX']
#         t17 = average['ONE_SEVEN']
#         t23 = average['TWO_THREE']
#         t24 = average['TWO_FOUR']
#         t25 = average['TWO_FIVE']
#         t26 = average['TWO_SIX']
#         t27 = average['TWO_SEVEN']
#         t34 = average['THREE_FOUR']
#         t35 = average['THREE_FIVE']
#         t36 = average['THREE_SIX']
#         t37 = average['THREE_SEVEN']
#         t45 = average['FOUR_FIVE']
#         t46 = average['FOUR_SIX']
#         t47 = average['FOUR_SEVEN']
#         t56 = average['FIVE_SIX']
#         t57 = average['FIVE_SEVEN']
#         t67 = average['SIX_SEVEN']
#         first_ul = int(average['first_sensor'] == 'one')
#         first_ur = int(average['first_sensor'] == 'two')
#         first_ll = int(average['first_sensor'] == 'four')
#         first_lr = int(average['first_sensor'] == 'three')
#         first_cl = int(average['first_sensor'] == 'five')
#         first_cu = int(average['first_sensor'] == 'six')
#         first_cr = int(average['first_sensor'] == 'seven')

#         # don't need first_lr because the other three 0/1 dummy variables take care of it, when they're all 0, the lin_reg knows this one is 1
#         # http://dss.princeton.edu/online_help/analysis/dummy_variables.htm
#         M1.append([t12**2, t13**2, t14**2, t15**2, t16**2, t17**2, t12*t13, t12*t14, t12*t15, t12*t16, t12*t17, t13*t14, t13*t15, t13*t16, t13*t17, t14*t15, t14*t16, t14*t17, t15*t16, t15*t17, t16*t17, t12, t13, t14, t15, t16, t17, 1])#, first_ul, first_ur, first_lr, first_ll, first_cl, first_cu, 1]
#         M2.append([t12**2, t23**2, t24**2, t25**2, t26**2, t27**2, t12*t23, t12*t24, t12*t25, t12*t26, t12*t27, t23*t24, t23*t25, t23*t26, t23*t27, t24*t25, t24*t26, t24*t27, t25*t26, t25*t27, t26*t27, t12, t23, t24, t25, t26, t27, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
#         M3.append([t13**2, t23**2, t34**2, t35**2, t36**2, t37**2, t13*t23, t13*t34, t13*t35, t13*t36, t13*t37, t23*t34, t23*t35, t23*t36, t23*t37, t34*t35, t34*t36, t34*t37, t35*t36, t35*t37, t36*t37, t13, t23, t34, t35, t36, t37, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])       
#         M4.append([t14**2, t24**2, t34**2, t45**2, t46**2, t47**2, t14*t24, t14*t34, t14*t45, t14*t46, t14*t47, t24*t34, t24*t45, t24*t46, t24*t47, t34*t45, t34*t46, t34*t47, t45*t46, t45*t47, t46*t47, t14, t24, t34, t45, t46, t47, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])        
#         M5.append([t15**2, t25**2, t35**2, t45**2, t56**2, t57**2, t15*t25, t15*t35, t15*t45, t15*t56, t15*t57, t25*t35, t25*t45, t25*t56, t25*t57, t35*t45, t35*t56, t35*t57, t45*t56, t45*t57, t56*t57, t15, t25, t35, t45, t56, t57, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
#         M6.append([t16**2, t26**2, t36**2, t46**2, t56**2, t67**2, t16*t26, t16*t36, t16*t46, t16*t56, t16*t67, t26*t36, t26*t46, t26*t56, t26*t67, t36*t46, t36*t56, t36*t67, t46*t56, t46*t67, t56*t67, t16, t26, t36, t46, t56, t67, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
#         M7.append([t17**2, t27**2, t37**2, t47**2, t57**2, t67**2, t17*t27, t17*t37, t17*t47, t17*t57, t17*t67, t27*t37, t27*t47, t27*t57, t27*t67, t37*t47, t37*t57, t37*t67, t47*t57, t47*t67, t57*t67, t17, t27, t37, t47, t57, t67, 1])#, first_ul, first_ur, first_ll, first_cl, first_cr, 1])
 
#     return [M1, M2, M3, M4, M5, M6, M7]

# def write(is_right_side, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7):
#     # File format:
#     # X1_1
#     # X1_2
#     # ...
#     # X1_28
#     # X2_1
#     # ...
#     # X2_28
#     # ...
#     # ...
#     # X7_28
#     # Y1_1
#     # ...
#     # ...
#     # Y7_28
    
#     filename = FILE_OUTPUT
#     if is_right_side:
#         filename += "-right.txt"
#     else:
#         filename += "-left.txt"
    
#     output = open(filename, 'w')
#     write_vector(xCoeff1, output)
#     write_vector(xCoeff2, output)
#     write_vector(xCoeff3, output)
#     write_vector(xCoeff4, output)
#     write_vector(xCoeff5, output)
#     write_vector(xCoeff6, output)
#     write_vector(xCoeff7, output)
#     write_vector(yCoeff1, output)
#     write_vector(yCoeff2, output)
#     write_vector(yCoeff3, output)
#     write_vector(yCoeff4, output)
#     write_vector(yCoeff5, output)
#     write_vector(yCoeff6, output)
#     write_vector(yCoeff7, output)    
#     output.close()    


    # curSpot = curSpot + 1
    # state = 'drop_left_init'

    #   for point in range(len(positions)):
    #     repetitions = []
    #     hit_strings = []
    #     #curCir.move(positions[point][1] * SCREEN_MULITPLIER, positions[point][0] * SCREEN_MULITPLIER)
    #     # while(True):

    #     for r in range(REPETITIONS):
    #       if is_right_side:
    #         side = "Right side, "
    #       else:
    #         side = "Left side, "
    #       curMsg = side + "drop the ball at (%d,%d): repetition %d" % (positions[point][0], positions[point][1], r+1)
    #       # print()
          
    #       # if DEBUG:
    #       #     hit_string = lines.pop(0)
    #       #     diffs = parse_hit(hit_string)
    #       # else:

    #       # hit_string = read_hit(arduino_serial)
    #       # diffs = parse_hit(hit_string)
    #       # if diffs is not None:
    #       #     repetitions.append(diffs)
    #       #     hit_strings.append(hit_string)

    #     # if not DEBUG:
    #     is_OK = prompt_if_OK()
    #     arduino_serial.flushInput()
    #     # else:
    #     #     is_OK = True
            
    #     if (is_OK):
    #         for repetition in repetitions:
    #             average = average_repetitions([ repetition ])
    #             training_values.append(average)
    #         # if not DEBUG:
    #         training_hits.write(''.join(hit_strings))
    #         training_hits.flush()
    #         break

    #     # if not DEBUG:
    #     #     is_OK = prompt_if_OK()
    #     #     arduino_serial.flushInput()
    #     # else:
    #     #     is_OK = True
            
    #     # if (is_OK):
    #     #     for repetition in repetitions:
    #     #         average = average_repetitions([ repetition ])
    #     #         training_values.append(average)
    #     #     if not DEBUG:
    #     #         training_hits.write(''.join(hit_strings))
    #     #         training_hits.flush()
    #     #     break

    

    #text = font.render(state, 1, (10, 10, 10))
    #background.blit(text, textpos)

    #text = font.render("{0}".format(curMsg), 1, (0,0,0))
    text = font.render(curMsg, 1, (0,0,0))
    screen.blit(text, (5, 10))
    #score += 1

    
    #if pressed[pygame.K_UP]: y -= 3
    #if pressed[pygame.K_DOWN]: y += 3
    #if pressed[pygame.K_LEFT]: x -= 3
    #if pressed[pygame.K_RIGHT]: x += 3
    
    #screen.fill((0, 0, 0))
    #if is_blue: color = (0, 128, 255)
    #else: color = (255, 100, 0)
    #pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
    
    pygame.display.flip()
    clock.tick(60)

if __name__ == '__main__': main()

#if __name__ == '__main__':
    #if not DEBUG:
    #    arduino_serial = open_serial(PORT, BAUD)
    #else:
    #    arduino_serial = None

    #win = GraphWin("Augmented Pingpong v0.3", 100, 100)
        
    #side = None
    #while side is None:
    #    side = raw_input("Calibrate [l]eft side only, [r]ight side only, or [b]oth?: ")
    #    if side != 'l' and side != 'r' and side != 'b':
    #        print 'Please enter l, r, or b.'
    #        side = None
    
    #if side == 'l' or side == 'b':
    #    [xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7] = train(arduino_serial, False)
    #    write(False, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7)
    #    error(xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7, False, get_hits_from_file(False), repeated_positions)
    #if side == 'r' or side == 'b':
    #    [xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7] = train(arduino_serial, True)
    #    write(True, xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7)
    #    error(xCoeff1, xCoeff2, xCoeff3, xCoeff4, xCoeff5, xCoeff6, xCoeff7, yCoeff1, yCoeff2, yCoeff3, yCoeff4, yCoeff5, yCoeff6, yCoeff7, True, get_hits_from_file(True), repeated_positions)

# TRAIN 
#   COLLECT_POINTS 
#     READ_HIT 
#     PARSE_HIT 
#     PROMPT_IF_OK 
#     AVERAGE_REPITIONS 
#   POPULATE_MATRICES 
# WRITE 


# train(arduino_serial, False)
  # training_values = collect_points(arduino_serial, is_right_side)
    # hit_string = read_hit(arduino_serial)
    # diffs = parse_hit(hit_string)

    # is_OK = prompt_if_OK()
    # arduino_serial.flushInput()

    # average = average_repetitions([ repetition ])

    # training_hits.write(''.join(hit_strings))
    # training_hits.flush()
  # [M1, M2, M3, M4, M5, M6, M7] = populate_matrices(training_values)

# write()