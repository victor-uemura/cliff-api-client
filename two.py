# Step 2: takes untagged messages and splits them by sentence and then looks for location identifiers. put all statements w locations into new sheet.

from cliff.api import Cliff
import pandas as pd
import geoip2.database
import re

reader = geoip2.database.Reader("../GeoLite2-City_20210202/GeoLite2-City.mmdb")

my_cliff = Cliff('http://localhost:8080')

file_name = "../processedData/messages.xlsx" # path to file + file name
sheet =  "Sheet1" # sheet name or sheet number or list of sheet numbers and names

df = pd.read_excel(io=file_name, sheet_name=sheet)
excel_data = []
check_repeat = []
for index, row in df.iterrows():
  parsed_row = re.split('[?.:]', row['message'])
  for sentence in parsed_row:
    if (len(sentence.split()) < 4 and len(sentence.strip()) > 2):
      if (sentence.strip() not in check_repeat):
        temp_data = {}
        check_repeat.append(sentence.strip())
        result = my_cliff.parse_text(sentence)
        try:
          targets = result['results']['places']['focus']
          if targets != {} :
            # message, author
            temp_data['author'] = row['author']
            temp_data['message'] = sentence.strip()
            # city data
            temp_data['cities'] = []
            if targets['cities'] != [] :
              for city in targets['cities']:
                temp_data['cities'].append((city['name'], city['lat'], city['lon']))
            #state data
            temp_data['states'] = []
            if targets['states'] != [] :
              for state in targets['states']:
                temp_data['states'].append((state['name'], state['lat'], state['lon']))
            #country data
            temp_data['countries'] = []
            if targets['countries'] != []:
              for country in targets['countries']:
                temp_data['countries'].append((country['name'], country['lat'], country['lon']))
            #ip data
            # ip_info = reader.city(row['ip'])
            temp_data['ip'] = row['ip']
            excel_data.append(temp_data)
        except:
          print("error occured", result)

excel_frame = pd.DataFrame(excel_data)
excel_frame.to_excel("../processedData/targeted_messages.xlsx", index=False)    