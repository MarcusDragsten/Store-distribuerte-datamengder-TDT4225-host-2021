from haversine import haversine, Unit
import datetime
from DbConnector import DbConnector
from tabulate import tabulate


class QueryProgram:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    def execute_query(self, queries):
        for query in queries:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            print(tabulate(rows, headers=self.cursor.column_names))
        return

    # How many users, activities and trackpoints are there in the dataset (after it is inserted into the database).
    def query1(self):
        queries = ["""
            SELECT COUNT(*) as NumberOfActivities FROM Activity""",
                   """
            SELECT COUNT(*) as NumberOfUsers FROM User""",
                   """
            SELECT COUNT(*) as NumberOfTrackPoints FROM TrackPoint"""]
        print('\n\n Solution to query 1:\n')
        self.execute_query(queries)

    # Find the average, minimum and maximum number of activities per user.
    def query2(self):
        # 1. Query: Calculating average number of activities per user, rounding to the nearest 0.1 decimal.
        # 2. Query: Calculating the minimum number of activities for a user, to avoid loosing the rows of the
        # users with zero activities when using COUNT, we're using a LEFT JOIN
        # 3. Query: Calculating the maximum number of activities for a user
        queries = ["""
            SELECT ROUND(numberOfActivities.noa/numberOfUsers.nou,1) AS AverageNumberOfActivities 
            FROM (
                SELECT COUNT(*) AS nou FROM User) AS numberOfUsers, (
                    SELECT COUNT(*) AS noa FROM Activity) AS numberOfActivities""",
                   """
            SELECT COUNT(Activity.user_id) AS MinNumberOfActivities FROM User
                LEFT JOIN Activity ON User.id = Activity.user_id
            GROUP BY User.id 
            ORDER BY MinNumberOfActivities ASC 
            LIMIT 1""",
                   """
            SELECT COUNT(*) AS MaxNumberOfActivities 
            FROM Activity 
            GROUP BY user_id 
            ORDER BY MaxNumberOfActivities DESC 
            LIMIT 1"""]
        print('\n\n Solution to query 2:\n')
        self.execute_query(queries)

    # Find the top 10 users with the highest number of activities.
    def query3(self):
        queries = ["""
            SELECT user_id AS TopTenUsers, COUNT(*) AS NumberofActivities 
            FROM Activity 
            GROUP BY user_id 
            ORDER BY NumberofActivities DESC 
            LIMIT 10"""]
        print('\n\n Solution to query 3:\n')
        self.execute_query(queries)

    # Find the number of users that have started the activity in one day and ended the activity the next day.
    def query4(self):
        queries = ["""
            SELECT DISTINCT user_id AS OverNightUsers 
            FROM Activity 
            WHERE DATEDIFF(end_date_time, start_date_time) = 1"""]
        print('\n\n Solution to query 4:\n')
        self.execute_query(queries)

    # Find activities that are registered multiple times. You should find the query even if you get zero results
    def query5(self):
        queries = ["""
            SELECT user_id AS Users, transportation_mode AS Transportation, 
                start_date_time AS 'Start date', end_date_time AS 'End date', COUNT(*) AS 'Number of lines that are equal' 
            FROM Activity 
            GROUP BY user_id, transportation_mode, start_date_time, end_date_time 
            HAVING COUNT(*)>1;"""]
        print('\n\n Solution to query 5:\n')
        self.execute_query(queries)

    # Find the number of users which have been close to each other in time and space (Covid-19 tracking).
    # Close is defined as the same minute (60 seconds) and space (100 meters).
    def query6(self):
        # To save time this only checks some users, to check the whole DB; remove the WHERE clause.
        # This query finds all the trackpoints from the DB and sorts by the date_time in ascending order.
        # From there python uses the result to check if they are withing 100 meters from each other,
        # and withing 60 seconds.
        query = """
            SELECT User.id, TrackPoint.lat, TrackPoint.lon, TrackPoint.date_time
            FROM (( User
                INNER JOIN Activity ON User.id = Activity.user_id)
                INNER JOIN TrackPoint ON Activity.id = TrackPoint.activity_id)
            WHERE User.id = '003' or User.id = '004' or User.id = '006' or User.id = '007'
            ORDER BY TrackPoint.date_time ASC;"""
        print('\n\n Solution to query 6:\n')
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        tabulate(rows, headers=self.cursor.column_names)
        matched_users = []

        for i, x in enumerate(rows):
            pos1 = (rows[i][1], rows[i][2])
            current_time = rows[i][3]
            goal_time = current_time + datetime.timedelta(seconds=60)
            j = i
            if x == rows[len(rows) - 60]:
                break
            while current_time < goal_time:
                j += 1
                pos2 = (rows[j][1], rows[j][2])
                if haversine(pos1, pos2, unit=Unit.METERS) <= 100 and rows[i][0] != rows[j][0]:
                    if (rows[i][0], rows[j][0]) not in matched_users:
                        if (rows[j][0], rows[i][0]) not in matched_users:
                            matched_users.append((rows[i][0], rows[j][0]))

                i += 1
                current_time = rows[i][3]
        print(matched_users, "total users:", len(matched_users) * 2)
        return len(matched_users) * 2

    # Find all users that have never taken a taxi.
    def query7(self):
        # Finding the non-taxi-users by finding the ones missing in the table with taxi users
        queries = [
            """
            SELECT id as NotTaxiUsers FROM User 
            WHERE id NOT IN (
                SELECT DISTINCT user_id 
                FROM Activity 
                WHERE (transportation_mode = 'taxi'))"""]
        print('\n\n Solution to query 7:\n')
        self.execute_query(queries)

    # Find all types of transportation modes and count how many distinct users that
    # have used the different transportation modes. Do not count the rows where the transportation mode is null.
    # Ordering descending on more popular to less popular, because it seems more interesting than alphabetically
    def query8(self):
        queries = ["""
            SELECT transportation_mode as TransporationMode, COUNT(DISTINCT user_id) AS NumberOfDistinctUsers 
            FROM Activity 
            WHERE transportation_mode != 'NULL'
            GROUP BY  transportation_mode 
            ORDER BY NumberOfDistinctUsers DESC"""]
        print('\n\n Solution to query 8:\n')
        self.execute_query(queries)

    # a) Find the year and month with the most activities. b) Which user had the most activities this year and month,
    # and how many recorded hours do they have? Do they have more hours recorded than the user with the second most
    # activities?
    def query9(self):
        # Assuming year-month related to each other, and not independently most popular year and most popular month
        # Also assuming we can use an activity's start time to calculate which year and month it was in
        query_a = """
            SELECT YEAR(start_date_time) AS Year, MONTH(start_date_time) AS Month, COUNT(*) AS NumberOfActivities 
            FROM Activity 
            GROUP BY Year, Month 
            ORDER BY NumberOfActivities DESC 
            LIMIT 1"""
        print('\n\n Solution to query 9a:\n')
        self.cursor.execute(query_a)
        result_query_a = self.cursor.fetchall()
        print(tabulate(result_query_a, headers=self.cursor.column_names))

        # Saving the results from 9a to use in the next query (9b part 1)
        top_year = result_query_a[0][0]
        top_month = result_query_a[0][1]

        # Using top year and month from task a to get the two most active users during this month
        # so that we can compare nr. 1 and nr. 2 in the next query (9b part 2)
        query_b1 = """
            SELECT user_id, COUNT(*) AS TopNumberOfActivities 
            FROM Activity 
            WHERE MONTH(start_date_time) = %(m)s  AND YEAR(start_date_time) = %(y)s 
            GROUP BY user_id
            ORDER BY TopNumberOfActivities DESC 
            LIMIT 2"""
        print('\n\n Solution to query 9b part 1:\n')
        self.cursor.execute(query_b1,
                            {'m': top_month, 'y': top_year})
        result_query_b1 = self.cursor.fetchall()
        print(tabulate(result_query_b1, headers=self.cursor.column_names))

        # Saving the results fra query 9b part 1 in variables
        most_activities = result_query_b1[0][0]
        second_most_activities = result_query_b1[1][0]

        query_b2 = """
            SELECT user_id, ROUND(SUM(TIMESTAMPDIFF(SECOND,start_date_time,end_date_time)/3600),2) AS Hours 
            FROM Activity 
            WHERE MONTH(start_date_time) = %(m)s AND YEAR(start_date_time) = %(y)s AND (user_id = %(ma)s OR user_id = %(sma)s)
            GROUP BY user_id 
            ORDER BY Hours DESC"""
        print('\n\n Solution to query 9b part 2:\n')
        self.cursor.execute(query_b2,
                            {'m': top_month, 'y': top_year, 'ma': most_activities, 'sma': second_most_activities})
        result_query_b2 = self.cursor.fetchall()
        print(tabulate(result_query_b2, headers=self.cursor.column_names))

    # Find the total distance (in km) walked in 2008, by user with id=112.
    def query10(self):
        query = """
            SELECT tp.activity_id, tp.lat, tp.lon 
            FROM TrackPoint AS tp 
                INNER JOIN Activity AS act ON act.id=tp.activity_id 
                WHERE act.user_id = 112 AND YEAR(tp.date_time) = 2008 AND act.transportation_mode = 'walk'"""
        print('\n\n Solution to query 10:\n')
        self.cursor.execute(query)
        queryData = self.cursor.fetchall()
        totalDistance = 0
        for tp in range(0, len(queryData) - 1):
            id = queryData[tp][0]
            lat = queryData[tp][1]
            lon = queryData[tp][2]
            if id == queryData[tp + 1][0]:
                totalDistance += haversine((lat, lon), (queryData[tp + 1][1], queryData[tp + 1][2]))
        print(round(totalDistance), 'km')

    # Find the top 20 users who have gained the most altitude meters.
    def query11(self):
        # Using LAG function to look at rows in the table that are directly after each other
        # Checking for invalid values with excluding lag_table.prev_altitude with value -777
        queries = ["""
            SELECT lag_table.user_id, ROUND(SUM(lag_table.altitude - lag_table.prev_altitude) * 0.3048, 0) AS AltitudeGained 
            FROM (
                SELECT tp.activity_id, tp.altitude, act.user_id, LAG(tp.altitude,1) OVER (PARTITION BY tp.activity_id) AS prev_altitude 
                FROM TrackPoint AS tp 
                    JOIN Activity AS act ON act.id = tp.activity_id
            ) AS lag_table 
            WHERE lag_table.altitude > lag_table.prev_altitude AND lag_table.prev_altitude != -777 
            GROUP BY lag_table.user_id 
            ORDER BY AltitudeGained DESC 
            LIMIT 20"""]
        print('\n\n Solution to query 11:\n')
        self.execute_query(queries)

    # Find all users who have invalid activities, and the number of invalid activities per user.
    # Also using LAG
    # 300 sec equals 5 minutes
    def query12(self):
        queries = ["""
            SELECT lag_table.user_id, COUNT(DISTINCT lag_table.activity_id) AS invalid_activities
            FROM(
                SELECT activity_id, user_id, date_time, LAG(date_time, 1) OVER (PARTITION BY tp.activity_id) AS prev_time 
            FROM TrackPoint AS tp 
                JOIN Activity AS act ON act.id = tp.activity_id) AS lag_table
            WHERE TIME_TO_SEC(TIMEDIFF(lag_table.date_time, lag_table.prev_time)) > 300
            GROUP BY lag_table.user_id"""]
        print('\n\n Solution to query 12:\n')
        self.execute_query(queries)


def main():
    program = None
    try:
        program = QueryProgram()
        # program.query1()
        # program.query2()
        # program.query3()
        # program.query4()
        # program.query5()
        # program.query6()
        # program.query7()
        # program.query8()
        # program.query9()
        # program.query10()
        program.query11()
        # program.query12()

    except Exception as e:
        print("ERROR: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()


if __name__ == '__main__':
    main()
