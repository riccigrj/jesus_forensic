from enum import Enum

class MBR(Enum):
	START_PROTECT = 444
	END_PROTECT = 446
	START_PART1 = 446
	END_PART1 = 462
	START_PART2 = 462
	END_PART2 = 478
	START_PART3 = 478
	END_PART3 = 494
	START_PART4 = 494
	END_PART4 = 510
	START_SIGNATUREF = 510
	END_SIGNATUREF = 512

class Type(Enum):
	FAT12 = 1
	FAT16CHS = 6
	FAT32CHS = 11

	@classmethod
	def listType(self):
		listT = []
		listT.append(m.value for m in Type)
		return listT

	@classmethod
	def get_type(self,code):
		for m in listType():
			if code == i:
				return i

class Part_MBR(Enum):
	START_STATUS = 0 
	END_STATUS = 1
	START_CHS_FIST_SECTOR = 1
	END_CHS_FIST_SECTOR = 4
	START_TYPE = 4
	END_TYPE = 5
	START_CHS_LAST_SECTOR = 5
	END_CHS_LAST_SECTOR = 8
	START_LBA_FIRST_SECTOR = 8
	END_LBA_FIRST_SECTOR = 12
	START_QTT_SECTOR = 12
	END_QTT_SECTOR = 16