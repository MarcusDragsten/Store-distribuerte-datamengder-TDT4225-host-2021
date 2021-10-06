class txtRedskap:

    def datoStartTXT(path, i):
        with open(path) as txtFil:
            start = txtFil.readlines()[i]
            return(start[:19])

    def datoSluttTXT(path,i):
        with open(path) as txtFil:
            slutt = txtFil.readlines()[i]
            return(slutt[20:39])

    def hentMode(path,i):
        with open(path) as txtFil:
            mode = txtFil.readlines()[i]
            return(mode[40:])

    def labelAntall(path):
            return  sum(1 for line in open(path)-1)



test= "kuyfiwayefwefg333"
print(test[len(test)-3:])
