# -*- coding: utf-8 -*-

import re

import numpy as np
#
# Import points from arduino format:
#	"hit: { [tstamp]:[level] [tstamp]:[level] ... [tstamp]:[level] [side]}"
#	from file: src/arduino/data/[file]
#
# To internal format:
#	"[tstamp],[tstamp], ... ,[tstamp],([x_coord],[y_coord])"
#	to file: src/python/data/[file]
#	
class TrainPointsImporter:
	def __init__(self):
		pass
	
	def from_lines_to_lines(self, in_lines):
		
		out_lines = []
		current_point = ""
		
		hit_pattern = "-?\d+:-?\d+|[lr]"
		hit_re = re.compile(hit_pattern)
		
		coords_pattern = "\((?P<x_coord>\d+)\,(?P<y_coord>\d+)\)"
		coords_re = re.compile(coords_pattern)
		
		for in_line in in_lines:
			if in_line.startswith("("):
				the_match = coords_re.match(in_line)
				#if the_match is not None:
				if the_match:
					str_X = the_match.group("x_coord")
					str_Y = the_match.group("y_coord")
					current_point = ""+str_X+","+str_Y+""
			else:		
				groups = hit_re.findall(in_line)
				if groups is not None:
					sensor_timings = [x.split(":")[0] for x in groups[:-1]]
					#sensor_values = [x.split(":")[1] for x in groups[:-1]]
					out_lines.append(current_point+","+",".join(sensor_timings))
		
		return out_lines

	def from_file_to_file(self, str_input_file, str_output_file):
		
		in_lines = [line.strip() for line in open(str_input_file) if line.strip() != ""]
		out_lines = self.from_lines_to_lines(in_lines)

		f = open(str_output_file, "w")
		f.writelines([line+"\n" for line in out_lines])
		f.close()
### afegit pel jordi 
	def line_to_line(self, line):
		
		out_line = []
		out_line = line['sensor_timings']
		out_line = [int(i) for i in out_line]
        
		return np.asarray(out_line)
"""
		current_point = ""
		
		hit_pattern = "-?\d+:-?\d+|[lr]"
		hit_re = re.compile(hit_pattern)
		
		coords_pattern = "\((?P<x_coord>\d+)\,(?P<y_coord>\d+)\)"
		coords_re = re.compile(coords_pattern)
		
		#for in_line in in_lines:
		if line.startswith("("):
			the_match = coords_re.match(line)
			#if the_match is not None:
			if the_match:
				str_X = the_match.group("x_coord")
				str_Y = the_match.group("y_coord")
				current_point = ""+str_X+","+str_Y+""
		else:		
			groups = hit_re.findall(line)
			if groups is not None:
				sensor_timings = [x.split(":")[0] for x in groups[:-1]]
				#sensor_values = [x.split(":")[1] for x in groups[:-1]]
				#out_lines.append(current_point+","+",".join(sensor_timings))
 				sensor_timings = [int(i) for i in sensor_timings] 
				out_line.append(sensor_timings) 
        
		return np.asarray(out_line)
"""        	

if __name__ == '__main__':
	
	importer = TrainPointsImporter()
	
	str_input_file = "../../../arduino/data/train_20160322_right.txt"
	str_output_file = "../../../python/data/train_points_20160322_right.txt"
	importer.from_file_to_file(str_input_file, str_output_file)

