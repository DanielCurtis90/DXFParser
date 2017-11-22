#Python file 
#TABLE 01: ('00', 'TABLE_NUMBER', [[25.456, 0.0, 0, 0, 0, 50.912, 25.45584412271637, 0, 0, 0, 25.456, 50.91168824543093, 0, 0, 0, 0.0, 25.45584412271637, 0, 0, 0]])
import os, sys

def shifted_bounds(shifted_dict):
	#Make sure this is shifted (no negative coords!)
	y_coords = []
	x_coords = []
	for value in shifted_dict.values():
		#dig into the first and second entries of the embedded coordinate list to get the x and y coordinates
		x_coords.append(value[1][0][0])
		y_coords.append(value[1][0][1])	
	bounds = [max(x_coords), max(y_coords)]
	return bounds

def write_blocks(block_dict):
	for key in block_dict:
		coord_list = block_dict[key][2]
		#If there are no coordinates, do not write anything
		if coord_list != []:
				#Dig one deeper to find the correct list (it's double nested)
				coord_list = coord_list[0]
				#Find the parameters for the bounding box
				boundX = max(coord_list[0::5]) 
				boundY = max(coord_list[1::5])
				with open("Output/" + str(key) + ".eps", "w") as blockfile:
					#Write the start and move to the first point
					blockfile.write(f"%!PS-Adobe-3.1 EPSF-3.0\n%%BoundingBox: 0 0 {boundX} {boundY}\n{coord_list[0]} {coord_list[1]} moveto\n")
					#iterate over remaining vertices (based on where the x coordinate for the second vertex is stored)
					cooc = 5
					for coord in coord_list[5::5]:
						blockfile.write(f"{coord_list[cooc]} {coord_list[cooc + 1]} lineto\n")
						cooc += 5
					blockfile.write("closepath\n2 setlinewidth\n0.5 setgray\nstroke\nshowpage")

	return None

def blocks_to_eps(block_dict, key, XCoord, YCoord, INSERT_value):
	block_string = []

	coord_list = block_dict[key][2]
	#If there are no coordinates, do not write anything
	if coord_list != []:
		#Dig one deeper to find the correct list (it's double nested)
		coord_list = coord_list[0]
		#Write the start and move to the first point
		block_string.append(f"{coord_list[0] + XCoord} {coord_list[1] + YCoord} moveto\n")
		#iterate over remaining vertices (based on where the x coordinate for the second vertex is stored)
		cooc = 5
		for coord in coord_list[5::5]:
			block_string.append(f"{coord_list[cooc] + XCoord} {coord_list[cooc + 1] + YCoord} lineto\n")
			cooc += 5
		block_string.append(f"closepath\n({INSERT_value}) show\n2 setlinewidth\n0.5 setgray\nstroke\n")

	return block_string

def draw_eps(shifted_dict, block_dict):
	bounds = shifted_bounds(shifted_dict)
	with open("Output/Map" + ".eps", "w") as outputfile:
		#Write the start and bounding box
		outputfile.write(f"%!PS-Adobe-3.1 EPSF-3.0\n%%BoundingBox: 0 0 {bounds[0]} {bounds[1]}\n/Times-Roman findfont\n24 scalefont\nsetfont\n")
		for key in shifted_dict:
			#Get the X and Y coordinates and the BlockKey
			XCoord = shifted_dict[key][1][0][0]
			YCoord = shifted_dict[key][1][0][1]
			BlockKey = shifted_dict[key][0]
			#Draw the block at the coordinates of the INSERT, send the key to find the right block
			block_string = blocks_to_eps(block_dict, BlockKey, XCoord, YCoord, key)
			for code_line in block_string:
				outputfile.write(f"{code_line}")
		outputfile.write("showpage")

	return None