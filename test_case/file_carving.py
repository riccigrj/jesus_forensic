
from image_dissect import *
from output_image_dissect import *
import mmap
import binascii
from file_signature import FileSignature

def file_carving(fileimage):
	with open(fileimage, "rb") as f:
		for signature in FileSignature.get_file_signatures():
			print(signature)

		#print(f.read()[18086400:18086912])

