from .utility import *
import json
import requests

class IPLocation:
    """
    This class is used to fetch location details of user's
    ip address using IPQUalityScore API
    """
    def __init__(self, request_ip):
        """ 
        For setting ip address for iplocation object

        """
        self.request_ip = request_ip

    """
    Return city and state from result of ipqualityscore API
    """
    def get_location(self):
        # Lookup a location for an IP Address
        # and catch any exceptions that might
        # be thrown
        try:
            # Retrieve the location information for an IP Address
            response = requests.get(url = IP_LOOKUP_ENDPOINT + self.request_ip)
            ip_lookup_response = json.loads(response.text)

            # If we are unable to retrieve the location information
            # for an IP address, null will be returned.
            if ip_lookup_response['success'] is False:
                return None, None
            else:
                # Print the Location dictionary.
                return ip_lookup_response['city'], ip_lookup_response['region']
        except Exception as e:
            return None, None