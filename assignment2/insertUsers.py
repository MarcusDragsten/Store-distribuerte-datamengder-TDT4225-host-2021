from DbConnector import DbConnector

class InsertUsers:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    def insertUsers(self):
        # Create an array for all users with labels
        labelFile = open("assignment2/labeled_ids.txt", "r")
        contentLabelFile = labelFile.read()
        labeledIds_list = contentLabelFile.splitlines()
        labelFile.close()

        # Create an array for all users
        userFile = open("assignment2/user_list.txt", "r")
        contentUserFile = userFile.read()
        allUsers_list = contentUserFile.splitlines()
        userFile.close()

        # Add the users, and check if they have a label
        for label in allUsers_list:
            has_label = 0
            if label in labeledIds_list:
                has_label = 1

            query = """INSERT INTO User VALUES ('%s', %s)
                    """

            self.cursor.execute(query % (label, has_label))
        self.db_connection.commit()


def main():
    program = None
    try:
        program = InsertUsers()
        program.insertUsers()
    except Exception as e:
        print("Error: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()
main()