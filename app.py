from flask import Flask, jsonify
from flask import request
from utility import *
from report import Report
import json
from flask_caching import Cache
import time

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)

cache.init_app(app)

@app.route("/")
@cache.cached(timeout=300)  # cache this view for 5 minutes
def cached_view():
    return time.ctime()

@app.route(REPORT_ENDPOINT, methods=[METHOD_GET])
def report():
    report = Report(request.remote_addr)
    # print(request.remote_addr)
    weather_report = report.process()

    response = json.dumps(weather_report)
    return app.response_class(response = response, mimetype=MIME_JSON)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)