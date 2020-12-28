###############################################
## Weather Cast API
###############################################
## Author: Dhiren Chandnani
## Version: 1.0
## Maintainer: Dhiren Chandnani
## Email: dhirensc65@gmail.com
###############################################


from flask import Flask, jsonify
from flask import request
from utility import *
from report import Report
import json
from flask_caching import Cache
import time
from geolocation.iplocation import IPLocation
from flask import render_template
from swagger.specific import setup_swagger_specific

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)

cache.init_app(app)

# swagger documentation
setup_swagger_specific(app)

@app.route("/")
def welcome():
    """
    Renders the landing page for the api.
    """
    # return "Hello there"
    return render_template('index.html')


@app.route(REPORT_ENDPOINT, methods=[METHOD_GET])
def report():
    """ 
        Is the report route.
        Its used to get daily weather report based on user location

        Returns: 
            response (json): Containing the location details and 3 day weather report.
    """
    request_ip = request.remote_addr
    
    # Call Ipstack to get ip address geolocation
    geolocation = IPLocation(request_ip)
    city, state = geolocation.get_location()

    if(city is None):
        response = json.dumps({"error": "Unable to get location from IP"})
        return app.response_class(response = response, mimetype=MIME_JSON)
    else:
        cached_response = cache.get(str(city) + "|" + str(state))
        if(cached_response):
            return app.response_class(response = json.dumps(cached_response), mimetype=MIME_JSON)
        else:
            report = Report(request_ip, city, state)
            # print(request.remote_addr)
            weather_report = report.process()
            if(not ("error" in weather_report)):
                cache_key = str(weather_report['city']) + "|" + str(weather_report['state'])
                cache.set(cache_key, weather_report, timeout=86400)
                
            response = json.dumps(weather_report)
            return app.response_class(response = response, mimetype=MIME_JSON)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 80)