import cvsRedskap as redCvs
import txtRedskap as redTxt

datoStart= redCvs.cvsRedskap.datoStartCSV("test.plt")
print(datoStart)
print(datoStart[0])
print(datoStart[1])

datoSlutt= redCvs.cvsRedskap.datoSluttCSV("test.plt")
print(datoSlutt)
print(datoSlutt[0])
print(datoSlutt[1])

godkjentLiner = redCvs.cvsRedskap.godkjentLinerCSV("test.plt")
print(godkjentLiner)


startDatoTxt = redTxt.txtRedskap.datoStartTXT("labels.txt", 1)
print(startDatoTxt)

sluttDatoTxt = redTxt.txtRedskap.datoSluttTXT("labels.txt", 1)
print(sluttDatoTxt)

