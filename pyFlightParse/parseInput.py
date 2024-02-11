import pandas as pd
#just define a function to take a city code and get all the stuff

def cityToAirports(city: str):
    code_data = pd.read_excel('airport-codes.xls')
    code_data = code_data[code_data.index % 2 != 0]
    #filter to specific city
    code_filtered = code_data[code_data['City name'] == city]
    return list(code_filtered['Airport Code'].values)

def airportToCity(airport: str):
    code_data = pd.read_excel('airport-codes.xls')
    code_data = code_data[code_data.index % 2 != 0]
    #filter to specific city
    code_filtered = code_data[code_data['Airport Code'] == airport]
    return [list(code_filtered['Airport Name'].values),list(code_filtered['City name'].values)]