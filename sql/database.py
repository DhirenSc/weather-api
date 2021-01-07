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
        For inserting data to the requests table or updating it based on expiry
          
        Returns: 
            Success: If insert or update was successful.
        """
        try:
            conn = self.connect()
            conn.autocommit = False
            rowcount = 0
            with conn.cursor(prepared=True) as cursor:
                location_row = (location_id, response_data['city'], response_data['state'])
                if(location_id is None):
                    location_id = uuid.uuid4().hex[:6].upper()
                    location_row = (location_id, response_data['city'], response_data['state'])
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
            self.disconnect()
            return True
        except Exception as e:
            conn.rollback()
            self.disconnect()
            return False
    
    """ 
        For checking the database for a particular location
          
        Returns: 
            check_location_flag: boolean value to denote if location exists and is not expired, 
            location_id: string value denoting location id 
            exception_flag: boolean value denoting if exception has occured
    """
    def check_location(self, city, state):
        check_location_flag, location_id, exception_flag = None, None, None
        try:
            conn = self.connect()
            check_location_flag, location_id, exception_flag = None, None, None
            with conn.cursor(prepared=True) as cursor:
                location_row = (city, state)
                cursor.execute(CHECK_LOCATION_QUERY, location_row)
                row = cursor.fetchone()
                if(row):
                    now = datetime.now()
                    if (now - row[1]).total_seconds() > NUMBER_OF_SECONDS:
                        # exceeded 24 hours
                        check_location_flag = False
                        location_id = row[0]
                        exception_flag = False
                    else:
                        # not exceeded 24 hours
                        check_location_flag = True
                        location_id = row[0]
                        exception_flag = False
                else:
                    # no location present
                    check_location_flag = False
                    location_id = None
                    exception_flag = False
            self.disconnect()
            return check_location_flag, location_id, exception_flag
        except:
            self.disconnect()
            return False, None, True
    
    """ 
        To fetch daily weather data for a particular location
          
        Returns: 
            daily_data: results from database, 
            exception_flag: boolean value denoting if exception has occured
    """
    def get_location_data(self, location_id):
        try:
            conn = self.connect()
            with conn.cursor(prepared=True) as cursor:
                cursor.execute(GET_DAILY_DATA, [(location_id)])
                daily_data = []
                for row in CursorByName(cursor):
                    daily_data.append(row)
                return daily_data, False
        except:
            self.disconnect()
            return None, True
    
    """ 
        For inserting every request into logs
          
        Returns: 
            check_insert_flag: boolean value denoting if log was inserted
    """
    def insert_into_logs(self, request_ip, city, state):
        try:
            conn = self.connect()
            rowcount = 0
            with conn.cursor(prepared=True) as cursor:
                location_row = (request_ip, city, state)
                cursor.execute(INSERT_LOG_QUERY, location_row)
                conn.commit()
                return cursor.rowcount == 1, False
        except:
            self.disconnect()
            return 0, True

