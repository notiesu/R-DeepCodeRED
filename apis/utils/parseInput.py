import requests
import json
import pandas as pd
import isodate 
from datetime import datetime
import os

class flight_api:
    def __init__(self, flight_token: str):
        self.flight_token = flight_token
        self.flight_headers = {'Authorization': 'Bearer ' + self.flight_token}
        self.airport_df = pd.read_excel('Data/airport-codes.xls')
        
        pass
    
    def parseTimes(self, isoTime):
        datetime_obj = datetime.fromisoformat(isoTime)
        return datetime_obj.strftime('%I:%S%p %m-%d-%Y')
    
    
    def airportToCity(self, airport: str):
        code_data = self.airport_df
        code_data = code_data[code_data.index % 2 != 0]
        #filter to specific city
        code_filtered = code_data[code_data['Airport Code'] == airport]
        return [list(code_filtered['Airport Name'].values),list(code_filtered['City name'].values)]
        
    def parseDuration(self, isoDuration):
        duration = isodate.parse_duration(isoDuration)
        hours = duration.days * 24 + duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        return f"{hours} hours, {minutes} minutes"
    
    def process_url(self, urls):
        dfs =[]
        bad = []
        for url in urls:
            # url = 'https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=HOU&destinationLocationCode=AUS&departureDate=2024-05-02&adults=1&nonStop=false&max=250'
            # exit()
            
            resp = requests.get(url, headers=self.flight_headers)
            print(resp.json())
            offers = resp.json()["data"]
            
            
            df = self.process(offers)
            dfs.append(df)
        
        if len(dfs) == 0:
            return pd.DataFrame()
        
        return pd.concat(dfs)
    
    
    def process(self, offers: list):
        
        
        data_list = []
        labels = ['totalPrice', 'currency', 'numSeats', 'duration', 'carrierCodes', 'departureTimes', 'arrivalTimes', 'timeSegments',
                'segmentDurations', 'departurePort', 'arrivalPort', 'segmentPorts']
        
        for offer in offers:
            #Simple stuff
            numSeats = offer['numberOfBookableSeats']
            currency = offer['price']['currency']
            totalPrice = offer['price']['grandTotal']
            duration = self.parseDuration(offer['itineraries'][0]['duration'])

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

                departureTimes.append(self.parseTimes(segment['departure']['at']))
                arrivalTimes.append(self.parseTimes(segment['arrival']['at']))
                timeSegments.append(f"{self.parseTimes(segment['departure']['at'])} to {self.parseTimes(segment['arrival']['at'])}")

                segmentDurations.append(self.parseDuration(segment['duration']))
                departurePorts.append(self.airportToCity(segment['departure']['iataCode'])[0])
                arrivalPorts.append(segment['arrival']['iataCode'])
                segmentPorts.append(f"{segment['departure']['iataCode']} to {segment['arrival']['iataCode']}")
            
            #Individual traveler pricings
            data = [totalPrice, currency, numSeats, duration, carrierCodes, departureTimes, arrivalTimes, timeSegments,
                    segmentDurations, departurePorts, arrivalPorts, segmentPorts]
            data_list.append(data)

        df = pd.DataFrame(data_list,columns=labels)
        
        return df