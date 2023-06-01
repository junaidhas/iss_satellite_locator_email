
import requests
import datetime as dt
import smtplib
import time

EMAIL = "learnerpython97@gmail.com"
PASSWORD = "password"
#need to use app password from gmail instead of password


MY_lat= 43.896080
MY_lng =-78.865128
# got the location of latitude and longitude of oshawa from https://www.latlong.net/ 

def is_overheard():
    response = requests.get(url ="http://api.open-notify.org/iss-now.json")
    # API to find the International space station(ISS) satellite current latitude and longitude
    response.raise_for_status()
    #check for any error while fetching the API

    data = response.json()
    print(data)
    iss_longitude = float(data['iss_position']['longitude'])
    iss_latitude = float(data['iss_position']['latitude'])
    # convertng to a float type to compare them with my location's latitude and longitude

#     iss_position = (iss_longitude,iss_latitude)
#     print(iss_position)

    if MY_lat-5 <= iss_latitude <=MY_lat+5 and MY_lng-5<= iss_longitude < MY_lng+5:
        return True


def is_night():

    parameters ={
        "lat" : MY_lat,
        "lng" : MY_lng,
        "formatted":0,

    }


    response = requests.get("https://api.sunrise-sunset.org/json",params=parameters)
    # API to find sunrise and sunset time for my location
    response.raise_for_status()

    data = response.json()
    print(data)
    print(type(data))
    sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
    sunset = data["results"]["sunset"].split("T")[1].split(":")[0]

    print(sunrise)
    print(sunset)

    time_now = dt.datetime.now().hour
  
    # if time_now is after sunset and before sunrise means it's night time
    if sunset <= time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    # repeats the process after every 60 seconds
    if is_overheard() and is_night():
        # sending an email to remind iss is near my location
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(EMAIL,PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=f"subject: International Space station is overhead !!!\n\nHey Buddy, ISS is near your location now, grab the telescope"
            )

