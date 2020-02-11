import os

path = 'C:\\Users\Lenovo\\Desktop\\Licenta2020CrivoiAndrei\\Licenta2020CrivoiAndrei\\samples\\grand_piano_samples'

for item in os.listdir(path):
    dst = item.split(' ')[0] + ' ' + item.split(' ')[1].split('.')[0].upper() + '.wav'
    print(dst)
    dst = path + '\\' + dst
    src = path + '\\' + item
    os.rename(src, dst)