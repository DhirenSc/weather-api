import requests
from utility import *
from sql.database import DBOperations
from geolocation.iplocation import IPLocation
import json
from flask_caching import Cache


class Report:
    
    def __init__(self, request_ip):
        """ 
        Constructor for the Report class. Initializes the attributes specified for the class.
  
        Parameters: 
            ip_address: IP address the client is using to access the api.
            
        """
        self.request_ip = '110.33.122.75'
    
    def process_response(self, data, location_id):
        response = {}
        json_data = json.loads(data)
        
        response['city'] = json_data['today']['city']
        response['state'] = json_data['today']['state']
        response['country'] = json_data['today']['country']
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
        return response

    def insert_or_update_db(self, response, location_id):
        self.db = DBOperations()
        insert_or_update_db_flag = self.db.insert_or_update_db(response, location_id)
        return insert_or_update_db_flag

    def check_location(self, city, state, country):
        self.db = DBOperations()
        location_id = self.db.check_location(city, state, country)
        return location_id
    
    def get_weather_data(self, location_id):
        self.db = DBOperations()
        location_data = self.db.get_location_data(location_id)
        return location_data

    def create_response_from_db(self, db_data):
        response = {}
        area_flag = True
        for row in db_data:
            if(area_flag == True):
                response['city'] = row['city']
                response['state'] = row['state']
                response['country'] = row['country']
                area_flag = False
            response['day'+str(row['day'])] = {}
            response['day'+str(row['day'])]['description'] = row['description']
            response['day'+str(row['day'])]['high_temp'] = float(round(row['high_temp'], 2))
            response['day'+str(row['day'])]['low_temp'] = float(round(row['low_temp'], 2))
            response['day'+str(row['day'])]['humidity'] = int(row['humidity'])
        print(response)
        return response
    
    def log_insert(self, request_ip, city, state, country):
        self.db = DBOperations()
        return self.db.insert_into_logs(request_ip, city, state, country)
    
    def process(self):

        # Call Ipstack to get ip address geolocation
        geolocation = IPLocation(self.request_ip)
        city, state, country = geolocation.get_location()
        # Check if such location data exists in cache (based on timestamp)
        # cached_response = Cache.get(city + "|" + state + "|" + country)
        # if cached_response:
        #     print(cached_response)
        
        # Check if location exists in DB (based on timestamp)
        check_location_flag, location_id = self.check_location(city, state, country)
        if(check_location_flag):
            print('found')
            # Location exists
            location_data = self.get_weather_data(location_id)
            weather_report = self.create_response_from_db(location_data)
            # log_insert_check = self.log_insert(self.request_ip, city, state, country)
            # if(log_insert_check):
            return weather_report
        else:
            response = requests.get(url = API_ENDPOINT, headers = {"x-forwarded-for": self.request_ip})
            print(response.text)
            weather_report = self.process_response(response.text, location_id)
            return weather_report