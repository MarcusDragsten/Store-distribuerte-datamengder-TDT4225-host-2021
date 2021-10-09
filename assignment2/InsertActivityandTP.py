from DbConnector import DbConnector
import os
#import txtRedskap
#import csvRedskap
import Utils

class InsertActivityandTP:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    # Method for inserting activities and trackpoints into the DB
    def insertData(self):
        label_path = ""
        activityID = 1
        trackPointID = 1

        #Remember to change the path if the code is to be tested.
        for (path, dirs, files) in os.walk("C:/Users/Marcus/dataset/Data", topdown=True):
        
            # Checks if the path ends with the user-number-folder > Use it as UserID
            if path[len(path)-3:].isnumeric():
                userID = path[len(path)-3:]
                print(userID)

                # Checks if the folder has a label > Creates path for the label
                if "labels.txt" in files:
                    label_path = path + "/labels.txt"
            
            # Now checks the path if it ends with "Trajectory" > Goes through the plt-files
            if path[len(path)-10:] == "Trajectory":
                for plt in files:
                    plt_path = path + "/" + plt
                    dateStartPLT = Utils.pltUtils.dateStart(plt_path)
                    dateEndPLT = Utils.pltUtils.dateEnd(plt_path)

                    # Checks if the folder has a label
                    if len(label_path) > 1:
                        lenLabel = Utils.txtUtils.countLines(label_path)
                     
                        # Loops through the lines in the label and checks if it matches the plt-files
                        for i in range(lenLabel):
                            dateStartTXT = Utils.txtUtils.dateStart(label_path, i)
                            dateEndTXT = Utils.txtUtils.dateEnd(label_path, i)

                            # Checks if the plt has the correct start and end date, according to the label
                            # Also rejects all plt-files with more than 2500 lines
                            if dateStartPLT == dateStartTXT and dateEndPLT == dateEndTXT and Utils.pltUtils.approvedLines(plt_path):
                                transportationMode = Utils.txtUtils.getMode(label_path, i)
                                
                                # Query for adding the activities 
                                actQuery = """INSERT INTO Activity VALUES (%s, '%s', '%s', '%s', '%s')
                                        """
                                self.cursor.execute(actQuery % (activityID, userID, transportationMode, dateStartPLT, dateEndPLT))
                                self.db_connection.commit()

                                # Looping through the trackpoints and add it to array
                                # Append the IDs in a tuple and the rest of the fields from the helping function
                                pltArr = []
                                for tp in range(Utils.pltUtils.countLinesWithValue(plt_path)):
                                    pltArr.append((trackPointID, activityID) + Utils.pltUtils.fileContent(plt_path, tp))
                                    trackPointID+=1

                                # Query for adding the trackpoints
                                tpQuery = """INSERT INTO TrackPoint VALUES (%s, %s, %s, %s, %s, %s)
                                        """
                                # Runs execute many, to instert all trackpoings from a file at once.
                                self.cursor.executemany(tpQuery, pltArr)
                                self.db_connection.commit()
                                activityID+=1

                    # If the user-folder does not have a label, add it to the DB
                    # Mostly the same adding method as the if-content. Might extract it as a method.
                    else:
                        # Only validation is that the PLT has max 2500 lines.
                        if Utils.pltUtils.approvedLines(plt_path):
                                actQuery = """INSERT INTO Activity VALUES (%s, '%s', NULL, '%s', '%s')
                                        """
                                self.cursor.execute(actQuery % (activityID, userID, dateStartPLT, dateEndPLT))
                                self.db_connection.commit()

                                pltArr2 = []
                                for tp in range(Utils.pltUtils.countLinesWithValue(plt_path)):
                                    pltArr2.append((trackPointID, activityID) + Utils.pltUtils.fileContent(plt_path, tp))
                                    trackPointID+=1

                                tpQuery = """INSERT INTO TrackPoint VALUES (%s, %s, %s, %s, %s, %s)
                                            """
                                self.cursor.executemany(tpQuery, pltArr2)
                                self.db_connection.commit()
                                activityID+=1
                
                label_path = ""

def main():
    program = None
    try:
        program = InsertActivityandTP()
        program.insertData()
    except Exception as e:
        print("Error: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()
main()