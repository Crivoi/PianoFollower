import os
import re

path = 'C:\\Users\Lenovo\\Desktop\\Licenta2020CrivoiAndrei\\Licenta2020CrivoiAndrei\\samples\\grand_piano_samples'

for item in os.listdir(path):
    dst = item[:-1]
    print(dst)
    dst = path + '\\' + dst
    src = path + '\\' + item
    os.rename(src, dst)
   