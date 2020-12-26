import requests
from utility import *
from sql.database import DBOperations
import json

class Report:
    
    def __init__(self, request_ip):
        """ 
        Constructor for the Report class. Initializes the attributes specified for the class.
  
        Parameters: 
            ip_address: IP address the client is using to access the api.
            
        """
        self.request_ip = request_ip
    
    def process_response(self, data):
        response = {}
        json_data = json.loads(data)
        
        response['description'] = json_data['today']['description']
        response['city'] = json_data['today']['city']
        response['state'] = json_data['today']['state']
        response['country'] = json_data['today']['country']
        response['day0'] = {}
        response['day0']['high_temp'] = float(json_data['today']['highTemperature'])
        response['day0']['low_temp'] = float(json_data['today']['lowTemperature'])
        response['day0']['humidity'] = int(json_data['today']['humidity'])
        counter = 1
        while(counter <= 3):
            response['day'+str(counter)] = {}
            response['day'+str(counter)]['high_temp'] = float(json_data['daily'][counter]['highTemperature'])
            response['day'+str(counter)]['low_temp'] = float(json_data['daily'][counter]['lowTemperature'])
            response['day'+str(counter)]['humidity'] = int(json_data['daily'][counter]['humidity'])
            counter = counter + 1
        
        success = self.insert_into_db(response, self.request_ip)
        return response

    def insert_into_db(self, response, request_ip):
        self.db = DBOperations()
        return self.db.insert_into_requests(response, request_ip)

    
    def get_weather_report(self):

        # sending post request and saving response as response object 
        r = requests.get(url = API_ENDPOINT, headers = {"x-forwarded-for": '49.248.19.26'})
        processed_response = self.process_response(r.text)
        # extracting response text
        return processed_response