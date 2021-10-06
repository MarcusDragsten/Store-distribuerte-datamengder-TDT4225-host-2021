import csv
class csvRedskap:


  def datoStartCSV(path):
    with open (path) as csv_file:
        firstLine =csv_file.readlines()[6]
        s= firstLine.split(",")
        ut = s[5] + " " + s[6][:8]
        return ut
        
  def datoSluttCSV(path):
    with open (path) as csv_file:
      finalLine =csv_file.readlines()[-1]
      s = finalLine.split(",")
      ut= s[5] + " " + s[6][:8]
      return ut
  

  def godkjentLinjerCSV(path):
       #Printer true hvis det er 2506 eller færre linjer
      return 2506 >= sum(1 for line in open(path))
      
  def linjerCSV(path):
        return sum(1 for line in open(path))-6

  def innholdPLT(path, i):
        i+=6
        with open (path) as csv_file:
          enLinje = csv_file.readlines()[i]
          s = enLinje.split(",")
          aResult = [s[0], s[1], s[3], s[5]+" "+ s[6][:8]]
          #print(aResult)
          return aResult
  #innholdPLT("test.plt", 0)    
          




