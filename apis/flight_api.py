import os
import pandas as pd
import requests
from utils.parseInput import flight_api
import aiohttp
import asyncio
import isodate 

class travelapi:
    
    def __init__(self):
        self.airport_token = 'E2qEG57wPvnCkvzKEsxlSoeuZ26q'
        self.airport_headers = {'Authorization': 'Bearer ' + self.airport_token}
        
        self.flight_token = 'vo6LTIXydSWXaAUGwbtUGl02vMWb'
        self.flight_headers = {'Authorization': 'Bearer ' + self.flight_token}
        
        self.flight_api = flight_api(self.flight_token)
    
    
    def first(self, input_: dict):
        
        
        origin = input_["originLocation"]
        destination = input_["destinationLocation"]
        

        origin_airports = self.cityToAirports(origin).head(3)
        # print(destination)
        destination_airports = self.cityToAirports(destination).head(3)
        # print(origin_airports)
        # print(destination_airports)
        # exit()
        combinations = [(origin, destination) for origin in origin_airports['iataCode'] for destination in destination_airports['iataCode']]
        
        urls = []
        for origin, destination in combinations:
            fixed_query = input_.copy()
            del fixed_query["destinationLocation"]
            del fixed_query["originLocation"]
            fixed_query["originLocationCode"] = origin
            fixed_query["destinationLocationCode"] = destination
            if fixed_query['returnDate'] == None:
                del fixed_query['returnDate']
                
            for key, value in fixed_query.items():
                fixed_query[key] = str(value)
                
            fixed_query['nonStop'] = fixed_query['nonStop'].lower()
                   
            url = self.createUrl(fixed_query)
            # url = self.flight_api.process(fixed_query)
            urls.append(url)
            
        dfs = self.flight_api.process_url(urls)
        return self.process_output(dfs)
       
    
    def process_output(self, dfs):
        if len(dfs) == 0:
            return dfs
        dfs.sort_values(by='totalPrice', ascending=True, inplace=True)
        print(dfs.head(5))
        return dfs.head(5)
    
    def createUrl(self, queries: dict) -> str:
    #Get all possible query fields and store
        print(queries)
        
        
                
        base = "https://test.api.amadeus.com/v2/shopping/flight-offers?"
        return base + ''.join((key  + '=' + value +'&') for key, value in queries.items())
        
    def cityToAirports(self, city: str):
        url = f'https://test.api.amadeus.com/v1/reference-data/locations?subType=AIRPORT&keyword={city}&page%5Blimit%5D=10&page%5Boffset%5D=0&sort=analytics.travelers.score&view=FULL'
        
        
        resp = requests.get(url, headers=self.airport_headers)
        out = resp.json()
        
        # Create an empty dataframe
        df = pd.DataFrame(columns=['iataCode', 'cityName', 'name'])

        # Iterate over the data and append it to the dataframe
        for i in out['data']:
            df = pd.concat([df, pd.DataFrame({'iataCode': [i['iataCode']], 'cityName': [i['address']['cityName']], 'name': [i['name']]})], ignore_index=True)

        # Print the dataframe
        return df
        
        
if __name__ == "__main__":
    ap = travelapi()
    input_ = { "destinationLocation": "New York", 
    "originLocation": "Dallas", 
    "departureDate": "2024-02-14", 
    "returnDate": "2024-02-15",
    "adults": "2",
    "children": "0",
    "infants": "0",
    "travelClass": "ECONOMY",
    "nonStop": "true",
    "currencyCode": "EUR",
    "maxPrice": "5000",
    "max": "10" }

    ap.first(input_)