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

            if path[len(path)-3:].isnumeric():
                userID = path[len(path)-3:]
                print(userID)

                if "labels.txt" in files:
                    label_path = path + "/labels.txt"
            
            if path[len(path)-10:] == "Trajectory":
                for plt in files:
                    plt_path = path + "/" + plt
                    datoStartCVS = csvRedskap.csvRedskap.datoStartCSV(plt_path)
                    datoSluttCVS = csvRedskap.csvRedskap.datoSluttCSV(plt_path)

                    if len(label_path) > 1:
                        labelAntall = txtRedskap.txtRedskap.labelAntall(label_path)
                        
                        for i in range(labelAntall):
                            datoStartTXT = txtRedskap.txtRedskap.datoStartTXT(label_path, i)
                            datoSluttTXT = txtRedskap.txtRedskap.datoSluttTXT(label_path, i)

                            if datoStartCVS == datoStartTXT and datoSluttCVS == datoSluttTXT and csvRedskap.csvRedskap.godkjentLinjerCSV(plt_path):
                                transportationMode = txtRedskap.txtRedskap.hentMode(label_path, i)
                                
                                actQuery = """INSERT INTO Activity VALUES (%s, '%s', '%s', '%s', '%s')
                                       """
                                self.cursor.execute(actQuery % (activityID, userID, transportationMode, datoStartCVS, datoSluttCVS))

                                for tp in range(csvRedskap.csvRedskap.linjerCSV(plt_path)):
                                    innholdPLT = csvRedskap.csvRedskap.innholdPLT(plt_path, tp)

                                    tpQuery = """INSERT INTO TrackPoint VALUES (%s, %s, '%s', '%s', %s, '%s')
                                        """
                                    self.cursor.execute(tpQuery % (trackPointID, activityID, innholdPLT[0], innholdPLT[1], innholdPLT[2], innholdPLT[3]))
                                    trackPointID+=1

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
                
                label_path = ""
        self.db_connection.commit()

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