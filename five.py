#Create spreadsheet with country, state and city counts

from cliff.api import Cliff
import pandas as pd
import ast

file_name = "../processedData/author_location.xlsx" # path to file + file name
sheet =  "Sheet1" # sheet name or sheet number or list of sheet numbers and names

df = pd.read_excel(io=file_name, sheet_name=sheet)
city_data = []
state_data = []
country_data = []

city_check = []
state_check = []
country_check = []
for index, row in df.iterrows():
  for city in ast.literal_eval(row['cities']):
    if city not in city_check:
      city_check.append(city)
      temp_city = {}
      temp_city['name'] = city[0]
      temp_city['lat'] = city[1]
      temp_city['lon'] = city[2]
      temp_city['count'] = 1
      city_data.append(temp_city)
    else :
      for item in city_data:
        if item['name'] == city[0]:
          item['count'] += 1

  for state in ast.literal_eval(row['states']):
    if state not in state_check:
      state_check.append(state)
      temp_state = {}
      temp_state['name'] = state[0]
      temp_state['lat'] = state[1]
      temp_state['lon'] = state[2]
      temp_state['count'] = 1
      state_data.append(temp_state)
    else :
      for item in state_data:
        if item['name'] == state[0]:
          item['count'] += 1

  for country in ast.literal_eval(row['countries']):
    if country not in country_check:
      country_check.append(country)
      temp_country = {}
      temp_country['name'] = country[0]
      temp_country['lat'] = country[1]
      temp_country['lon'] = country[2]
      temp_country['count'] = 1
      country_data.append(temp_country)
    else :
      for item in country_data:
        if item['name'] == country[0]:
          item['count'] += 1

city_excel_frame = pd.DataFrame(city_data)
city_excel_frame.to_excel("../processedData/cities.xlsx", index=False)  

state_excel_frame = pd.DataFrame(state_data)
state_excel_frame.to_excel("../processedData/states.xlsx", index=False)  

country_excel_frame = pd.DataFrame(country_data)
country_excel_frame.to_excel("../processedData/countries.xlsx", index=False)  
