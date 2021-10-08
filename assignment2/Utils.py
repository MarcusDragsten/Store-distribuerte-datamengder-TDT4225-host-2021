#This class is for txt files
class txtUtils:
    
    #Get the start date from the index i
    def dateStart(path, i):
        i+=1
        with open(path) as txtFil:
            start = txtFil.readlines()[i]
            start= start[:19]
            L=list(start)
            L[4] = "-"
            L[7] = "-"
            newString = ''.join(map(str, L))
            return newString

    #Get the end date from the index i
    def dateEnd(path,i):
        i+=1
        with open(path) as txtFil:
            end = txtFil.readlines()[i]
            end = end[20:39]
            L=list(end)
            L[4] = "-"
            L[7] = "-"
            newString = ''.join(map(str, L))
            return newString

    #Get the transportation mode from the index i
    def getMode(path,i):
        i+=1
        with open(path) as txtFil:
            mode = txtFil.readlines()[i]
            return(mode[40:len(mode)-1])

    #Count the lines in a file
    def countLines(path):
            return  sum(1 for line in open(path)) -1

#This class is for csv and in this case plt files
class pltUtils:
        
    #Get the start date 
    def dateStart(path):
        with open (path) as csv_file:
            firstLine =csv_file.readlines()[6]
            s= firstLine.split(",")
            output = s[5] + " " + s[6][:8]
            return output

    #Get the end date  
    def dateEnd(path):
        with open (path) as csv_file:
            finalLine =csv_file.readlines()[-1]
            s = finalLine.split(",")
            output= s[5] + " " + s[6][:8]
            return output

    #Returns true if there is a maximum of 2500 
    # lines of usable content in the file
    def approvedLines(path):
        return 2506 >= sum(1 for line in open(path))

    #This method is not used. If the dataset is increased a lot, 
    # it may be appropriate to use it
    def bufcount(filename):
        f = open(filename)                  
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.read # loop optimization

        buf = read_f(buf_size)
        while buf:
            lines += buf.count('\n')
            buf = read_f(buf_size)
        return lines

    #Returns the number of lines in the file with usable values
    def countLinesWithValue(path):
            return sum(1 for line in open(path))-6

    #Returns a tuple with the values from the line i
    def fileContents(path, i):
            i+=6
            with open (path) as csv_file:
                oneLine = csv_file.readlines()[i]
                s = oneLine.split(",")
                tResults = (s[0], s[1], s[3], s[5]+" "+ s[6][:8])
                return tResults
