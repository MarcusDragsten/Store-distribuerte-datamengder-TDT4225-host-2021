from pymongo import collection
from DbConnector import DbConnector
import os
import Utils
from datetime import datetime

class InsertData:

    def __init__(self):
        self.connection = DbConnector()
        self.client = self.connection.client
        self.db = self.connection.db

    # Method for inserting activities and trackpoints into the DB
    def insertData(self):
        label_path = ""
        activityID = 1
        trackPointID = 1

        #Remember to change the path if the code is to be tested.
        for (path, dirs, files) in os.walk("C:/Users/Yoga/dataset/Data", topdown=True):

            # Checks if the path ends with the user-number-folder > Use it as UserID
            if path[len(path)-3:].isnumeric():
                userID = path[len(path)-3:]
                print(userID)

                # Checks if the folder has a label > Creates path for the label
                if "labels.txt" in files:
                    label_path = path + "/labels.txt"
            activityIDs = []
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
                                # Initializing array for all the trackpoint-ids for referencing in the activity-collection
                                # Also initializing an array for the trackpoint-documents that are to be added into the DB
                                trackPointIDs = []
                                tpDocs = []

                                # Iterating through the plt-files to add the trackpoints into the database.
                                for tp in range(Utils.pltUtils.countLinesWithValue(plt_path)):
                                    tpContent = [Utils.pltUtils.fileContent(plt_path, tp)]
                                    tpDocs.append(
                                        {
                                            "_id": trackPointID,
                                            "lat": float(tpContent[0][0]),
                                            "lon": float(tpContent[0][1]),
                                            "altitude": int(tpContent[0][2]),
                                            "date_time": datetime.strptime(tpContent[0][3], '%Y-%m-%d %H:%M:%S'),
                                            "activity_id": activityID
                                        }
                                    )
                                    # Appending the trackpoint-ids for referencing in Activity
                                    # Incrementing the trackpoint-id
                                    trackPointIDs.append(trackPointID)
                                    trackPointID += 1
                                    
                                # Inserting the trackpoints into the TrackPoint collection
                                collection = self.db["TrackPoint"]
                                collection.insert_many(tpDocs)

                                # Extracting the transportation mode using an utility function
                                transportationMode = Utils.txtUtils.getMode(label_path, i)

                                # Initializing a document for the activity for adding into the Activity collection
                                # Since it has a label, adding the transportation mode to the activity
                                activityDoc = {
                                    "_id": activityID,
                                    "transportation_mode": transportationMode,
                                    "start_date_time": datetime.strptime(dateStartPLT, '%Y-%m-%d %H:%M:%S'),
                                    "end_date_time": datetime.strptime(dateEndPLT, '%Y-%m-%d %H:%M:%S'),
                                    "trackPoint_ids": trackPointIDs,
                                    "user_id": userID
                                }

                                # Inserting the document into the Activity collection
                                collection = self.db["Activity"]
                                collection.insert_one(activityDoc)

                                # Appending the activity-ids into an array for referencing in the user collection
                                # Incrementing the activity-id
                                activityIDs.append(activityID)
                                activityID += 1

                    # If the user-folder does not have a label, add it to the DB
                    # Mostly the same adding method as the if-content. Might extract it as a method.
                    else:
                        # Only validation is that the PLT has max 2500 lines.
                        if Utils.pltUtils.approvedLines(plt_path):
                            trackPointIDs = []
                            tpDocs = []

                            # Iterating through the plt-files, and adding the trackpoints to the tp-array
                            for tp in range(Utils.pltUtils.countLinesWithValue(plt_path)):
                                tpContent = [Utils.pltUtils.fileContent(plt_path, tp)]
                                tpDocs.append(
                                    {
                                        "_id": trackPointID,
                                        "lat": float(tpContent[0][0]),
                                        "lon": float(tpContent[0][1]),
                                        "altitude": int(tpContent[0][2]),
                                        "date_time": datetime.strptime(tpContent[0][3], '%Y-%m-%d %H:%M:%S'),
                                        "activity_id": activityID
                                    }
                                )

                                # Appending the trackpoint-ids to the tp-id-array
                                # Incrementing trackpoint-id
                                trackPointIDs.append(trackPointID)
                                trackPointID += 1

                            # Adding the trackpoints to the TrackPoint collection
                            collection = self.db["TrackPoint"]
                            collection.insert_many(tpDocs)

                            # Initializing the document for activity without transportation mode
                            activityDoc = {
                                "_id": activityID,
                                "start_date_time": datetime.strptime(dateStartPLT, '%Y-%m-%d %H:%M:%S'),
                                "end_date_time": datetime.strptime(dateEndPLT, '%Y-%m-%d %H:%M:%S'),
                                "trackPoint_ids": trackPointIDs,
                                "user_id": userID
                            }

                            # Inserting the activity into the Activity collection
                            collection = self.db["Activity"]
                            collection.insert_one(activityDoc)

                            # Appending the activity-ids to an array for referencing in the user collection
                            # Incrementing the activity-id
                            activityIDs.append(activityID)
                            activityID += 1
                
                # Initializing the user document wiht an id and the array with activity-ids for referencing
                userDoc = {
                    "_id": userID,
                    "activities_ids": activityIDs
                }

                # Inserting the user document into the user collection
                collection = self.db["User"]
                collection.insert_one(userDoc)

                # Reseting the label path and the id-arrays
                label_path = ""
                activityIDs = []
                trackPointIDs = []

def main():
    program = None
    try:
        program = InsertData()
        program.insertData()
    except Exception as e:
        print("Error: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()

if __name__ == '__main__':
    main()
