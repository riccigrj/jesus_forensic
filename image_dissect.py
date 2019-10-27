#!/usr/bin/python3.6

import sys
import binascii
from dict_enum import *
import struct

def get_sector(first_sector,last_sector, sector_size, fileimage):
	first_sector = first_sector*sector_size
	last_sector = last_sector*sector_size
	with open(fileimage, "rb") as f:
		sectors = f.read()[first_sector:last_sector]
	return sectors

class MBRDissector():
	def __init__ (self, fileimage):
		self.fileimage = fileimage

	def get_mbr(self):
		mbrSector = get_sector(0,1,512, self.fileimage)
		listPartPri = []
		for i in range(1,4):
			partPri = {}
			part = mbrSector[(MBR.START_PART1+((i-1)*16)):(MBR.END_PART1+(i*16))]
			partPri["STATUS"] = binascii.hexlify(part[PART_MBR.START_STATUS:PART_MBR.END_STATUS])
			partPri["FIRST_SECTOR"] = struct.unpack('<I', part[PART_MBR.START_LBA_FIRST_SECTOR:PART_MBR.END_LBA_FIRST_SECTOR])[0]
			partPri["QTT_SECTOR"] = struct.unpack('<I', part[PART_MBR.START_QTT_SECTOR:PART_MBR.END_QTT_SECTOR])[0]
			partPri["LAST_SECTOR"] = partPri["FIRST_SECTOR"]+partPri["QTT_SECTOR"]-1
			typeP = struct.unpack('<b', part[PART_MBR.START_TYPE:PART_MBR.END_TYPE])[0]
			partPri["TYPE"] = TYPE.get_type(typeP)
			listPartPri.append(partPri)
		return listPartPri

class FATDissector():
	def __init__(self,partPri, fileimage):
		self.partPri = partPri
		self.fileimage = fileimage
		self.boot = self.get_fat_boot()
		self.root = self.get_root_directory()

	def get_fat_boot(self):
		fatBootSector = get_sector(self.partPri["FIRST_SECTOR"], self.partPri["FIRST_SECTOR"]+1, 512, self.fileimage)
		fatBoot = {}
		fatBoot["DESC_FAB"] = fatBootSector[FAT_RESERVED.START_DESC_FAB:FAT_RESERVED.END_DESC_FAB].decode("utf-8")
		fatBoot["BYTES_SECTOR"] = struct.unpack('<h', fatBootSector[FAT_RESERVED.START_BYTES_SECTOR:FAT_RESERVED.END_BYTES_SECTOR])[0]
		fatBoot["QTT_ALOC_TABLE"] = struct.unpack('<b', fatBootSector[FAT_RESERVED.START_QTT_ALOC_TABLE:FAT_RESERVED.END_QTT_ALOC_TABLE])[0]
		fatBoot["RESERVED_SECTORS"] = struct.unpack('<h',fatBootSector[FAT_RESERVED.START_RESERVED_SECTORS:FAT_RESERVED.END_RESERVED_SECTORS])[0]
		fatBoot["SECTORS_CLUSTER"] = struct.unpack('<b', fatBootSector[FAT_RESERVED.START_SECTOR_CLUSTER:FAT_RESERVED.END_SECTOR_CLUSTER])[0]
		fatBoot["QTT_ROOT_ENTRY"] = struct.unpack('<h',fatBootSector[FAT_RESERVED.START_QTT_ROOT_ENTRY:FAT_RESERVED.END_QTT_ROOT_ENTRY])[0]
		
		if(self.partPri["TYPE"] == TYPE.FAT32CHS):
			fatBoot["FIRST_CLUSTER_ROOT"] = struct.unpack('i',fatBootSector[FAT32_RESERVED.START_FIRST_ROOT_CLUSTER:FAT32_RESERVED.END_FIRST_ROOT_CLUSTER])[0]
			fatBoot["QTT_SECTORS_ALOC_TABLE_32"] = struct.unpack('i',fatBootSector[FAT32_RESERVED.START_QTT_SECTOR_ALOC_TABLE:FAT32_RESERVED.END_QTT_SECTOR_ALOC_TABLE])[0]
			fatBoot["ROOT_FIRST_SECTOR"] = ((fatBoot["QTT_SECTORS_ALOC_TABLE_32"]*2)+fatBoot["RESERVED_SECTORS"]+self.partPri["FIRST_SECTOR"])
			fatBoot["ROOT_LAST_SECTOR"] = fatBoot["ROOT_FIRST_SECTOR"] + fatBoot["SECTORS_CLUSTER"]
		else:
			fatBoot["QTT_SECTORS_ALOC_TABLE"] = struct.unpack('<h', fatBootSector[FAT16_RESERVED.START_QTT_SECTOR_ALOC_TABLE:FAT16_RESERVED.END_QTT_SECTOR_ALOC_TABLE])[0]
			fatBoot["ROOT_FIRST_SECTOR"] = (self.partPri["FIRST_SECTOR"]+fatBoot["RESERVED_SECTORS"]+(fatBoot["QTT_SECTORS_ALOC_TABLE"]*2))
			fatBoot["ROOT_LAST_SECTOR"] = fatBoot["ROOT_FIRST_SECTOR"]+int((fatBoot["QTT_ROOT_ENTRY"]*32)/fatBoot["BYTES_SECTOR"])
		return fatBoot

	def get_root_directory(self):
		fatRootDirectorySector = get_sector(self.boot["ROOT_FIRST_SECTOR"],self.boot["ROOT_LAST_SECTOR"],self.boot["BYTES_SECTOR"],self.fileimage)
		fatRootDirectory = {}
		files = []
		qtt = int(((self.boot["ROOT_LAST_SECTOR"]-self.boot["ROOT_FIRST_SECTOR"])*self.boot["BYTES_SECTOR"])/32)
		for i in range(0,qtt):
			file = {}
			file["FILE_NAME"] = fatRootDirectorySector[FAT_ALOC_TABLE.START_FILE_NAME+(i*32):FAT_ALOC_TABLE.END_FILE_NAME+(i*32)]
			file["EXT_FILE"] = fatRootDirectorySector[FAT_ALOC_TABLE.START_EXT_FILE+(i*32):FAT_ALOC_TABLE.END_EXT_FILE+(i*32)]
			file["FILE_SIZE"] = struct.unpack('<l',fatRootDirectorySector[FAT_ALOC_TABLE.START_FILE_SIZE+(i*32):FAT_ALOC_TABLE.END_FILE_SIZE+(i*32)])[0]
			file["FISRT_CLUSTER"] = struct.unpack('<h',fatRootDirectorySector[FAT_ALOC_TABLE.START_FIRST_CLUSTER+(i*32):FAT_ALOC_TABLE.END_FIRST_CLUSTER+(i*32)])[0]
			if file["FISRT_CLUSTER"]!= 0:
				files.append(file) 
			if self.partPri["TYPE"] == TYPE.FAT32CHS:
				file["FISRT_CLUSTER"] -= 3
			else:
				file["FISRT_CLUSTER"] -= 2

		fatRootDirectory["FILES"] = files
		return fatRootDirectory

	def get_data_non_fragmented(self, file):
		sector = (file["FISRT_CLUSTER"]) * self.boot["SECTORS_CLUSTER"]
		nCluster = int((file["FILE_SIZE"]/(self.boot["BYTES_SECTOR"] * self.boot["SECTORS_CLUSTER"])))
		if (file["FILE_SIZE"]%(self.boot["BYTES_SECTOR"] * self.boot["SECTORS_CLUSTER"])  != 0 ):
			nCluster+=1
		cluster = get_sector(self.boot["ROOT_LAST_SECTOR"]+sector, self.boot["ROOT_LAST_SECTOR"]+sector+nCluster, self.boot["BYTES_SECTOR"], self.fileimage)
		return (cluster)

