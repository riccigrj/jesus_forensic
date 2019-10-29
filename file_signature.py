#!/usr/bin/python3

from enum import Enum, IntEnum

class FileSignature(Enum):
	def __init__(self, desc, header, trailer):
		self.desc = desc
		self.header = header
		self.trailer = trailer

	JPG = ("JPG", b'\xff\xd8', b'\xff\xd9')
	PNG = ("PNG", b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', b'\x49\x45\x4E\x44\xAE\x42\x60')
	#BMP - Os outros 4 bytes significa size
	BMP = ("BMP", b'\x42\x4d', None)
	GIF = ("GIF", b'\x47\x49\x46\x38\x37\x61', b'\x00\x3B')
	TIF = ("TIF", b'\x49\x49', None)
	PCX = ("PCX", b'\x0A\x02\x01\x01', None)

	@classmethod
	def get_file_signatures(self):
		return [self.JPG, self.PNG, self.BMP, self.GIF, self.TIF, self.PCX]
