#Kipling Crossing
import os

for filename in os.listdir():
    if '.csv' in filename:
        print(filename)
        f = open(filename,"r")
        f_new = open("Cobbity_"+filename,'w')


        for line in f:
            f_new.write(line.replace('-',',-'))
            #print(line.replace('-',',-').split())

        f.close()
        f_new.close()
