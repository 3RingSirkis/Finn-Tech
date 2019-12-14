# coding: utf-8

# # Retrieve weather data
#     
#   {
#     "id": 4095415,
#     "name": "Vestavia Hills",
#     "country": "US",
#     "coord": {
#       "lon": -86.787773,
#       "lat": 33.448719
#     }
#   },
#     
# # {"Vestavia Hills" : "4095415", "Dothan" : "4059102", "Denver" : "4463523"}
# 
# Find a list of Cities and their IDs here: https://openweathermap.org/current
# Example URL:https://samples.openweathermap.org/data/2.5/weather?id=2172797&appid=b6907d289e10d714a6e88b30761fae22

import requests, json, datetime, smtplib, ssl, getpass

locations = {"Dothan" : "4059102"}

senderEmail = "FinnTheBoykin@gmail.com"

# ******************************************************************************** #
def main():
    receiverEmail = input("To who do you want to send this email?:")
    password = getpass.getpass(prompt='Enter the password for ' + senderEmail + ': ')
    
    for location in locations:
        
        response = getWeatherData(locations[location])

        main = response["main"]

        maxTemp = K2F(main["temp_max"])

        requestDateTime = currentDateTime()

        writeResults(location, requestDateTime, maxTemp)
        
        sendEmail(senderEmail, receiverEmail, password, maxTemp, location)

    
# Function to convert Kelvin to Fahrenheit - I could have used a library but I wanted to do it myself
def K2F(kTemp):
    fTemp = kTemp * 9/5 - 459.67
    
    fTemp = round(fTemp, 2)
    
    return fTemp


# Function to retrive the user's API key from "APIKey.txt"
def getAPIKey():
    apiKeyFile = open("APIKey.txt", "r")
    
    apiKey = apiKeyFile.read()
    
    apiKeyFile.close()                    
    
    return apiKey


# Retrieve weather data
def getWeatherData(locationID):
    apiKey = getAPIKey()
    endPoint = "http://api.openweathermap.org/data/2.5/"    # Base URL for Open Weather Map API

    # Define the request type 
    requestType = "weather?id="                             # Returns current weather values (updates every 10 minutes)
    # requestType = "forecast?id="                          # Returns the multiday weather forecast

    # Construct the request URL
    requestURL = endPoint + requestType + locationID + "&appid=" + apiKey

    # Make a 'GET' request to the URL
    response = requests.get(requestURL)
    
    # Decode the request into JSON
    x = response.json()
    
    return x


# Get the date and time of the request
def currentDateTime():
    now = datetime.datetime.now()
    
    requestDate = now.strftime("%Y-%m-%d")              # Format the date as YYYY-MM-DD 
    
    requestTime = now.strftime("%H:%M:%S")              # Format the time as HH:MM:SS
    
    return(requestDate, requestTime)


# Write the results to a text file
def writeResults(locationName, requestDateTime, maxTemp):
    fileName = locationName + ".txt"    

    f = open(fileName,"a+")

    f.write(requestDateTime[0] + "|" + requestDateTime[1] + "|" + str(maxTemp) + "\n")
    
    f.close()

# Create a connection to Gmail, construct the message, and send the email
def sendEmail(senderEmail, receiverEmail, password, maxTemp, location):
    message = """Subject: Woof woof!
    
Thank you for signing up for Finn's Weather Service. It is currently """ + str(maxTemp) + ' degrees in ' + location + '.'

    # Create a secure SSL context
    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(senderEmail, password)

        server.sendmail(senderEmail, receiverEmail, message)

    print("woof!")
    
# ******************************************************************************** #
if __name__ == "__main__":
    main()
    
else:
    print("I don't really know what this part does")
