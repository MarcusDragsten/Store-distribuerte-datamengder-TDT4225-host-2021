class txtRedskap:

    def datoStartTXT(path, i):
        with open(path) as txtFil:
            start = txtFil.readlines()[i]
            return(start[:19])

    def datoSluttTXT(path,i):
        with open(path) as txtFil:
            slutt = txtFil.readlines()[i]
            return(slutt[20:39])

    def datoSluttTXT(path,i):
        with open(path) as txtFil:
            slutt = txtFil.readlines()[i]
            return(slutt[20:39])



    print(datoStartTXT("labels.txt",1) )
    print(datoSluttTXT("labels.txt",1) )