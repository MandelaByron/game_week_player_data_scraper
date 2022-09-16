
import pandas as pd
from player import player_browser, get_player_data

from game import get_game_data, driver
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
try:
    for i,entry in enumerate(target[0:100]):
        #entry['Player Id']
        players=player_browser(entry['Player Id'])


        data={**players[i],**entry}
        
        #print(data)
        final_data.append(data)
except:
    pass

df= pd.DataFrame(final_data) 
df.drop(columns=['Player Id'],inplace=True) 
df.to_excel(f'{excel}.xlsx',index=False)
#player_data= browser(player_id='')

#print(response.text)