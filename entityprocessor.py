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

def lwpolyline_extractor(entity):
	attr_list = []
	attr_list.append(f"Elevation: {entity.dxf.elevation}, ")
	attr_list.append(f"Constant Line Width: {entity.dxf.const_width}, ")
	attr_list.append(f"Number of Vertices: {entity.dxf.count}, ")
	attr_list.append(f"Point Information: ")
	for poly_point in entity.get_points():
		attr_list.append(f"Point: {poly_point}, ")
	attr_list.append(f"Is shape closed?: {entity.closed} ")
	return attr_list

def lwpolyline_points(entity):
	coord_list = []
	for poly_point in entity.get_points():
		for coord in poly_point:
			coord_list.append(coord)
	return coord_list

def insert_extractor(entity):
	#assumes the passed in entity is an INSERT entity
	#not retrieving the text attribute, using that as key prior to calling this
	#additionally not pulling the assigned block name as we need to it key into the block dictionary
	insertattr_list = []
	
	insertattr_list.append(entity.dxf.insert)
	insertattr_list.append(entity.dxf.rotation)
	insertattr_list.append(entity.dxf.xscale)
	insertattr_list.append(entity.dxf.yscale)
	insertattr_list.append(entity.dxf.zscale)


	''' THIS MAY BE NEEDED LATER
	insertattr_list.append(f"Block Name: {entity.dxf.name}, ")
	insertattr_list.append(f"Line Type: {entity.dxf.linetype}, ")
	insertattr_list.append(f"Color: {entity.dxf.color}, ")
	insertattr_list.append(f"Repeated Row Insertion Count: {entity.dxf.row_count}, ")
	insertattr_list.append(f"Repeated Row Insertion Spacing: {entity.dxf.row_spacing}, ")
	insertattr_list.append(f"Repeated Column Insertion Count: {entity.dxf.column_count}, ")
	insertattr_list.append(f"Repeated Column Insertion Spacing: {entity.dxf.column_spacing}, ")
	'''
	return insertattr_list

def line_extractor(entity):
	attr_list = []
	attr_list.append(f"Start Point: {entity.dxf.start}, ")
	attr_list.append(f"End Point: {entity.dxf.end}")
	return attr_list

def mtext_extractor(entity):
	attr_list = []
	attr_list.append(f"Text: {entity.get_text()}, ")
	attr_list.append(f"Insertion Point: {entity.dxf.insert}, ")
	attr_list.append(f"Character Height: {entity.dxf.char_height}, ")
	attr_list.append(f"Width: {entity.dxf.width}, ")
	attr_list.append(f"Attachment Point Flag: {entity.dxf.attachment_point}, ")
	attr_list.append(f"Text Flow Direction Flag: {entity.dxf.flow_direction}, ")
	attr_list.append(f"Style: {entity.dxf.style}, ")
	if hasattr(entity, 'text_direction'):
		attr_list.append(f"Text Direction (Overrides Rotation!): {entity.dxf.text_direction}, ")
	attr_list.append(f"Rotation: {entity.dxf.rotation}, ")
	attr_list.append(f"Line Spacing Style Flag: {entity.dxf.line_spacing_style}, ")
	attr_list.append(f"Line Spacing Factor: {entity.dxf.line_spacing_factor}, ")
	return attr_list

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






	

