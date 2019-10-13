import sys
import io
import binascii
from mbr import MBR, Part_MBR
import struct

fileimage = sys.argv[1]
sector_size = 512

def get_sector(first_sector,last_sector):
	first_sector = first_sector*sector_size
	last_sector = last_sector*sector_size
	with open(fileimage, "r") as f:
		sectors = f.read()[first_sector:last_sector]
	return sectors

def mbr():
	output = "----- MBR ----\n"
	mbr = get_sector(0,1)

	output += mbr[510:512]
	return output

def main():
	
		part1 = f.read()[MBR.START_PART1:MBR.END_PART1]
		print("---PART1---")
		val = struct.unpack( '<I', part1[Part_MBR.START_LBA_FIRST_SECTOR:Part_MBR.END_LBA_FIRST_SECTOR])
		print(val)
if __name__ == "__main__":
	print(mbr())