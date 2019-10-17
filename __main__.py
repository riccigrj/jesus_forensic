#!/usr/bin/python3

import sys
from image_dissect import *
from output_image_dissect import *

fileimage = sys.argv[1]

if __name__ == "__main__":
	dissector = ImageDissect(fileimage)
	listPartPri = dissector.mbr(0,1)
	for partPri in listPartPri:
		fatBoot = dissector.get_fat_boot(partPri["first_sector"],partPri["first_sector"]+1)
		rootFirstSector = (partPri["first_sector"]+fatBoot["RESERVED_SECTORS"]+(fatBoot["QTT_SECTORS_ALOC_TABLE"]*2))
		rootLastSector = rootFirstSector+int((fatBoot["QTT_ROOT_ENTRY"]*32)/512)
		rootDirectory = dissector.get_fat_root_directory(rootFirstSector,rootLastSector,fatBoot["QTT_ROOT_ENTRY"])
		for file in rootDirectory["FILES"]:
			if (b'\xe5' in file["FILE_NAME"]):
				#First cluster of the data section has cluster ID 2
				data = dissector.get_fat_data(rootLastSector, (file["FISRT_CLUSTER"]-2),fatBoot["SECTORS_CLUSTER"])
				print(file)
		first = partPri["first_sector"]+fatBoot["RESERVED_SECTORS"]
		print(first)
		last = first + fatBoot["QTT_SECTORS_ALOC_TABLE"]
		print (dissector.get_next_cluster(4, dissector.get_sector(first,last)))

