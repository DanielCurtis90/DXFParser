import ezdxf
from entityprocessor import *


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
                lwpolycoord_list.append(lwpolyline_points(block_entity))
            if block_entity.dxftype() == "ATTDEF":
                tag = block_entity.dxf.tag
                prompt = block_entity.dxf.prompt
                contains_attdef = True

        if contains_attdef:
            block_dict[new_block_key] = [tag, prompt, lwpolycoord_list]
    for key, value in block_dict.items():
        outputfile.write(f"Key Value Pair: {key}: {value}, \n")

with open("output.txt", "a") as outputfile:
    insert_dict = {}
    full_dict = {}
    for entity in modelspace:
        insert_list = []
        if entity.dxftype() == "INSERT":
            new_insert_key = None
            for attrib in entity.attribs():
                new_insert_key = attrib.dxf.text
            insert_list.append(entity.dxf.name)
            insert_list.append(insert_extractor(entity))
            insert_dict[new_insert_key] = [insert_list]
    
    for key, value in insert_dict.items():
        outputfile.write(f"Insert Key Value Pair: {key}: {value}, \n")
        inner_list = value[0]
        if key != None:
            full_dict[key] = [value, block_dict[inner_list[0]]]

    outputfile.write("\n")
    for key, value in full_dict.items():
        outputfile.write(f"Combined information: {key}: {value}, \n")
