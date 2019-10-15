import sys
from image_dissect import *
from output_image_dissect import *

fileimage = sys.argv[1]

if __name__ == "__main__":
	dissector = ImageDissect(fileimage)
	listPartPri = dissector.mbr(0,1)
	for partPri in listPartPri:
		fat = dissector.fat(partPri["first_sector"],partPri["last_sector"])
		print(fat)
	#print(output_mbr(listPartPri))

