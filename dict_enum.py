#!/usr/bin/python3

from enum import Enum, IntEnum

class MBR(IntEnum):
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

class TYPE(Enum):
    def __init__(self, cod, label):
        self.cod = cod
        self.label = label

    FAT12 = (1, "FAT12")
    FAT16CHS = (6, "FAT16CHS")
    FAT32CHS = (11, "FAT32CHS")

    @classmethod
    def listType(self):
        return [self.FAT12, self.FAT16CHS, self.FAT32CHS]

    @classmethod
    def get_type(self,code):
        listT = self.listType()
        for typePart in listT:
            if code == typePart.cod:
                return typePart

class PART_MBR(IntEnum):
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

class FAT_RESERVED(IntEnum):
    START_BOOT = 0
    END_BOOT = 3
    START_DESC_FAB = 3
    END_DESC_FAB = 11
    START_BYTES_SECTOR = 11
    END_BYTES_SECTOR = 13
    START_SECTOR_CLUSTER = 13
    END_SECTOR_CLUSTER = 14
    START_RESERVED_SECTORS = 14
    END_RESERVED_SECTORS = 16
    START_QTT_ALOC_TABLE = 16
    END_QTT_ALOC_TABLE = 17
    START_QTT_ROOT_ENTRY = 17
    END_QTT_ROOT_ENTRY = 19
    STAR_DESC_MEDIA = 21
    END_DESC_MEDIA = 22


class FAT_ALOC_TABLE(IntEnum):
    START_FILE_NAME = 0
    END_FILE_NAME = 8
    START_EXT_FILE = 8
    END_EXT_FILE = 11
    START_FIRST_CLUSTER = 26
    END_FIRST_CLUSTER = 28
    START_FILE_SIZE = 28
    END_FILE_SIZE = 32

class FAT16_RESERVED(IntEnum):
    START_QTT_SECTOR_ALOC_TABLE = 22
    END_QTT_SECTOR_ALOC_TABLE = 24

class FAT32_RESERVED(IntEnum):
    START_FIRST_ROOT_CLUSTER = 44
    END_FIRST_ROOT_CLUSTER = 48
    START_QTT_SECTOR_ALOC_TABLE = 36
    END_QTT_SECTOR_ALOC_TABLE = 40