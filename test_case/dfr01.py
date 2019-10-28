#!/usr/bin/python3

from image_dissect import *
from output_image_dissect import *


def non_fragmented_file_fat (fileimage):
	mbrDissector = MBRDissector(fileimage)
	listPartPri = mbrDissector.get_mbr()
	print(output_mbr(listPartPri))
	for partPri in listPartPri:
		fatDissector = FATDissector(partPri, fileimage)
		fatBoot = fatDissector.boot
		fatRoot = fatDissector.root
		for file in fatRoot["FILES"]:
			if (b'\xe5' in file["FILE_NAME"]):
				#First cluster of the data section has cluster ID 2
				print(file)
				data = fatDissector.get_data_non_fragmented(file)
				name = file["FILE_NAME"].replace(b'\xe5', b'\x58').decode("utf-8")
				ext = file["EXT_FILE"].decode("utf-8")
				f = open(name+"."+ext, "w+")
				f.write(data.decode("utf-8"))
				f.close
