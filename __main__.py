import sys
from test_case.dfr01 import *

fileimage = sys.argv[1]

if __name__ == "__main__":
	non_fragmented_file_fat(fileimage)