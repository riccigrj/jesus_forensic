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
		alocTableFirstSector = (fatBoot["RESERVED_SECTORS"]+(fatBoot["QTT_SECTORS_ALOC_TABLE"]*2))
		alocTabaleLastSector = alocTableFirstSector+512
		fatAlocTable = dissector.fat_aloc_table(alocTableFirstSector,alocTabaleLastSector)
		print(fatBoot, fatAlocTable)

