from .connect import DBConnection
from .utility import *

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
    
    def insert_into_requests(self, response_data, request_ip):
        """ 
        For inserting data to the requests table
          
        Returns: 
            row count: Number of rows inserted.
        """
        conn = self.connect()
        with conn.cursor(prepared=True) as cursor:
            request_row = (request_ip, response_data['city'], response_data['state'], response_data['country'])
            cursor.execute(INSERT_REQUEST_QUERY, request_row)
            conn.commit()
            return cursor.rowcount