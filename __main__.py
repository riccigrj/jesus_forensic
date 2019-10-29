import sys
from test_case.deleted_file_recovery import *
from test_case.file_carving import *

fileimage = sys.argv[1]

if __name__ == "__main__":
	#non_fragmented_file_fat(fileimage)
	file_carving(fileimage)