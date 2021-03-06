"""
    Contains constants being used at the database level
"""

HOST = 'sql9.freemysqlhosting.net'
DATABASE = 'sql9385632'
USERNAME = 'sql9385632'
PASSWORD = 'ClNZxGuQ19'

NUMBER_OF_SECONDS = 86400 # seconds in 24 hours
INSERT_LOCATION_QUERY = "INSERT INTO locations (location_id, city, state) VALUES (%s, %s, %s)"
INSERT_DAILY_QUERY = "INSERT INTO daily_data (location_id, day, description, high_temp, low_temp, humidity) VALUES (%s, %s, %s, %s, %s, %s)"
UPDATE_LOCATION_QUERY = "UPDATE locations SET timestamp = %s WHERE location_id = %s"
UPDATE_DAILY_QUERY = "UPDATE daily_data SET description = %s, high_temp = %s, low_temp = %s, humidity = %s WHERE location_id = %s AND day = %s"
INSERT_LOG_QUERY = "INSERT INTO logs (ip, city, state) values (%s, %s, %s)"
CHECK_LOCATION_QUERY = "SELECT location_id, timestamp FROM locations WHERE city = %s AND state = %s"
GET_DAILY_DATA = "SELECT * FROM daily_data JOIN locations using(location_id) WHERE location_id = %s"