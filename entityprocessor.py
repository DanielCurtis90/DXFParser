import ezdxf

def entity_processor(entity):
	if entity.dxftype() == 'LWPOLYLINE':
		return lwpolyline_extractor(entity)

def lwpolyline_extractor(entity):
	polyattr_list = []
	polyattr_list.append(f"Elevation: {entity.dxf.elevation}, ")
	polyattr_list.append(f"Point Information: ")
	for poly_point in entity.get_points():
		polyattr_list.append(f"Point: {poly_point}, ")
	polyattr_list.append(f"Is shape closed?: {entity.closed} ")
	return polyattr_list
