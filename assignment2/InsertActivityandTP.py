from DbConnector import DbConnector
from tabulate import tabulate
import os
import txtRedskap
import cvsRedskap

class InsertActivity:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    def insertActivity(self):
        label_path = ""

        for (path, dirs, files) in os.walk("C:/Users/Yoga/dataset/Data", topdown=True):


            # print(path)
            # print(dirs)
            # print(files)

            if path[len(path)-3:].isnumeric():
                actId = path[len(path)-3:]

                if "labels.txt" in files:
                    print(actId)
                    label_path = path + "/labels.txt"
                    #print(label_path)
            
            if path[len(path)-10:] == "Trajectory":
                counterID = 1
                for plt in files:
                    #print(files)
                    print("Her går vi gjennom PLT-filer ---------------------------------------------------------------------------")
                    #print(plt)
                    plt_path = path + "/" + plt
                    print("Her printer vi PLT-Pathen",plt_path)
                    #print(plt_path)

                    if len(label_path) > 1:
                        labelAntall = txtRedskap.txtRedskap.labelAntall(label_path)
                        datoStartCVS = cvsRedskap.cvsRedskap.datoStartCSV(plt_path)
                        datoSluttCVS = cvsRedskap.cvsRedskap.datoSluttCSV(plt_path)
                        #print(labelAntall)
                        print("Her går vi gjennom alle labels")
                        for i in range(labelAntall):
                            
                            #print("inni for", i)
                            datoStartTXT = txtRedskap.txtRedskap.datoStartTXT(label_path, i)
                            datoSluttTXT = txtRedskap.txtRedskap.datoSluttTXT(label_path, i)
                            print(datoStartCVS, datoStartTXT, datoSluttCVS, datoSluttTXT)
                            # if datoStartCVS == datoStartTXT:
                            #     print("teet")

                            if datoStartCVS == datoStartTXT and datoSluttCVS == datoSluttTXT and cvsRedskap.cvsRedskap.godkjentLinerCSV(plt_path):
                                print(datoStartCVS, datoStartTXT, datoSluttCVS, datoSluttTXT)
                                transportationMode = txtRedskap.txtRedskap.hentMode(label_path, i)
                                
                                actQuery = """INSERT INTO Activity VALUES ('%s', %s, %s, %s, %s)
                                       """
                                
                                self.cursor.execute(actQuery % (counterID, actId, transportationMode, datoStartCVS, datoSluttCVS))



                label_path = ""

                        #print("yeet")
                    #else:
                        #print("else")




                # else:
                #     print("yeet")


                # if "labels.txt" in files:
                #     print("true", actId)
                # else:
                #     print("yeet") 


            #print(path[len(path)-3:])

        #query = """INSERT INTO Activity VALUES ('%s', %s, %s, %s, %s)
        #        """
        #self.cursor.execute(query % ())


def main():
    program = None
    try:
        program = InsertActivity()
        program.insertActivity()
    except Exception as e:
        print("Error: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()
main()