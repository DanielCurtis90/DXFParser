#Python file 
#TABLE 01: ('00', 'TABLE_NUMBER', [[25.456, 0.0, 0, 0, 0, 50.912, 25.45584412271637, 0, 0, 0, 25.456, 50.91168824543093, 0, 0, 0, 0.0, 25.45584412271637, 0, 0, 0]])
import os, sys

def write_eps(blockdict):
	for key in blockdict:
		coord_list = blockdict[key][2]
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