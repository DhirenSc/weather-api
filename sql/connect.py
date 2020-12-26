import mysql.connector
from mysql.connector import Error
from .utility import *

class DBConnection:        
    def connect(self):
        """ 
        For connecting to the database.
          
        Returns: 
            connection: Connection reference to the database
        """
        self.conn = mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, password=PASSWORD)
        return self.conn

    def disconnect(self):
        """ 
        For disconnecting from the database.
          
        Returns: 
            boolean: Whether or not sucessfully disconnected from the database
        """

        if(self.conn.is_connected()):
            return self.conn.close()
        else:
            return False