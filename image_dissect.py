#!/usr/bin/python3

import sys
import binascii
from dict_struct import *
import struct

sector_size = 512

class ImageDissect(object):
	def __init__(self, fileimage):
		self.fileimage = fileimage
		
	def get_sector(self,first_sector,last_sector):
		first_sector = first_sector*sector_size
		last_sector = last_sector*sector_size
		with open(self.fileimage, "rb") as f:
			sectors = f.read()[first_sector:last_sector]
		return sectors

	def mbr(self, first_sector, last_sector):
		mbrSector = self.get_sector(first_sector,last_sector)
		listPartPri = []
		for i in range(1,4):
			partPri = {}
			part = mbrSector[(MBR.START_PART1+((i-1)*16)):(MBR.END_PART1+(i*16))]
			partPri["status"] = binascii.hexlify(part[PART_MBR.START_STATUS:PART_MBR.END_STATUS])
			partPri["first_sector"] = struct.unpack('<I', part[PART_MBR.START_LBA_FIRST_SECTOR:PART_MBR.END_LBA_FIRST_SECTOR])[0]
			partPri["qtt_sectors"] = struct.unpack('<I', part[PART_MBR.START_QTT_SECTOR:PART_MBR.END_QTT_SECTOR])[0]
			partPri["last_sector"] = partPri["first_sector"]+partPri["qtt_sectors"]-1
			typeP = struct.unpack('<b', part[PART_MBR.START_TYPE:PART_MBR.END_TYPE])[0]
			partPri["typePart"] = TYPE.get_type(typeP)
			listPartPri.append(partPri)

		return listPartPri

	def fat(self,first_sector, last_sector):
		fatSector = self.get_sector(first_sector, last_sector)
		fat = {}
		fat["DESC_FAB"] = fatSector[FAT_RESERVED.START_DESC_FAB:FAT_RESERVED.END_DESC_FAB].decode("utf-8")
		fat["DESC_MEDIA"] = struct.unpack('<b',fatSector[FAT_RESERVED.STAR_DESC_MEDIA:FAT_RESERVED.END_DESC_MEDIA])
		return fat

		