#!/usr/bin/python3

from enum import Enum, IntEnum

class FileSignature(Enum):
	def __init__(self, desc, header, trailer):
		self.desc = desc
		self.header = header
		self.trailer = trailer

	PNG = ("PNG", b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', b'\x49\x45\x4E\x44\xAE\x42\x60')