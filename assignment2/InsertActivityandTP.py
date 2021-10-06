from DbConnector import DbConnector
from tabulate import tabulate
import os
import txtRedskap
import csvRedskap

class InsertActivity:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    def insertActivity(self):
        label_path = ""
        activityID = 1
        trackPointID = 1

        for (path, dirs, files) in os.walk("C:/Users/Yoga/dataset/Data", topdown=True):


            # print(path)
            # print(dirs)
            # print(files)

            if path[len(path)-3:].isnumeric():
                userID = path[len(path)-3:]
                print(userID)

                if "labels.txt" in files:
                    label_path = path + "/labels.txt"
                    #print(label_path)
            
            if path[len(path)-10:] == "Trajectory":
                for plt in files:
                    
                    #print(files)
                    #print("Her går vi gjennom PLT-filer ---------------------------------------------------------------------------")
                    #print(plt)
                    plt_path = path + "/" + plt
                    datoStartCVS = csvRedskap.csvRedskap.datoStartCSV(plt_path)
                    datoSluttCVS = csvRedskap.csvRedskap.datoSluttCSV(plt_path)
                    #print("Her printer vi PLT-Pathen",plt_path)
                    #print(plt_path)

                    if len(label_path) > 1:
                        labelAntall = txtRedskap.txtRedskap.labelAntall(label_path)
                        #print(labelAntall)
                        #print("Her går vi gjennom alle labels")
                        for i in range(labelAntall):
                            
                            #print("inni for", i)
                            datoStartTXT = txtRedskap.txtRedskap.datoStartTXT(label_path, i)
                            datoSluttTXT = txtRedskap.txtRedskap.datoSluttTXT(label_path, i)
                            #print(datoStartCVS, datoStartTXT, datoSluttCVS, datoSluttTXT)
                            # if datoStartCVS == datoStartTXT:
                            #     print("teet")

                            if datoStartCVS == datoStartTXT and datoSluttCVS == datoSluttTXT and csvRedskap.csvRedskap.godkjentLinjerCSV(plt_path):
                                print(datoStartCVS, datoStartTXT, datoSluttCVS, datoSluttTXT)
                                transportationMode = txtRedskap.txtRedskap.hentMode(label_path, i)
                                print(transportationMode)
                                
                                actQuery = """INSERT INTO Activity VALUES (%s, '%s', '%s', '%s', '%s')
                                       """
                                self.cursor.execute(actQuery % (activityID, userID, transportationMode, datoStartCVS, datoSluttCVS))

                                for tp in range(csvRedskap.csvRedskap.linjerCSV(plt_path)):
                                    innholdPLT = csvRedskap.csvRedskap.innholdPLT(plt_path, tp)

                                    tpQuery = """INSERT INTO TrackPoint VALUES (%s, %s, '%s', '%s', %s, '%s')
                                        """
                                    self.cursor.execute(tpQuery % (trackPointID, activityID, innholdPLT[0], innholdPLT[1], innholdPLT[2], innholdPLT[3]))
                                    trackPointID+=1

                                self.db_connection.commit()

                                activityID+=1
                    
                    else:
                        if csvRedskap.csvRedskap.godkjentLinjerCSV(plt_path):
                                actQuery = """INSERT INTO Activity VALUES (%s, '%s', NULL, '%s', '%s')
                                       """
                                self.cursor.execute(actQuery % (activityID, userID, datoStartCVS, datoSluttCVS))

                                for tp in range(csvRedskap.csvRedskap.linjerCSV(plt_path)):
                                    innholdPLT = csvRedskap.csvRedskap.innholdPLT(plt_path, tp)

                                    tpQuery = """INSERT INTO TrackPoint VALUES (%s, %s, '%s', '%s', %s, '%s')
                                            """
                                    self.cursor.execute(tpQuery % (trackPointID, activityID, innholdPLT[0], innholdPLT[1], innholdPLT[2], innholdPLT[3]))
                                    trackPointID+=1
                                activityID+=1
                                self.db_connection.commit()

                label_path = ""


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