from logging import currentframe
from DbConnector import DbConnector
from tabulate import tabulate
from haversine import haversine, Unit
import datetime


class Part2:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    def task6(self):

        query = """SELECT
            User.id,
            TrackPoint.lat,
            TrackPoint.lon,
            TrackPoint.date_time
            FROM
            (
                (
                User
                INNER JOIN Activity ON User.id = Activity.user_id
                )
                INNER JOIN TrackPoint ON Activity.id = TrackPoint.activity_id
            )
            WHERE User.id = '003' or User.id = '004' or User.id = '006' or User.id = '007' or User.id = '030'
            ORDER BY
            TrackPoint.date_time ASC;
            """

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        tabulate(rows, headers=self.cursor.column_names)
        matched_users = []

        for i, x in enumerate(rows):
            pos1 = (rows[i][1], rows[i][2])
            current_time = rows[i][3]
            goal_time = current_time + datetime.timedelta(seconds=60)
            j = i
            if x == rows[len(rows)-60]:
                break
            while current_time < goal_time:
                j += 1
                pos2 = (rows[j][1], rows[j][2])
                if haversine(pos1, pos2, unit=Unit.METERS) <= 100 and rows[i][0] != rows[j][0]:
                    if (rows[i][0], rows[j][0]) not in matched_users:
                        if (rows[j][0], rows[i][0]) not in matched_users:
                            matched_users.append((rows[i][0], rows[j][0]))

                i+=1
                current_time = rows[i][3]
        print(matched_users)
        return len(matched_users) * 2



def main():
    program = None
    program = Part2()
    print(program.task6())
    # program = None
    # try:
    #     program = Task2()
    #     program.proximity_check()
    # except Exception as e:
    #     print("Error: Failed to use database:", e)
    # finally:
    #     if program:
    #         program.connection.close_connection()
main()
