from parseData import *

def flightParse(input: dict):
    queries = createQueries(input)
    offers = sendQuery(queries)
    return makeFrame(offers)

input = { "destinationLocation": "Dallas", 
"originLocation": "Houston", 
"departureDate": "2023-02-16", 
"returnDate": "2023-03-01", 
"adults": "2",
 "children": "0",
  "infants": "0",
   "travelClass": "ECONOMY",
    "nonStop": "false",
     "currencyCode": "USD",
      "maxPrice": "None",
       "max": "None" }

df = flightParse(input)
print(df)