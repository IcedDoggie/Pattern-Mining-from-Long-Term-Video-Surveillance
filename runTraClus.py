import os
from os.path import isfile, join
from subprocess import call
import sys
import shutil
def runTraClus(day_to_analyze):
    dirpath = 'E:\Documents\MMU Studies\Python Scripts\TraClusAlgorithm\src'
    root = 'E:\Documents\MMU Studies\Python Scripts'
    
    cycle_days = 0
#    day_to_analyze = 1
    while cycle_days < 5:
    #	 filename = str(cycle_days) + "_cluster"
    #	filename = "Day_6_" + str(cycle_days)
        filename = "30_days_" + str(cycle_days + 1) + "_loop_" + str(day_to_analyze)
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







