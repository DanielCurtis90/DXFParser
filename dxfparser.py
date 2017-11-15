import ezdxf
from entityprocessor import *

#parsed_dxf is a Drawing object in ezdxf
parsed_dxf = ezdxf.readfile("ScrapeMe.dxf")

modelspace = parsed_dxf.modelspace()

layers = parsed_dxf.layers

#we're comparing the layer name to the entity name to extract entities layer by layer
with open("output.txt", "w") as outputfile:
    	for L in layers:
    		L.on()
    		outputfile.write(f"Layer name: {L.dxf.name} \n")
    		for e in modelspace:
    			if e.dxf.layer == L.dxf.name:
    				outputinfo = entity_processor(e)
    				outputfile.write(f"Entity Type: {e.dxftype()} \n")
    				outputfile.write(f"Attributes:  {outputinfo} \n")




#This outputs the entities and their type found in the model space (does not output any paper space)
#with open("output.txt", "w") as outputfile:
#    	for e in modelspace:
#    		outputfile.write("DXF Entity: %s\n" % e.dxftype())
			
#block_layout = parsed_dxf.blocks.__iter__()

#with open("output.txt", "a") as outputfile:
#	outputfile.write("Block Layout Information \n")
#	for BL in block_layout:
		
		#Need to grab info from individual blocks too, make a list for each block layout of attributes.
#		block_attibutes = BL.block.tag
#		
#		outputfile.write(f"Block Name: {BL.name} {block_attibutes}\n")