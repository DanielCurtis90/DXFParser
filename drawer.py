#Python file 
#TABLE 01: ('00', 'TABLE_NUMBER', [[25.456, 0.0, 0, 0, 0, 50.912, 25.45584412271637, 0, 0, 0, 25.456, 50.91168824543093, 0, 0, 0, 0.0, 25.45584412271637, 0, 0, 0]])
import os, sys
from entityprocessor import *

def shifted_bounds(shifted_dict):
	#Make sure this is shifted (no negative coords!)
	y_coords = []
	x_coords = []
	for value in shifted_dict.values():
		#dig into the first and second entries of the embedded coordinate list to get the x and y coordinates
		x_coords.append(value.xpoint)
		y_coords.append(value.ypoint)	
	bounds = [min(x_coords), max(x_coords), min(y_coords), max(y_coords)]
	return bounds

def blocks_to_eps(block_dict, INSERT):
	block_string = []
	Refd_Block = block_dict[INSERT.name]
	#Check if there are LWPOLYLINES to draw
	if hasattr(Refd_Block, 'lwpolylines'):
		#Write the start and move to the first point
		first_x = Refd_Block.lwpolylines[0].vertices[0].xpoint
		first_y = Refd_Block.lwpolylines[0].vertices[0].ypoint
		block_string.append(f"{first_x + INSERT.xpoint} {first_y + INSERT.ypoint} moveto\n")
		#iterate over remaining vertices (based on where the x coordinate for the second vertex is stored)
		for vertex in Refd_Block.lwpolylines[0].vertices[1:]:
			block_string.append(f"{vertex.xpoint + INSERT.xpoint} {vertex.ypoint + INSERT.ypoint} lineto\n")
		block_string.append(f"closepath\n({INSERT.ID}) show\n2 setlinewidth\n0.5 setgray\nstroke\n")
	return block_string

def draw_eps(shifted_dict, block_dict):
	bounds = shifted_bounds(shifted_dict)
	with open("Output/Map" + ".eps", "w") as outputfile:
		#Write the start and bounding box
		outputfile.write(f"%!PS-Adobe-3.1 EPSF-3.0\n%%BoundingBox: {bounds[0]} {bounds[2]} {bounds[1]} {bounds[3]}\n/Times-Roman findfont\n24 scalefont\nsetfont\n")
		for value in shifted_dict.values():
			#Draw the block at the coordinates of the INSERT, send the key to find the right block
			block_string = blocks_to_eps(block_dict, value)
			for code_line in block_string:
				outputfile.write(f"{code_line}")
		outputfile.write("showpage")

	return None