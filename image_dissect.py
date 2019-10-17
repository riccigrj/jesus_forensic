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

	def get_fat_boot(self,first_sector, last_sector):
		fatBootSector = self.get_sector(first_sector, last_sector)
		fatBoot = {}
		fatBoot["DESC_FAB"] = fatBootSector[FAT_RESERVED.START_DESC_FAB:FAT_RESERVED.END_DESC_FAB].decode("utf-8")
		fatBoot["DESC_MEDIA"] = fatBootSector[FAT_RESERVED.START_VOLUME_LABEL:FAT_RESERVED.END_VOLUME_LABEL].decode("ascii")
		fatBoot["BYTES_SECTOR"] = struct.unpack('<h', fatBootSector[FAT_RESERVED.START_BYTES_SECTOR:FAT_RESERVED.END_BYTES_SECTOR])[0]
		fatBoot["QTT_SECTORS_ALOC_TABLE"] = struct.unpack('<h', fatBootSector[FAT_RESERVED.START_QTT_SECTOR_ALOC_TABLE:FAT_RESERVED.END_QTT_SECTOR_ALOC_TABLE])[0]
		fatBoot["QTT_ALOC_TABLE"] = struct.unpack('<b', fatBootSector[FAT_RESERVED.START_QTT_ALOC_TABLE:FAT_RESERVED.END_QTT_ALOC_TABLE])[0]
		fatBoot["RESERVED_SECTORS"] = struct.unpack('<h',fatBootSector[FAT_RESERVED.START_RESERVED_SECTORS:FAT_RESERVED.END_RESERVED_SECTORS])[0]
		fatBoot["SECTORS_CLUSTER"] = struct.unpack('<b', fatBootSector[FAT_RESERVED.START_SECTOR_CLUSTER:FAT_RESERVED.END_SECTOR_CLUSTER])[0]
		fatBoot["QTT_ROOT_ENTRY"] = struct.unpack('<h',fatBootSector[FAT_RESERVED.START_QTT_ROOT_ENTRY:FAT_RESERVED.END_QTT_ROOT_ENTRY])[0]
		return fatBoot
	
	def get_fat_root_directory(self, first_sector,last_sector, qtt_root_entry):
		fatRootDirectorySector = self.get_sector(first_sector,last_sector)
		fatRootDirectory = {}
		files = []
		for i in range(0,qtt_root_entry):
			file = {}
			file["FILE_NAME"] = fatRootDirectorySector[FAT_ALOC_TABLE.START_FILE_NAME+(i*32):FAT_ALOC_TABLE.END_FILE_NAME+(i*32)]
			file["EXT_FILE"] = fatRootDirectorySector[FAT_ALOC_TABLE.START_EXT_FILE+(i*32):FAT_ALOC_TABLE.END_EXT_FILE+(i*32)]
			file["FILE_SIZE"] = struct.unpack('<l',fatRootDirectorySector[FAT_ALOC_TABLE.START_FILE_SIZE+(i*32):FAT_ALOC_TABLE.END_FILE_SIZE+(i*32)])[0]
			file["FISRT_CLUSTER"] = struct.unpack('<h',fatRootDirectorySector[FAT_ALOC_TABLE.START_FIRST_CLUSTER+(i*32):FAT_ALOC_TABLE.END_FIRST_CLUSTER+(i*32)])[0]
			files.append(file)
		fatRootDirectory["FILES"] = files
		return fatRootDirectory

	def get_fat_data(self,first_sector, cluster, sector_p_cluster, fat):
		sectors = cluster * sector_p_cluster
		cluster = self.get_sector(first_sector+sectors, first_sector+sectors+1)
		while (b'\xff' not in get_next_cluster(sectors, sector_p_cluster, fat)):
			nextCluster = struct.unpack('<h',get_next_cluster(cluster, sector_p_cluster, fat))
			cluster += get_fat_data(first_sector, nextCluster, fat)
		return (cluster)

	def get_next_cluster(self, sectors, fat):
		first = int((sectors/2)*3)
		return(fat[first:first+3])	

