import ezdxf
from entityprocessor import *
from drawer import *


#parsed_dxf is a Drawing object in ezdxf
parsed_dxf = ezdxf.readfile("ScrapeMe.dxf")

modelspace = parsed_dxf.modelspace()

layers = parsed_dxf.layers

#Iterate through the Block space and extract the Entities within them
#First go through each block within the dxf file
block_dict = {}
for block_ref in parsed_dxf.blocks:
    new_block_key = block_ref.name
    block_dict[new_block_key] = BLOCK(block_ref)

#Assign INSERT entities to a dictionary and initialize their objects
insert_dict = {}
for entity in modelspace:
    if entity.dxftype() == "INSERT":
        for attrib in entity.attribs():
            INSERT_ID = attrib.dxf.text
            insert_dict[INSERT_ID] = INSERT(entity)

#Zero the INSERT coordinates           
shifted_dict = (insertcoord_shift(insert_dict))

draw_eps(shifted_dict, block_dict)
