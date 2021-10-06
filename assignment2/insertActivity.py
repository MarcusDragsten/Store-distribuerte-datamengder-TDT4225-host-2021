import cvsRedskap as red

datoStart= red.cvsRedskap.datoStart("test.plt")
print(datoStart)
print(datoStart[0])
print(datoStart[1])

datoSlutt= red.cvsRedskap.datoSluttCSV("test.plt")
print(datoSlutt)
print(datoSlutt[0])
print(datoSlutt[1])

godkjentLiner = red.cvsRedskap.godkjentLinerCSV("test.plt")
print(godkjentLiner)
#Fungerer :) 

