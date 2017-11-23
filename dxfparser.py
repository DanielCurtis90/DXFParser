import ezdxf
from entityprocessor import *
from drawer import *


#parsed_dxf is a Drawing object in ezdxf
parsed_dxf = ezdxf.readfile("ScrapeMe.dxf")

modelspace = parsed_dxf.modelspace()

layers = parsed_dxf.layers

#Iterate through the Block space and extract the Entities within them
#First go through each block within the dxf file
with open("output.txt", "w") as outputfile:
    block_dict = {}
    for block in parsed_dxf.blocks:
        new_block_key = block.name
        contains_attdef = False
        lwpolycoord_list = []
        for block_entity in block:
            if block_entity.dxftype() == "LWPOLYLINE":
                #append each set (list) of lwpolyline coordinates to a master list
                #this will generally appear to be two nested lists in the case of only one lwpolyline existing
                lwpolycoord_list.append(lwcoord_shift(lwpolyline_points(block_entity)))
            if block_entity.dxftype() == "ATTDEF":
                tag = block_entity.dxf.tag
                prompt = block_entity.dxf.prompt
                contains_attdef = True

        if contains_attdef and block.name != "None":
            block_dict[new_block_key] = tag, prompt, lwpolycoord_list
    for key, value in block_dict.items():
        outputfile.write(f"Block Key Value Pair: {key}: {value}, \n")

#Assign INSERT entities to a dictionary and initialize their objects
with open("output.txt", "a") as outputfile:
    insert_dict = {}
    for entity in modelspace:
        if entity.dxftype() == "INSERT":
            for attrib in entity.attribs():
                INSERT_ID = attrib.dxf.text
                insert_dict[INSERT_ID] = INSERT(entity)
    
    shifted_dict = (insertcoord_shift(insert_dict))
    

'''
    for key, value in insert_dict.items():
        outputfile.write(f"Insert Key Value Pair: {key}: {value}, \n")
    for key, value in shifted_dict.items():
        outputfile.write(f"Shifted Insert Key Value Pair: {key}: {value}, \n")
'''

draw_eps(shifted_dict, block_dict)
