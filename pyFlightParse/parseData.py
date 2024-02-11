import requests
import json
from parseInput import *
import pandas as pd
import isodate 
from datetime import datetime

token = 'BkGZkKAPuE9DBIVoBaG01xTzSL1W'
headers = {'Authorization': 'Bearer ' + token}

def createUrl(queries: dict) -> str:
    #Get all possible query fields and store
    base = "https://test.api.amadeus.com/v2/shopping/flight-offers?"
    return base + ''.join((key  + '=' + value +'&') for key, value in queries.items())

def createQueries(input: dict):
    #convert the input data to be used for querying
    queries=[]
    toCodes = cityToAirports(input["destinationLocation"])
    fromCodes = cityToAirports(input["originLocation"])
    new_query=input.copy()
    new_query["destinationLocationCode"] = toCodes[0]
    new_query["originLocationCode"] = fromCodes[0]
    del new_query["destinationLocation"]
    del new_query["originLocation"]

    url = createUrl(new_query)
    queries.append(url)
    return queries

def sendQuery(input: dict):
    queries = createQueries(input)
    resp = requests.get(queries[0], headers=headers)
    offers = resp.json()["data"]
    return offers

def parseDuration(isoDuration):
    duration = isodate.parse_duration(isoDuration)
    hours = duration.days * 24 + duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    return f"{hours} hours, {minutes} minutes"

def parseTimes(isoTime):
    datetime_obj = datetime.fromisoformat(isoTime)
    return datetime_obj.strftime('%I:%S%p %m-%d-%Y')

def makeFrame(offers):
    data_list = []
    labels = ['totalPrice', 'currency', 'numSeats', 'duration', 'carrierCodes', 'departureTimes', 'arrivalTimes', 'timeSegments',
            'segmentDurations', 'departurePort', 'arrivalPort', 'segmentPorts']
    
    for offer in offers:
        #Simple stuff
        numSeats = offer['numberOfBookableSeats']
        currency = offer['price']['currency']
        totalPrice = offer['price']['grandTotal']
        duration = parseDuration(offer['itineraries'][0]['duration'])

        #first flight itinerary for simplicity
        segments = offer['itineraries'][0]['segments']

        carrierCodes = []
        #*********
        departureTimes = []
        arrivalTimes = []
        timeSegments = []
        #*********

        segmentDurations = []
        departurePorts = []
        arrivalPorts = []
        segmentPorts = []


        for segment in segments:
            carrierCodes.append(segment['carrierCode'])

            departureTimes.append(parseTimes(segment['departure']['at']))
            arrivalTimes.append(parseTimes(segment['arrival']['at']))
            timeSegments.append(f"{parseTimes(segment['departure']['at'])} to {parseTimes(segment['arrival']['at'])}")

            segmentDurations.append(parseDuration(segment['duration']))
            departurePorts.append(airportToCity(segment['departure']['iataCode'])[0])
            arrivalPorts.append(segment['arrival']['iataCode'])
            segmentPorts.append(f"{segment['departure']['iataCode']} to {segment['arrival']['iataCode']}")
        
        #Individual traveler pricings
        data = [totalPrice, currency, numSeats, duration, carrierCodes, departureTimes, arrivalTimes, timeSegments,
                segmentDurations, departurePorts, arrivalPorts, segmentPorts]
        data_list.append(data)

    df = pd.DataFrame(data_list,columns=labels)
    return df

