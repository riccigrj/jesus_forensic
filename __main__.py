#!/usr/bin/python3

import sys
from image_dissect import *
from output_image_dissect import *

fileimage = sys.argv[1]

if __name__ == "__main__":
	dissector = ImageDissect(fileimage)
	listPartPri = dissector.mbr(0,1)
	for partPri in listPartPri:
		fatBoot = dissector.fat_boot(partPri["first_sector"],partPri["first_sector"]+1)
		rootFirstSector = (partPri["first_sector"]+fatBoot["RESERVED_SECTORS"]+(fatBoot["QTT_SECTORS_ALOC_TABLE"]*2))
		rootLastSector = rootFirstSector+32 #32
		rootDirectory = dissector.fat_aloc_table(rootFirstSector,rootLastSector)
		for file in rootDirectory["FILES"]:
			if (b'\xe5' in file["FILE_NAME"]):
				data = dissector.get_data_fat(rootLastSector, file["FISRT_CLUSTER"]-2,fatBoot["SECTORS_CLUSTER"])
				print(file)

