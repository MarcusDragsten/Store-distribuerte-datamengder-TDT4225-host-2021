class txtRedskap:

    def datoStartTXT(path, i):
        i+=1
        with open(path) as txtFil:
            start = txtFil.readlines()[i]
            start= start[:19]
            L=list(start)
            L[4] = "-"
            L[7] = "-"
            nyString = ''.join(map(str, L))
            return nyString

    def datoSluttTXT(path,i):
        i+=1
        with open(path) as txtFil:
            slutt = txtFil.readlines()[i]
            slutt = slutt[20:39]
            L=list(slutt)
            L[4] = "-"
            L[7] = "-"
            nyString = ''.join(map(str, L))
            return nyString


    def hentMode(path,i):
        i+=1
        with open(path) as txtFil:
            mode = txtFil.readlines()[i]
            return(mode[40:len(mode)-1])

    def labelAntall(path):
            return  sum(1 for line in open(path)) -1



