#!/usr/bin/python3

import sys
from image_dissect import *
from output_image_dissect import *

fileimage = sys.argv[1]

if __name__ == "__main__":
	dissector = ImageDissect(fileimage)
	listPartPri = dissector.mbr(0,1)
	print(output_mbr(listPartPri))
	for partPri in listPartPri:
		fatBoot = dissector.get_fat_boot(partPri["first_sector"],partPri["first_sector"]+1)
		rootFirstSector = 0
		if (partPri["typePart"].cod == 11):
			print("FAT32")
			rootFirstSector = (partPri["first_sector"]+fatBoot["RESERVED_SECTORS"]+(fatBoot["QTT_SECTORS_ALOC_TABLE_32"]*2))+((fatBoot["FIRST_CLUSTER_ROOT"]+2) * fatBoot["SECTORS_CLUSTER"])
			print(rootFirstSector)
		else:
			rootFirstSector = (partPri["first_sector"]+fatBoot["RESERVED_SECTORS"]+(fatBoot["QTT_SECTORS_ALOC_TABLE"]*2))
		rootLastSector = rootFirstSector+int((fatBoot["QTT_ROOT_ENTRY"]*32)/fatBoot["BYTES_SECTOR"])
		rootDirectory = dissector.get_fat_root_directory(rootFirstSector,rootLastSector,fatBoot["QTT_ROOT_ENTRY"])
		fat = dissector.get_fat((partPri["first_sector"]+fatBoot["RESERVED_SECTORS"]),(partPri["first_sector"]+fatBoot["RESERVED_SECTORS"]+fatBoot["QTT_SECTORS_ALOC_TABLE"]))
		for file in rootDirectory["FILES"]:
			if (b'\xe5' in file["FILE_NAME"]):
				#First cluster of the data section has cluster ID 2
				print(file)
				data = dissector.get_fat_data_non_fragmented(file, rootLastSector, fatBoot)
				#print(data)

