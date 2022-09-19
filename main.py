

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
import datetime
import unicodedata
from league_country import league_country
from datetime import datetime as dt

with open('week.json','r') as f:
    data=json.load(f)
    start=data['start']
    end=data['end']
    excel = data['excel_name']
#url = "https://www.soraredata.com/apiv2/SO5/userPerformersAll/all/false/304/sorare1010/all"
def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
target=[]
for i in range(start,end):
    #driver(i)
    game_data=driver(i)
    new=game_data
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
    
### change this to limit the results. 
### "target" fetches all. target[0:n] limits upto the first n-1
    for i,entry in enumerate(target[90:130]):
        try:
 
            driver.get('https://www.soraredata.com/apiv2/players/info/' + entry['Player Id'])
            

            print(i)
            
            #print(driver.page_source)
            soup = BeautifulSoup(driver.page_source,'lxml')
            
            


            jsondata = json.loads(soup.get_text())

            name=jsondata['player']['DisplayName']
            print(f"scraping the data of {name}")
            
            status_updates=jsondata['availabilityStatus']['status']
            origins = jsondata['availabilityStatus']['origins']

            description = jsondata['availabilityStatus']['description']
            print(description)
            if description == '':
                Status = ''
                updated=''
                sources=''
                until =''
                if origins == 'Default':
                    origins = ''
                
            else:
                Status = status_updates + f'({description})'
                sources = jsondata['availabilityStatus']['sources']
                try:
                    until = jsondata['availabilityStatus']['until']
                    until = str(until)
                    n=until.split('T')
                    until=n[0]
                    test_string =until
                    test_string=test_string.replace('-','/')
                    until=datetime.datetime.strptime(test_string,'%Y/%m/%d').strftime('%m/%d/%Y')
                except:
                    until =''
            #until = dt.fromisoformat(until[:-1])
                updated = jsondata['availabilityStatus']['updatedAt']
                updated = dt.fromisoformat(updated[:-1])
                test=str(updated)
                test=test.split(" ")
                new=datetime.datetime.strptime(test[0], "%Y-%m-%d").strftime("%m/%d/%Y")
                new=new + " " + test[1]
                updated=''.join(new)


            date_of_birth = jsondata['player']['DateOfBirth']
            test_string =date_of_birth
            #test_string=test_string.replace('-','/')
            date_of_birth=datetime.datetime.strptime(test_string,'%d/%m/%Y').strftime('%m/%d/%Y')
            

            team = jsondata['team']['DisplayName']

            league = jsondata['team']["League"]
            
            slug = jsondata['team']['LeagueSlug']
            
            league_count=league_country(slug)
            print(league_count)
            


                
            try:
                country = jsondata['player']["Country"]           
                country=pycountry.countries.get(alpha_2=f'{country}')
                country= country.name
                
            except:
                country = jsondata['player']['NationalTeam']
                country = country.title()
            #print(country.name)

            position =jsondata["player"]["Position"]
            if position == 'Defender':
                position = 'D'
            elif position == 'Goalkeeper':
                position = 'G'
            elif position == 'Forward':
                position = 'F'
            
            elif position == 'Midfielder':
                position = 'M'
            else:
                pass
            
            try:

                contract_end=jsondata["contract_end"]
                #print(contract_end)
                n=contract_end.split('T')
                contract_end=n[0]
                test_string =contract_end
                test_string=test_string.replace('-','/')
                contract_end=datetime.datetime.strptime(test_string,'%Y/%m/%d').strftime('%m/%d/%Y')
            except:
                contract_end='-'

            status = jsondata['player']["PlayingStatus"]

            position_ranking = jsondata["position_ranking"]
            
            if position_ranking == -1:
                position_ranking = 'N/A'

            position_ranking_overal= jsondata["overall_ranking"]
            if position_ranking_overal == -1:
                position_ranking_overal = 'N/A'
            
            items={
                'Player Name': strip_accents(name).replace('ł','l'),
                'Date Of Birth': date_of_birth,
                'Team': strip_accents(team),
                'League': strip_accents(league) + " - " + league_count,               
                'Country': country,
                'Position':position,
                'Contract End': contract_end,
                'Status': status,
                'Position ranking':position_ranking,
                'Overal Position Ranking': position_ranking_overal,
                'Status_Player': Status,
                'Source':sources,
                'Until':until,
                'UpdatedAt': updated
            }
            #print(len(player_data_list))
            items = {**entry,**items}
            #print(items)
            player_data_list.append(items)
        except Exception as e:
            print(e)
            pass
            #entry['Player Id']
            #players=player_browser()


            #data={**players[i],**entry}
            
            #print(data)
            #final_data.append(data)


df= pd.DataFrame(player_data_list) 
df.drop(columns=['Player Id'],inplace=True) 
df.replace({False: 0, True: 1}, inplace=True)
df = df[['Game Week','Player Name','Date Of Birth','Contract End','Country','Position','Status','Position ranking','Overal Position Ranking','Team','League','Status_Player','Source','Until','UpdatedAt','Game_Against','Score','Home/Away','Game_Started','Played Position','Game_Time','Came_From_Bench','Stayed_On_Bench','Out_of_Squad','Goals','Goal_Assists','Penalty_Kicks_Won','Clearances_of_Line','Clean_Sheet','Red_Cards','Yellow Cards','Own Goals','Errors_led_to_goal','Penalty conceded','Penalty Saved','Decisive','All round Score','Total']]
df.to_excel(f'{excel}.xlsx',index=False)
#player_data= browser(player_id='')

#print(response.text)
