#Step 4: takes messages and makes sure location is counted once per author
from cliff.api import Cliff
import pandas as pd
import ast

file_name = "../processedData/final_targeted_messages.xlsx" # path to file + file name
sheet =  "Sheet1" # sheet name or sheet number or list of sheet numbers and names

df = pd.read_excel(io=file_name, sheet_name=sheet)
excel_data = []
author_id = []
for index, row in df.iterrows():
  if row['author'] not in author_id or str(row['author']) == "0":
    author_id.append(row['author'])
    temp_data = {}
    temp_data['author'] = row['author']
    temp_data['cities'] = row['cities']
    temp_data['states'] = row['states']
    temp_data['countries'] = row['countries']
    excel_data.append(temp_data)
  else:
    for data_row in excel_data:
      if data_row['author'] == row['author']:
        if row['cities'] != []:
          for city in ast.literal_eval(row['cities']):
            if city not in ast.literal_eval(data_row['cities']):
              temp_cities = ast.literal_eval(data_row['cities'])
              temp_cities.append(city)
              data_row['cities'] = str(temp_cities)
        if row['states'] != []:
          for state in ast.literal_eval(row['states']):
            if state not in ast.literal_eval(data_row['states']):
              temp_state = ast.literal_eval(data_row['states'])
              temp_state.append(state)
              data_row['states'] = str(temp_state)
        if row['countries'] != []:
          for country in ast.literal_eval(row['countries']):
            if country not in ast.literal_eval(data_row['countries']):
              temp_country = ast.literal_eval(data_row['countries'])
              temp_country.append(country)
              data_row['countries'] = str(temp_country)

excel_frame = pd.DataFrame(excel_data)
excel_frame.to_excel("../processedData/author_location.xlsx", index=False)  
