from flask import Flask, jsonify
from flask import request
from utility import *
from report import Report
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route(REPORT_ENDPOINT, methods=[METHOD_GET])
def report():
    report = Report(request.remote_addr)
    # print(request.remote_addr)
    weather_report = report.get_weather_report()
    response = json.dumps(weather_report)
    return app.response_class(response = response, mimetype=MIME_JSON)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)