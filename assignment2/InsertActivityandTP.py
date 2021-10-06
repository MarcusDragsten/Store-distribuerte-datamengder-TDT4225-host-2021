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
        for (path, dirs, files) in os.walk("C:/Users/Yoga/dataset/Data", topdown=True):

            # print(path)
            # print(dirs)
            # print(files)

            if path[len(path)-3:].isnumeric():
                actId = path[len(path)-3:]

                if "labels.txt" in files:
                    #print(actId)
                    label_path = path + "/labels.txt"
                    #print(label_path)
            
            if path[len(path)-10:] == "Trajectory":
                for plt in files:
                    plt_path = path + "/" + plt

                    if len(label_path) > 1:
                        labelAntall = txtRedskap.txtRedskap.labelAntall(label_path)
                        datoStartCVS = cvsRedskap.cvsRedskap.datoStartCSV(plt_path)
                        datoSluttCVS = cvsRedskap.cvsRedskap.datoSluttCSV(plt_path)

                        for i in range(labelAntall):
                            datoStartTXT = txtRedskap.txtRedskap.datoStartTXT(label_path, i)
                            datoSluttTXT = txtRedskap.txtRedskap.datoSluttTXT(label_path, i)
                            
                            




                        print("yeet")
                    else:
                        print("yeet")




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