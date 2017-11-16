import ezdxf

def entity_processor(entity):
	if entity.dxftype() == 'LWPOLYLINE':
		return lwpolyline_extractor(entity)
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

def insert_extractor(entity):
	insertattr_list = []
	insertattr_list.append(f"Block Name: {entity.dxf.name}, ")
	insertattr_list.append(f"Line Type: {entity.dxf.linetype}, ")
	insertattr_list.append(f"Color: {entity.dxf.color}, ")
	insertattr_list.append(f"Scaling Factor (X): {entity.dxf.xscale}, ")
	insertattr_list.append(f"Scaling Factor (Y): {entity.dxf.yscale}, ")
	insertattr_list.append(f"Scaling Factor (Z): {entity.dxf.zscale}, ")
	insertattr_list.append(f"Rotation: {entity.dxf.rotation}, ")
	insertattr_list.append(f"Repeated Row Insertion Count: {entity.dxf.row_count}, ")
	insertattr_list.append(f"Repeated Row Insertion Spacing: {entity.dxf.row_spacing}, ")
	insertattr_list.append(f"Repeated Column Insertion Count: {entity.dxf.column_count}, ")
	insertattr_list.append(f"Repeated Column Insertion Spacing: {entity.dxf.column_spacing}, ")
	insertattr_list.append(f"Insertion Point: {entity.dxf.insert}")
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



