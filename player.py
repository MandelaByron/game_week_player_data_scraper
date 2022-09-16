import pycountry
import json
from selenium import webdriver
from bs4 import BeautifulSoup


options=webdriver.ChromeOptions()

options.add_argument("window-size=5,0")
#url = "25231422346618897466161184991066014710242912075232564827261144631247649555194"

#content = None
player_data_list=[]
def player_browser(player_id):
    with webdriver.Chrome('chromedriver.exe',options=options) as driver:
        driver.get('https://www.soraredata.com/apiv2/players/info/' + player_id)
        content=driver.page_source
        get_player_data(content)
        return player_data_list
        #return content
      

#content=driver.page_source
def get_player_data(func):
    
    
    soup = BeautifulSoup(func,'lxml')


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
    player_data_list.append(items)

