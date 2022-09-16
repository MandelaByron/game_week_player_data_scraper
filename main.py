

import time
import pandas as pd
from player import player_browser, get_player_data
from selenium import webdriver
from game import get_game_data, driver
from bs4 import BeautifulSoup
import pycountry
import json

with open('week.json','r') as f:
    data=json.load(f)
    start=data['start']
    end=data['end']
    excel = data['excel_name']
#url = "https://www.soraredata.com/apiv2/SO5/userPerformersAll/all/false/304/sorare1010/all"

target=[]
for i in range(start,end):
    new=game_data=driver(i)
    target=target + new
    #game_data=driver(i)

#target=set(target)

print(len(target))
#game_data
final_data=[]
player_data_list=[]
with webdriver.Chrome('chromedriver.exe') as driver:
    

    for i,entry in enumerate(target):
        
        driver.get('https://www.soraredata.com/apiv2/players/info/' + entry['Player Id'])
        time.sleep(1)
        #print(driver.page_source)
        soup = BeautifulSoup(driver.page_source,'lxml')


        jsondata = json.loads(soup.get_text())

        name=jsondata['player']['FullName']
        print(f"scraping the data of {name}")

        date_of_birth = jsondata['player']['DateOfBirth']

        team = jsondata['team']['DisplayName']

        league = jsondata['team']["League"]

        country = jsondata['player']["Country"]
        country=pycountry.countries.get(alpha_2=f'{country}')
        #print(country.name)

        position =jsondata["position"]["main_position"]
        try:

            contract_end=jsondata["contract_end"]
            #print(contract_end)
            n=contract_end.split('T')
            contract_end=n[0]
        except:
            contract_end='-'

        status = jsondata['player']["PlayingStatus"]

        position_ranking = jsondata["position_ranking"]

        position_ranking_overal= jsondata["overall_ranking"]
        
        items={
            'Player Name': name,
            'Date Of Birth': date_of_birth,
            'Team': team,
            'League': league,
            'Country': country.name,
            'Position':position,
            'Contract End': contract_end,
            'Status': status,
            'Position ranking':position_ranking,
            'Overal Position Ranking': position_ranking_overal
        }
        #print(len(player_data_list))
        items = {**entry,**items}
        player_data_list.append(items)
            #entry['Player Id']
            #players=player_browser()


            #data={**players[i],**entry}
            
            #print(data)
            #final_data.append(data)


df= pd.DataFrame(player_data_list) 
df.drop(columns=['Player Id'],inplace=True) 
df.to_excel(f'{excel}.xlsx',index=False)
#player_data= browser(player_id='')

#print(response.text)