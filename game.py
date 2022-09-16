from bs4 import BeautifulSoup
import pandas as pd
import json
from selenium import webdriver

options=webdriver.ChromeOptions()

options.add_argument("window-size=5,0")
#url = "25231422346618897466161184991066014710242912075232564827261144631247649555194"

#content = None

def driver(week):
    with webdriver.Chrome(r'C:\Users\HP\Dropbox\PC\Desktop\Sorare\chromedriver.exe',options=options) as driver:
        driver.get(f'https://www.soraredata.com/apiv2/SO5/userPerformersAll/all/false/{week}/sorare1010/all')
        global game_week 
        game_week=week
        content=driver.page_source
        data=get_game_data(content)
        return data
        #return content
    
def get_game_data(func):
    data =[]
    #json_data=json.loads(text)
    soup = BeautifulSoup(func,'lxml')


    json_data = json.loads(soup.get_text())
    for i,result in enumerate(json_data):
        
    #print(i)
        player_id = result['stats']['PlayerId']
        
        player_team = result['player']['TeamId']
        #print(player_team)
        
        away_team = result['game']['AwayTeamId']
        
        home_team = result['game']['HomeTeamId']
        
        home_goals =result['game']['HomeGoals']
        
        away_goals = result['game']['AwayGoals']
        
        home_team_goals =''
        away_team_goals =''
        
        player_team_home = True
        if player_team == away_team:
            player_team_home = False
            
        if player_team_home == True:
            home_team_goals = home_goals
            away_team_goals = away_goals
        else:
            home_team_goals =away_goals
            away_team_goals = home_goals
        result["away_display_name"]
        result["home_display_name"]  
        game_against = ''
        if player_team ==  home_team:
            game_against = result["away_display_name"]
        else:
            game_against = result["home_display_name"]   
        
        score =str(home_team_goals) + " - " +  str(away_team_goals)
        #print(game_against)
        
        date = result['game']['GameTime']
        
        started = result['stats']['Started']
        
        position = result['player']['Position']
        
        game_time =result['stats']['mins_played']
        
        came_from_bench = result['stats']['SubbedOn']
        #came_from_bench= str(came_from_bench)
        #print(came_from_bench)
    
        #print(type(came_from_bench))
        
        if came_from_bench:
            stayed_on_bench = True
        else:
            stayed_on_bench = False

        #print(stayed_on_bench)   
        
        out_of_squad = True
        
        if result['stats']['OnGameSheet']:
            out_of_squad = False
            
        #print(out_of_squad)
        
        goals = result['stats']['Goals']
        
        goal_assists = result['stats']['AdjustedGoalAssist']
        
        penalty_kicks_won = result['stats']['AssistPenaltyWon']
        
        clearance_offline = result['stats']['ClearanceOffLine']
        
        clean_sheet = result['stats']['CleanSheet']
        
        red_cards = result['stats']['RedCard']
        
        yellow_cards = result['stats']['YellowCard']
        
        own_goals = result['stats']['OwnGoals']
        
        error_led_to_goal= result['stats']['ErrorLeadToGoal']
        
        penalty_conceded = result['stats']['PenaltyConceded']
        
        penalty_save = result['stats']['PenaltySave']
        
        all_round_score = result['stats']['AllAroundScore']
        
        decisve = result['stats']['LevelGK']
        
        overal_score = result['stats']['SO5Score']
        
        items ={
            'Player Id': player_id,
            'Game Week':game_week,
            'Game_Against': game_against,
            'Score':score,
            'Game_Stareted': started,
            'Position': position,
            "Game_Time":game_time,
            'Came_From_Bench':came_from_bench,
            'Stayed_On_Bench':stayed_on_bench,
            'Out_of_Squad':out_of_squad,
            'Goals':goals,
            'Goal_Assists':goal_assists,
            'Penalty_Kicks_Won':penalty_kicks_won,
            'Clearances_of_Line':clearance_offline,
            'Clean_Sheet':clean_sheet,
            'Red_Cards':red_cards,
            'Yellow Cards':yellow_cards,
            'Own Goals':own_goals,
            'Errors_led_to_goal':error_led_to_goal,
            'Penalty conceded':penalty_conceded,
            'Penalty Saved':penalty_save,
            'Decisive':decisve,
            'All round Score':all_round_score,
            'Total': overal_score
        }
        
        data.append(items)
        #print(items)
        
        
    return data

   
    #print(score)