"""
    Contains constants being used at the database level
"""

HOST = 'HOSTNAME'
DATABASE = 'DATABASE'
USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'

INSERT_REQUEST_QUERY = "INSERT INTO requests (ip, city, state, country) values (%s, %s, %s, %s)"