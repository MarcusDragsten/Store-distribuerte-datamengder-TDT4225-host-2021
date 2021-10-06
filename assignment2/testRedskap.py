import cvsRedskap as redCvs
import txtRedskap as redTxt

datoStart= redCvs.cvsRedskap.datoStartCSV("test.plt")

# print(datoStart)
# print(datoStart[0])
# print(datoStart[1])

datoSlutt= redCvs.cvsRedskap.datoSluttCSV("test.plt")
# print(datoSlutt)
# print(datoSlutt[0])
# print(datoSlutt[1])

godkjentLiner = redCvs.cvsRedskap.godkjentLinerCSV("test.plt")
# print(godkjentLiner)


startDatoTxt = redTxt.txtRedskap.datoStartTXT("labels.txt", 0)
# print("Halooo", startDatoTxt)

sluttDatoTxt = redTxt.txtRedskap.datoSluttTXT("labels.txt", 0)
# print(sluttDatoTxt)

mode = redTxt.txtRedskap.hentMode("labels.txt", 1)
# print(mode)

#print(datoStart)
#print(startDatoTxt)

print(datoSlutt)
print(sluttDatoTxt)

if datoStart == startDatoTxt and datoSlutt == sluttDatoTxt:
    print("Seier")

