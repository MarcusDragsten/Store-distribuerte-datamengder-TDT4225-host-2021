import csv
class cvsRedskap:


  def datoStartCSV(path):
    with open (path) as csv_file:
        firstLine =csv_file.readlines()[6]
        s= firstLine.split(",")
        ut = s[5] + s[6]
        return ut
        
  def datoSluttCSV(path):
    with open (path) as csv_file:
      finalLine =csv_file.readlines()[-1]
      s = finalLine.split(",")
      ut= s[5]+ s[6]
      return ut
  

  def godkjentLinerCSV(path):
       #Printer true hvis det er 2506 eller færre linjer
      return 2506 >= sum(1 for line in open(path))

  def innholdPLT(path):
        with open (path) as csv_file:
          result = csv.reader(csv_file, delimiter=",")
          aResult = []
          jump=0
          for row in result:
                jump +=1
                if jump == 7:
                  print(row)
                  aResult +=[row[0] + row[1] + row[3] + row[5] + row[6]]   
          return aResult
          




