import sys
import os
import time


filelist = os.listdir('directory goes here')

filecount = [x[4:7] for x in filelist]

filedigits = []
for val in filecount:
  if val.isdigit():
    filedigits.append(int(val))
  else:
    filedigits.append(0)

looper = max(filedigits)

find . -name "file3_*.png" -print0 | cat - <(echo -ne "montage.png\0") | xargs -0  montage -tile x4 -geometry +0+0




#need to loop through the files and stitch/montage the images together
