import requests
from utility import *
from sql.database import DBOperations
from geolocation.iplocation import IPLocation
import json
from flask_caching import Cache


class Report:
    """ 
        This is the class where all weather report is created for a user request.
        
        Attributes: 
            request_ip: IP address the client is using to access the api.
            city: city dervied from the ip geolocation api
            state: state dervied from the ip geolocation api
    """
    
    def __init__(self, request_ip, city, state):
        """ 
        Constructor for the Report class. Initializes the attributes specified for the class.
  
        Parameters: 
            request_ip: IP address the client is using to access the api.
            city: city dervied from the ip geolocation api
            state: state dervied from the ip geolocation api
        """
        self.request_ip = request_ip
        self.city = city
        self.state = state
    
    """ 
        For processing third party api data and creating a response object
    """
    def create_response_from_api(self, data, location_id):
        response = {}
        json_data = json.loads(data)
        response['city'] = json_data['today']['city']
        response['state'] = json_data['today']['state']
        response['day0'] = {}
        response['day0']['description'] = json_data['today']['description']
        response['day0']['high_temp'] = float(json_data['today']['highTemperature'])
        response['day0']['low_temp'] = float(json_data['today']['lowTemperature'])
        response['day0']['humidity'] = int(json_data['today']['humidity'])
        counter = 1
        while(counter <= 3):
            response['day'+str(counter)] = {}
            response['day'+str(counter)]['description'] = json_data['daily'][counter]['description']
            response['day'+str(counter)]['high_temp'] = float(json_data['daily'][counter]['highTemperature'])
            response['day'+str(counter)]['low_temp'] = float(json_data['daily'][counter]['lowTemperature'])
            response['day'+str(counter)]['humidity'] = int(json_data['daily'][counter]['humidity'])
            counter = counter + 1
        success = self.insert_or_update_db(response, location_id)
        if(success):
            return response
        else:
            return None
    
    """ 
        For inserting new location into the database or updating the same depending on
        time period. If time of new call exceeds 24 hrs, data needs to be updated
    """
    def insert_or_update_db(self, response, location_id):
        self.db = DBOperations()
        insert_or_update_db_flag = self.db.insert_or_update_db(response, location_id)
        return insert_or_update_db_flag

    """ 
        For checking if a location exists in the database. Also checks if data for
        that location is expired
    """
    def check_location(self, city, state):
        self.db = DBOperations()
        check_location_flag, location_id, exception_flag = self.db.check_location(city, state)
        return check_location_flag, location_id, exception_flag

    """ 
        For weather data from database for a location
    """
    def get_weather_data_from_db(self, location_id):
        self.db = DBOperations()
        location_data, exception_flag = self.db.get_location_data(location_id)
        if(not exception_flag):
            return location_data
        else:
            return None

    """ 
        For creating a response object based on data from database
    """
    def create_response_from_db(self, db_data):
        response = {}
        area_flag = True
        for row in db_data:
            if(area_flag == True):
                response['city'] = row['city']
                response['state'] = row['state']
                area_flag = False
            response['day'+str(row['day'])] = {}
            response['day'+str(row['day'])]['description'] = row['description']
            response['day'+str(row['day'])]['high_temp'] = float(round(row['high_temp'], 2))
            response['day'+str(row['day'])]['low_temp'] = float(round(row['low_temp'], 2))
            response['day'+str(row['day'])]['humidity'] = int(row['humidity'])
        return response
    
    """ 
        For inserting into logs
    """
    def log_insert(self, request_ip, city, state):
        self.db = DBOperations()
        return self.db.insert_into_logs(request_ip, city, state)
    
    """ 
        For starting the report process. It goes from checking if location exists to 
        fetching data from 3rd party api.
    """
    def process(self):
        # Check if location exists in DB (based on timestamp)
        check_location_flag, location_id, exception_flag = self.check_location(self.city, self.state)
        weather_report = None
        if(not exception_flag):
            if(check_location_flag):
                # Location exists
                location_data = self.get_weather_data_from_db(location_id)
                if(location_data):
                    weather_report = self.create_response_from_db(location_data)
                else:
                    weather_report = {"error": "Unable to find this location"}
            else:
                # Location does not exist or needs to be updated
                response = requests.get(url = API_ENDPOINT, headers = {"x-forwarded-for": self.request_ip})
                if(response):
                    weather_report = self.create_response_from_api(response.text, location_id)
                    if(weather_report is None):
                        weather_report = {"error": "Unable to update or insert new data"}                        
                else:
                    weather_report = {"error": "Unable to fetch weather data from API"}
        else:
            weather_report = {"error": "DB Connection issue. Try again later"}
        
        log_insert_check, log_exception_flag = self.log_insert(self.request_ip, weather_report['city'], weather_report['state'])
        if(not log_exception_flag):
            if(not log_insert_check):
                weather_report = {"error": "Unable to log request"}
        else:
            weather_report = {"error": "DB connection issue. Unable to log request"}

        return weather_report