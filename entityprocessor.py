import ezdxf

def entity_processor(entity):
	if entity.dxftype() == 'LWPOLYLINE':
		#return lwpolyline_extractor(entity)
		return lwpolyline_points(entity)
	elif entity.dxftype() == 'INSERT':
		return insert_extractor(entity)
	elif entity.dxftype() == 'LINE':
		return line_extractor(entity)
	elif entity.dxftype() == 'MTEXT':
		return mtext_extractor(entity)
	else:
		return "No Extractor defined for this Entity type"

def lwpolyline_points(entity):
	coord_list = []
	for poly_point in entity.get_points():
		for coord in poly_point:
			coord_list.append(coord)
	return coord_list

class VERTEX:
	def __init__(self, vertex_info):
		self.xpoint = vertex_info[0]
		self.ypoint = vertex_info[1]
		self.startw = vertex_info[2]
		self.endw = vertex_info[3]
		self.bulge = vertex_info[4]

class LWPOLYLINE:
	def __init__(self, entity):
		#As the amount of vertices in a LWPOLYLINE can be any number, we need to create a list
		vertices = []
		#Returns a list of vertex information (another list)
		for point in entity.get_points():
			vertices.append(VERTEX(point))
		#Zero the coordinates
		x_coords = []
		y_coords = []
		for vertex in vertices:
			x_coords.append(vertex.xpoint)
			y_coords.append(vertex.ypoint)
		#For each entry in these x or y coordinate lists, increase them by the absolute value of the lowest negative number
		#This zeroes the coordinate system. Then round them to 3 decimal places. 
		#Only do this if the lowest number in the x or y coordinate list is a negative!
		shiftx_coords = [round(x + abs(min(x_coords)), 3) if min(x_coords) < 0 else round(x, 3) for x in x_coords]
		shifty_coords = [round(y + abs(min(y_coords)), 3) if min(y_coords) < 0 else round(y, 3) for y in y_coords]
		#Reassign the shifted coordinates
		for counter, vertex in enumerate(vertices):
			vertex.xpoint = shiftx_coords[counter]
			vertex.ypoint = shifty_coords[counter]
		self.vertices = vertices

class INSERT:
	def __init__(self, entity):
		for attrib in entity.attribs():
			self.ID = attrib.dxf.text
		self.name = entity.dxf.name
		self.rotation = entity.dxf.rotation
		self.xscale = entity.dxf.xscale
		self.yscale = entity.dxf.yscale
		self.zscale = entity.dxf.zscale
		self.xpoint = entity.dxf.insert[0] 
		self.ypoint = entity.dxf.insert[1] 
		self.zpoint = entity.dxf.insert[2] 

class BLOCK:
	def __init__(self, block_ref):
		self.name = block_ref.name
		#Go through each type of block entity and add them to lists of their type
		#Define the tag and prompt attributes from the ATTDEF blockentity
		for block_entity in block_ref:
			if block_entity.dxftype() == "LWPOLYLINE":
				self.lwpolylines = []
				self.lwpolylines.append(LWPOLYLINE(block_entity))
			elif block_entity.dxftype() == "ATTDEF":
				self.tag = block_entity.dxf.tag
				self.prompt = block_entity.dxf.prompt

def insertcoord_shift(insert_dict):
	x_coords = []
	y_coords = []
	shifted_dict = insert_dict
	for value in insert_dict.values():
		#dig into the first and second entries of the embedded coordinate list to get the x and y coordinates
		x_coords.append(value.xpoint)
		y_coords.append(value.ypoint)
	#For each entry in these x or y coordinate lists, increase them by the absolute value of the lowest negative number
	#This zeroes the coordinate system. Then round them to 3 decimal places. 
	#Only do this if the lowest number in the x or y coordinate list is a negative!
	shiftx_coords = [round(x + abs(min(x_coords)), 3) if min(x_coords) < 0 else round(x, 3) for x in x_coords]
	shifty_coords = [round(y + abs(min(y_coords)), 3) if min(y_coords) < 0 else round(y, 3) for y in y_coords]
	#Update the shifted coordinates
	for counter, value in enumerate(shifted_dict.values()):
		#update the rounded and shifted coordinates
		value.xpoint = shiftx_coords[counter]
		value.ypoint = shifty_coords[counter]
	return shifted_dict

def lwcoord_shift(coord_list):
	#Grab all x and y coordinates and put them into their own lists
	#Assumes input list is an integer!
	x_coords = coord_list[0::5]
	y_coords = coord_list[1::5]
	#For each entry in these x or y coordinate lists, increase them by the absolute value of the lowest negative number
	#This zeroes the coordinate system. Then round them to 3 decimal places. 
	#Only do this if the lowest number in the x or y coordinate list is a negative!
	shiftx_coords = [round(x + abs(min(x_coords)), 3) if min(x_coords) < 0 else round(x, 3) for x in x_coords]
	shifty_coords = [round(y + abs(min(y_coords)), 3) if min(y_coords) < 0 else round(y, 3) for y in y_coords]
	#Put the lists back together and keep the other info in the coord_list we acted upon
	stiched_list = coord_list
	stiched_list[0::5] = shiftx_coords
	stiched_list[1::5] = shifty_coords

	return stiched_list







	

