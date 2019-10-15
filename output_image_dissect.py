#!/usr/bin/python3

def output_mbr(listPartPri):
	output = "----- MBR -----\n"
	i = 0 
	for partPri in listPartPri:
		i+=1
		output += "----- PART"+str(i)+"-----\n"
		output += "STATUS = "+("BOOT (" if  partPri["status"] == "5a5a" else "INATIVA (")+str(partPri["status"])+")\n"
		output += "TYPE = "+ str(partPri["typePart"]) + "\n" 
		output += "FIRST SECTOR = "+ str(partPri["first_sector"]) + "\n"
		output += "QUANTITY OF SECTORS = "+str(partPri["qtt_sectors"])+"\n"
		output += "LAST SECTOR = "+str(partPri["last_sector"])+"\n\n"
	return output