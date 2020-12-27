from .utility import *
from ipstack import GeoLookup
import json

class IPLocation:
    def __init__(self, request_ip):
        """ 
        For setting ip address for iplocation object

        """
        self.request_ip = request_ip

    def get_location(self):
        geo_lookup = GeoLookup(API_KEY)
        # Lookup a location for an IP Address
        # and catch any exceptions that might
        # be thrown
        try:
            # Retrieve the location information for an IP Address

            location = geo_lookup.get_location(self.request_ip)
            print(location)
            # location = LOCATION_SAMPLE_2

            # If we are unable to retrieve the location information
            # for an IP address, null will be returned.
            if location is None:
                return None, None, None
            else:
                # Print the Location dictionary.
                return location['city'], location['region_name'], location['country_name']
        except Exception as e:
            print(e)
            return None, None, None