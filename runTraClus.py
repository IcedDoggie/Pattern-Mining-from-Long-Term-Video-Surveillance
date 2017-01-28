import os
from os.path import isfile, join
from subprocess import call
import sys
import shutil

dirpath = 'E:\Documents\MMU Studies\Python Scripts\TraClusAlgorithm\src'
root = 'E:\Documents\MMU Studies\Python Scripts'
# 30_days_1_loop_0
# cycle_loop = 5
# cycle_counter = 1
# cycle_days = 0
# while cycle_counter <= cycle_loop:
# 	cycle_days = 0
# 	while cycle_days < 7:
# 		filename = str(sys.argv[1])
# 		filename = filename + "_days_" + str(cycle_counter) + "_loop_" + str(cycle_days)

# 		filename_tra = filename + ".tra"
# 		output = filename + ".txt" 
# 		print(filename_tra)

# 		os.chdir(dirpath)
# 		print(os.getcwd())
# 		# call(["java", "boliu.Main", filename_tra, output, "29", "8"])
# 		call(["java", "boliu.Main", filename_tra, output])
# 		os.chdir(root)
# 		cycle_days += 1

# 	cycle_counter += 1
#30_days_1_loop_3
cycle_days = 0
while cycle_days < 5:
#	 filename = str(cycle_days) + "_cluster"
#	filename = "Day_6_" + str(cycle_days)
    filename = "30_days_" + str(cycle_days + 1) + "_loop_3"
    filename_tra = filename + ".tra"
    filename_txt = filename + ".txt"
#    print(filename_tra)
    output = filename + ".txt"

	# move file to traclus src
    src = root + '\\' + filename_tra
    dst = dirpath + '\\' + filename_tra
    shutil.move(src, dst)
    
   
    
    os.chdir(dirpath)
    print(os.getcwd())
	# call(["java", "boliu.Main", filename_tra, output, "29", "8"])
    call(["java", "boliu.Main", filename_tra, output])
    
    src = dirpath + '\\' + filename_txt
    dst = root + '\\' + filename_txt
    shutil.move(src, dst) 
    
    os.chdir(root)
    cycle_days += 1







