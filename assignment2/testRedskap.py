import cvsRedskap as redCvs
import txtRedskap as redTxt

datoStart= redCvs.cvsRedskap.datoStartCSV("C:/Users\Yoga\Store-distribuerte-datamengder-TDT4225-host-2021/assignment2/test.plt")
print(datoStart)
print(datoStart[0])
print(datoStart[1])

datoSlutt= redCvs.cvsRedskap.datoSluttCSV("C:/Users\Yoga\Store-distribuerte-datamengder-TDT4225-host-2021/assignment2/test.plt")
print(datoSlutt)
print(datoSlutt[0])
print(datoSlutt[1])

godkjentLiner = redCvs.cvsRedskap.godkjentLinerCSV("C:/Users\Yoga\Store-distribuerte-datamengder-TDT4225-host-2021/assignment2/test.plt")
print(godkjentLiner)


startDatoTxt = redTxt.txtRedskap.datoStartTXT("C:/Users\Yoga\Store-distribuerte-datamengder-TDT4225-host-2021/assignment2/test.plt", 1)
print("hei", startDatoTxt)

sluttDatoTxt = redTxt.txtRedskap.datoSluttTXT("C:/Users\Yoga\Store-distribuerte-datamengder-TDT4225-host-2021/assignment2/test.plt", 1)
print(sluttDatoTxt)

mode = redTxt.txtRedskap.hentMode("C:/Users\Yoga\Store-distribuerte-datamengder-TDT4225-host-2021/assignment2/test.plt", 1)
print(mode)

