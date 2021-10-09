from DbConnector import DbConnector
from tabulate import tabulate

class CreateTables:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    def create_userTable(self):
        query = """CREATE TABLE IF NOT EXISTS User (
                    id VARCHAR(255) NOT NULL PRIMARY KEY,
                    has_labels BOOLEAN)
                """
        self.cursor.execute(query)
        self.db_connection.commit()

    def create_activityTable(self):
        query = """CREATE TABLE IF NOT EXISTS Activity (
                    id INT NOT NULL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    transportation_mode VARCHAR(255),
                    start_date_time DATETIME,
                    end_date_time DATETIME,
                    FOREIGN KEY (user_id) REFERENCES User(id))
                """
    
        self.cursor.execute(query)
        self.db_connection.commit()

    def create_trackpointTable(self):
        query = """CREATE TABLE IF NOT EXISTS TrackPoint (
                    id INT NOT NULL PRIMARY KEY,
                    activity_id INT NOT NULL,
                    lat DOUBLE,
                    lon DOUBLE,
                    altitude INT,
                    date_time DATETIME,
                    FOREIGN KEY (activity_id) REFERENCES Activity(id))
                """

        self.cursor.execute(query)
        self.db_connection.commit()

    def show_tables(self):
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))

def main():
    program = None
    try:
        program = CreateTables()
        program.create_userTable()
        program.create_activityTable()
        program.create_trackpointTable()
        program.show_tables()
    except Exception as e:
        print("Error: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()

if __name__ == '__main__':
    main()

