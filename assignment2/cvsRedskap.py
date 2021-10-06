class cvsRedskap:


  def datoStartCSV(path):
    with open (path) as csv_file:
        firstLine =csv_file.readlines()[6]
        s= firstLine.split(",")
        return s[5], s[6]
        
  def datoSluttCSV(path):
    with open (path) as csv_file:
      finalLine =csv_file.readlines()[-1]
      s = finalLine.split(",")
      return s[5], s[6]
  


  def godkjentLinerCSV(path):
      linjer=0
      for row in open(path):
        linjer+= 1
        #Printer true hvis det er 2506 eller færre linjer
      return 2506 >= linjer




# with open ('test.plt') as csv_fileS:
#     firstLine =csv_fileS.readlines()[6]
#     y= firstLine.split(",")
#     print(y[5], y[6])  

# with open ('test.plt') as csv_fileE:
#     #Finne sluttDato
#     finalLine =csv_fileE.readlines()[-1]
#     x = finalLine.split(",")
#     print(x[5], x[6])


