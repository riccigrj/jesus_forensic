#!/usr/bin/python3

def output_mbr(listPartPri):
	output = "----- MBR -----\n"
	i = 0 
	for partPri in listPartPri:
		i+=1
		output += "----- PART"+str(i)+"-----\n"
		output += "STATUS = "+("BOOT (" if  partPri["STATUS"] == "5a5a" else "INATIVA (")+str(partPri["STATUS"])+")\n"
		output += "TYPE = "+ str(partPri["TYPE"]) + "\n" 
		output += "FIRST SECTOR = "+ str(partPri["FIRST_SECTOR"]) + "\n"
		output += "QUANTITY OF SECTORS = "+str(partPri["QTT_SECTOR"])+"\n"
		output += "LAST SECTOR = "+str(partPri["LAST_SECTOR"])+"\n\n"
	return output