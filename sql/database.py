from .connect import DBConnection
from .utility import *
from .cursor_by_name import CursorByName
from datetime import datetime, timedelta
import uuid
import time

class DBOperations:
    def connect(self):
        """ 
        For connecting to the database.
          
        Returns: 
            connection: Connection reference to the database
        """

        self.db_conn = DBConnection()
        return self.db_conn.connect()

    def disconnect(self):
        """ 
        For disconnecting from the database.
        """

        self.db_conn.disconnect()

    def insert_or_update_db(self, response_data, location_id):
        """ 
        For inserting data to the requests table
          
        Returns: 
            row count: Number of rows inserted.
        """
        # try:
        conn = self.connect()
        conn.autocommit = False
        rowcount = 0
        with conn.cursor(prepared=True) as cursor:
            location_row = (location_id, response_data['city'], response_data['state'], response_data['country'])
            if(location_id is None):
                print("new id")
                location_id = uuid.uuid4().hex[:6].upper()
                location_row = (location_id, response_data['city'], response_data['state'], response_data['country'])
                cursor.execute(INSERT_LOCATION_QUERY, location_row)
                counter = 0
                while(counter <= 3):
                    description = response_data['day'+str(counter)]['description']
                    high_temp = response_data['day'+str(counter)]['high_temp']
                    low_temp = response_data['day'+str(counter)]['low_temp']
                    humidity = response_data['day'+str(counter)]['humidity']
                    daily_row = (location_id, counter, description, high_temp, low_temp, humidity)
                    cursor.execute(INSERT_DAILY_QUERY, daily_row)
                    counter = counter + 1
            else:
                print("update_id")
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                location_row = (timestamp, location_id)
                cursor.execute(UPDATE_LOCATION_QUERY, location_row)
                counter = 0
                while(counter <= 3):
                    description = response_data['day'+str(counter)]['description']
                    high_temp = response_data['day'+str(counter)]['high_temp']
                    low_temp = response_data['day'+str(counter)]['low_temp']
                    humidity = response_data['day'+str(counter)]['humidity']
                    daily_row = (description, high_temp, low_temp, humidity, location_id, counter)
                    cursor.execute(UPDATE_DAILY_QUERY, daily_row)
                    counter = counter + 1
            conn.commit()
            return True
        # except Exception as e:
        #     print(e)
        #     conn.rollback()
        #     return False
    
    def check_location(self, city, state, country):
        conn = self.connect()
        with conn.cursor(prepared=True) as cursor:
            location_row = (city, state, country)
            cursor.execute(CHECK_LOCATION_QUERY, location_row)
            row = cursor.fetchone()
            if(row):
                now = datetime.now()
                print(now)
                print(row[1])
                if (now - row[1]).total_seconds() > NUMBER_OF_SECONDS:
                    # exceeded 24 hours
                    print("here 1")
                    return False, row[0]
                else:
                    # not exceeded 24 hours
                    print("here 2")
                    return True, row[0]
            else:
                # no location present
                print("here 3")
                return False, None
    
    def get_location_data(self, location_id):
        conn = self.connect()
        with conn.cursor(prepared=True) as cursor:
            data_row = (str(location_id))
            cursor.execute(GET_DAILY_DATA, [(location_id)])
            daily_data = []
            for row in CursorByName(cursor):
                daily_data.append(row)
            # print(rows)
            return daily_data
    
    def insert_into_logs(self, request_ip, city, state, country):
        conn = self.connect()
        rowcount = 0
        with conn.cursor(prepared=True) as cursor:
            location_row = (request_ip, city, state, country)
            print(location_row)
            cursor.execute(INSERT_LOG_QUERY, location_row)
            conn.commit()
            return cursor.rowcount == 1

