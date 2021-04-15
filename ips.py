#Reads members csv file and then creates spreadsheet with country and city counts.
import pandas as pd
import geoip2.database

reader = geoip2.database.Reader("../GeoLite2-City_20210202/GeoLite2-City.mmdb")

file_name = "../processedData/core_members.xls" # path to file + file name
sheet =  "Sheet1" # sheet name or sheet number or list of sheet numbers and names

df = pd.read_excel(io=file_name, sheet_name=sheet)
city_data = []
country_data = []
check_city = []
check_country = []
for index, row in df.iterrows():
  response = reader.city(row['ip'])
  if response.city.name != None and str(response.city.name + response.country.name) not in check_city:
    check_city.append(str(response.city.name + response.country.name))
    temp_city = {}
    temp_city['name'] = response.city.name
    temp_city['country'] = response.country.name
    temp_city['lat'] = response.location.latitude
    temp_city['lon'] = response.location.longitude
    temp_city['count'] = 1
    city_data.append(temp_city)
  else:
    for item in city_data:
      if item['name'] == response.city.name and item['country'] == response.country.name:
        item['count'] += 1

  if response.country.name != None and response.country.name not in check_country:
    check_country.append(response.country.name)
    temp_country = {}
    temp_country['name'] = response.country.name
    temp_country['count'] = 1
    country_data.append(temp_country)
  else:
    for item in country_data:
      if item['name'] == response.country.name:
        item['count'] += 1
  
city_excel_frame = pd.DataFrame(city_data)
city_excel_frame.to_excel("../processedData/ip_cities.xlsx", index=False) 

country_excel_frame = pd.DataFrame(country_data)
country_excel_frame.to_excel("../processedData/ip_countries.xlsx", index=False)   