import sys
import os
import time

try:
    directory_name=sys.argv[1]
    print(directory_name)
except:
    print('Please pass directory_name')

filelist = os.listdir(directory_name)

filecount = [x[4:7] for x in filelist]

filedigits = []
for val in filecount:
  if val.isdigit():
    filedigits.append(int(val))
  else:
    filedigits.append(0)

looper = max(filedigits)

currentdir = os.getcwd()

os.chdir(directory_name)

for x in range(1,looper+1):
  montagename = "find . -name \"file%03d*.png\" -print0 | cat - <\(echo -ne \"montage%03d.png\"\) | xargs -0 montage -tile x4 -geometry +0+0" % (x, x)
  #send assembled system command
  os.system(montagename)
  
os.chdir(currentdir)

