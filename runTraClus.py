import os
from os.path import isfile, join
from subprocess import call
import sys
import shutil
def runTraClus(day_to_analyze, counter_list_day):
    dirpath = 'E:\Documents\MMU Studies\Python Scripts\TraClusAlgorithm\src'
    root = 'E:\Documents\MMU Studies\Python Scripts'

    filename = "test_day_" + str(counter_list_day) + "_" + str(day_to_analyze)
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

