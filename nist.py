import sys
import io
import binascii
from mbr import MBR, Part_MBR, Type
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
	output = "----- MBR -----\n"
	mbr = get_sector(0,1)

	for i in range(1,4):
		part = mbr[(MBR.START_PART1+((i-1)*16)):(MBR.END_PART1+(i*16))]
		status = binascii.hexlify(part[Part_MBR.START_STATUS:Part_MBR.END_STATUS])
		first_sector = struct.unpack('<I', part[Part_MBR.START_LBA_FIRST_SECTOR:Part_MBR.END_LBA_FIRST_SECTOR])[0]
		qtt_sectors = struct.unpack('<I', part[Part_MBR.START_QTT_SECTOR:Part_MBR.END_QTT_SECTOR])[0]
		end_sector = first_sector+qtt_sectors-1
		typeP = struct.unpack('<b', part[Part_MBR.START_TYPE:Part_MBR.END_TYPE])[0]

		output += "----- PART"+str(i)+"-----\n"
		output += "STATUS = "+("BOOT (" if  status == "5a5a" else "INATIVA (")+status+")\n"
		output += "TYPE = "+ str(Type.get_type(typeP)) + "\n" 
		output += "FIRST SECTOR = "+ str(first_sector) + "\n"
		output += "QUANTITY OF SECTORS = "+str(qtt_sectors)+"\n"
		output += "LAST SECTOR = "+str(end_sector)+"\n\n"

	return output

def main():
	
		part1 = f.read()[MBR.START_PART1:MBR.END_PART1]
		print("---PART1---")
		val = struct.unpack( '<I', part1[Part_MBR.START_LBA_FIRST_SECTOR:Part_MBR.END_LBA_FIRST_SECTOR])
		print(val)
if __name__ == "__main__":
	print(mbr())