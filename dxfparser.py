import ezdxf
from entityprocessor import *


#parsed_dxf is a Drawing object in ezdxf
parsed_dxf = ezdxf.readfile("ScrapeMe.dxf")

modelspace = parsed_dxf.modelspace()

layers = parsed_dxf.layers

#Iterate through the Block space and extract the Entities within them
#First go through each block within the dxf file
with open("output.txt", "w") as outputfile:
    for block in parsed_dxf.blocks:
        outputfile.write(f"Block Name: {block.name} \n")
        #Now look through the entities within each block
        for block_entity in block:
            #Now classify and extract each subentity in each block
            outputinfo = entity_processor(block_entity)
            outputfile.write(f"Block-SubEntity Type: {block_entity.dxftype()} \n")
            outputfile.write(f"Attributes:  {outputinfo} \n")


#We're comparing the layer name to the entity name to extract entities layer by layer
with open("output.txt", "a") as outputfile:
    outputfile.write(f"Modelspace Entity Data by Layer")	
    for L in layers:
        L.on()
        outputfile.write(f"Layer name: {L.dxf.name} \n")
        for e in modelspace:
            if e.dxf.layer == L.dxf.name:
                outputinfo = entity_processor(e)
                outputfile.write(f"Entity Type: {e.dxftype()} \n")
                outputfile.write(f"Attributes:  {outputinfo} \n")

