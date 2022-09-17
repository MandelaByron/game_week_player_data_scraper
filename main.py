

import time
import pandas as pd
from player import player_browser, get_player_data
from selenium import webdriver
from game import get_game_data, driver
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  
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

API_KEY = ''
options=webdriver.ChromeOptions()

options.add_argument("window-size=5,0")
options.add_argument('--no-sandbox')
options.page_load_strategy = 'eager'
#options.add_argument('--disable-dev-sh-usage')

proxy_options = {
    'proxy': {
        'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
        'https': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
        'no_proxy': 'localhost,127.0.0.1'
    }
}


driver = webdriver.Chrome(ChromeDriverManager().install(), 
                            options=options, 
                            seleniumwire_options=proxy_options)
with driver as driver:
    

    for i,entry in enumerate(target[0:10]):
        try:
            driver.get('https://www.soraredata.com/apiv2/players/info/' + entry['Player Id'])
            

            print(i)
         
            #print(driver.page_source)
            soup = BeautifulSoup(driver.page_source,'lxml')


            jsondata = json.loads(soup.get_text())

            name=jsondata['player']['DisplayName']
            print(f"scraping the data of {name}")

            date_of_birth = jsondata['player']['DateOfBirth']

            team = jsondata['team']['DisplayName']

            league = jsondata['team']["League"]
            try:
                country = jsondata['player']["Country"]
                country=pycountry.countries.get(alpha_2=f'{country}')
            except:
                country=''
            #print(country.name)

            position =jsondata["player"]["Position"]
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
        except:
            pass
            #entry['Player Id']
            #players=player_browser()


            #data={**players[i],**entry}
            
            #print(data)
            #final_data.append(data)


df= pd.DataFrame(player_data_list) 
df.drop(columns=['Player Id'],inplace=True) 
df.replace({False: 0, True: 1}, inplace=True)
df = df[['Game Week','Player Name','Date Of Birth','Contract End','Country','Position','Status','Position ranking','Overal Position Ranking','Team','League','Game_Against','Score','Home/Away','Game_Started','Played Position','Game_Time','Came_From_Bench','Stayed_On_Bench','Out_of_Squad','Goals','Goal_Assists','Penalty_Kicks_Won','Clearances_of_Line','Clean_Sheet','Red_Cards','Yellow Cards','Own Goals','Errors_led_to_goal','Penalty conceded','Penalty Saved','Decisive','All round Score','Total']]
df.to_excel(f'{excel}.xlsx',index=False)
#player_data= browser(player_id='')

#print(response.text)
