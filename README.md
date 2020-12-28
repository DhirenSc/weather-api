# Weather Report API [Case Study]

- This repository contains work done for developing Weather Cast REST API.
- This API returns specific weather data based on a users current location.
- Response contains 3 key fields - City, State and Day.
- Day is divided into 4 parts - 0, 1, 2 and 3.
- 0 represents the current day. 1, 2 and 3 represent consecutive days.
- For each day, weather description, high-temperature, low-temperature and humidity is displayed.

## Instructions to run locally:

1. Clone the repository to a folder in your system.
2. Make sure you have python 3 and ```pip``` installed in your machine.
3. Enter the cloned repository and run these commands:

```python
1. pip3 install -r requirements.txt
2. python3 app.py
```
4. The app will start on this URL : http://0.0.0.0:80/
5. Go to your browser and run http://localhost/api/report to get the weather report for your location.

## Live version:

Focus being on the REST API, I have hosted the api on a remote server.

LINK : http://weathercast.ga

TEST REPORT : http://weathercast.ga/api/report

DOCUMENTATION : http://weathercast.ga/swagger

This is just for testing purposes.

## MySQL Database:

- MySQL datbase is hosted via freemysqlhosting.net. I have added a file named ```create_database.sql``` in the ```sql``` folder which contains the DDL scripts.
- Database connection details are placed in ```database/utility.py``` in case you want to run the database locally or want to host database someplace else.

## IPQualityScore API:

- The geolocation API I have used is IPQualityScore (https://www.ipqualityscore.com/documentation/proxy-detection/overview). This API returns the geo-location details for a particular IP Address.
- API key can be found in ```iplocation/utility.py```

## Built with:
```
- Flask
- MySQL
```

## AWS Deployment

![alt text](https://github.com/DhirenSc/weather-api/blob/main/static/AWS%20Architecture.png?raw=True)
