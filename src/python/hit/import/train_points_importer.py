# -*- coding: utf-8 -*-

import re

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
				if coords_re is not None:
					str_X = the_match.group("x_coord")
					str_Y = the_match.group("y_coord")
					current_point = "("+str_X+","+str_Y+")"
			else:		
				groups = hit_re.findall(in_line)
				if groups is not None:
					sensor_timings = [x.split(":")[0] for x in groups[:-1]]
					#sensor_values = [x.split(":")[1] for x in groups[:-1]]
					out_lines.append(",".join(sensor_timings)+":"+current_point)
		
		return out_lines

	def from_file_to_file(self, str_input_file, str_output_file):
		
		in_lines = [line.strip() for line in open(str_input_file) ]
		out_lines = self.from_lines_to_lines(in_lines)

		f = open(str_output_file, "w")
		f.writelines([line+"\n" for line in out_lines])
		f.close()
		
if __name__ == '__main__':
	
	importer = TrainPointsImporter()

	str_input_file = "../../../arduino/data/train_points_references.txt"
	str_output_file = "../../../python/data/train_points_1.txt"
	importer.from_file_to_file(str_input_file, str_output_file)

	str_input_file = "../../../arduino/data/train_points_references_and_mid.txt"
	str_output_file = "../../../python/data/train_points_2.txt"
	importer.from_file_to_file(str_input_file, str_output_file)
