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
       #Printer true hvis det er 2506 eller færre linjer
      return 2506 >= sum(1 for line in open(path))




