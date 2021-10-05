import csv
import os



# for (root,dirs,files) in os.walk('Test', topdown=true):
#         print (root)
#         print (dirs)
#         print (files)
#         print ('--------------------------------')

with open ('test.plt') as csv_fileS:
    firstLine =csv_fileS.readlines()[6]
    y= firstLine.split(",")
    print(y[5], y[6])  

with open ('test.plt') as csv_fileE:
    #Finne sluttDato
    finalLine =csv_fileE.readlines()[-1]
    x = finalLine.split(",")
    print(x[5], x[6])



