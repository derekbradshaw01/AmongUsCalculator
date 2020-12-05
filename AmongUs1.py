


import pandas as pd
import copy

pd.options.display.max_columns = 10

#sheet = pd.read_excel('test.xlsx', 'Sheet1', na_filter=False, usecols=
#                    ["Player Name", "Total Games Played", "Total Imposter Games", "IMP%", "Imp Wins", "Imp Kills", 
#                    "Crew Wins", "Times Murdered", "Times Ejected", "Finished Tasks", "EMs Called", "Bodies Reported"])
#
#sheetdict = sheet.to_dict('index')
#
#playersParent = {}
#creates a dict {name : [any other column name]}
#EX:    players["Birdsaw"]["Total Games Played"]    = 606
#for key in sheetdict:
#    temp = {sheetdict[key]["Player Name"] : sheetdict[key]}
#    playersParent.update(temp)

#Converts each players imposter percentage to a percent, to two decimal places
#for key in playersParent:
#    playersParent[key]["IMP%"] = round(playersParent[key]["IMP%"] * 100, 2)

#playersParent{} is only used to make a copy from here on, playersParent{} is the copy so we dont need to do this each time

#------------------------------------------Here are all the functions used--------------------------------------------------
def init_game():
    print("Hello, and Welcome.  Please Enter the names of players in your game (seperated by a ', ')...")
    names = input()
    lst = names.split(', ')
    print("How many imposters are in your game?")
    IMPcount = int(input())
    temp = []
    for name in lst:#creates dict of each player and thier info--> dict['name']['info']
        temp.append({
            "name"  : name,
            "clear" : False,
            "alive" : True,
            "IMP_percent" : round((IMPcount/len(lst)) * 100, 2)
            })
    
    print("Game with " + str(len(lst)) + " players, " + str(IMPcount) + " imposters, initiating...")
    return temp, len(lst), names, IMPcount

def pull_data(players, IMPcount):
    """
    Displays all info: #Imposters left; Alive players (Confirm clear & likelyhood), Dead players
    prints out the table of info for Alive/Dead players
    
    PARAM:
    players - dict of all players in the game
    numImp - The number of imposters alive

    RETURN:
    NONE

    """
    Alive ={}
    Dead = {}
    DisplayDead = False
    for player in players: #print(player['name'])
        if player['alive'] == True:
            Alive[player['name']] = {
                'clear' :   player['clear'],
                'IMP_percent'   :   player['IMP_percent']             
                }
        if player['alive'] == False:
            Dead[player['name']] = {
                'clear' :   player['clear'],
                'IMP_percent'   :   player['IMP_percent']             
                 }
            DisplayDead = True
    print("<------------------------------------------------------------------------->")
    print("Number of Imposters Remaining: " + str(IMPcount))
    print()
    print("Alive:")
    df_alive = pd.DataFrame.from_dict(Alive)
    print(df_alive)
    print()
    if DisplayDead:
        print("Dead:")
        df_dead = pd.DataFrame.from_dict(Dead)
        print(df_dead)


def percentCalc(players, IMPcount):#this is the repetetative function to calculate the likely hood of someone being the imposter
    aliveCount = 0
    clearCount = 0
    for player in players:
        if player['alive'] ==  True:
            aliveCount += 1
        if player['clear'] ==  True and player['alive'] == True:
            clearCount += 1

    for player in players:
       if player['alive'] == True and player['clear'] == False:
            p = {'IMP_percent'   :  round((IMPcount/(aliveCount - clearCount)) * 100, 2)}
            player.update(p)
    return players



def dead(players, numImp, dead):
    """
    Someone Died, So we want to change their 'alive' to False
        then reclaculate everyone's percentages.

    PARAM: 
    players - dict of all players in the game
    numImp - The number of imposters alive
    dead - who died

    RETURN:
    players
    """
    for player in players:
        if player['name'] == dead:
            a = {'alive'    :   False}
            p = {'IMP_percent'   :   0}
            c = {'clear'    :   True}
            player.update(a)
            player.update(p)
            player.update(c)
    players = percentCalc(players, numImp)
    pull_data(players, numImp)
    return players

def clear(players, numImp, cleared):
    """
    Someone is hard cleared, so we want to clear them in 'clear'
        then change thier IMP_percent to 0, then recalc everyone's percentages

    PARAM: 
    players - dict of all players in the game
    numImp - The number of imposters alive
    cleared - who has been cleared

    RETURN:
    players
    """
    for player in players:
        if player['name'] == cleared:
            p = {'IMP_percent'   :   0}
            c = {'clear'    :   True}
            player.update(p)
            player.update(c)
    players = percentCalc(players, numImp)
    pull_data(players, numImp)
    return players

def confirmed_eject(players, numImp, confirmed):
    """
    Confirmed Imposter Eject, we change thier state to dead, set their percent to 100
        recalculate everyone's percentages

    PARAM: 
    players - dict of all players in the game
    numImp - The number of imposters alive
    confirmed - who was a confirmed imposter

    RETURN:
    players
    numImp - we needed to subtract by 1
    """
    for player in players:
        if player['name'] == confirmed:
            a = {'alive'    :   False}
            p = {'IMP_percent'   :   100}
            c = {'clear'    :   False}
            player.update(a)
            player.update(p)
            player.update(c)
            numImp = numImp - 1
    players = percentCalc(players, numImp)
    pull_data(players, numImp)
    return players, numImp

def display_help():
    print("So this is almost easy to understand, but this help section is most likely for my drunk self.")
    print("Basic Functions include:")
    print()
    print("> dead [Player Name]")
    print("This is for when one player is dead. Case-Sensative")
    print()
    print("> clear [Player Name]")
    print("Use this to hard-clear a player.  This is for something")
    print("like a medbay scan.  Can't be undone. Case-Sensative")
    print()
    print("> confirmed [Player Name]")
    print("This is for when you catch a killer, or some circumstance")
    print("where you are 10,000% sure it is them. Can't be Undone.")
    print("Case-Sensative")
    print()
    print("> data")
    print("this is the table that is displayed often, but it seemed")
    print("like a nice feature since it was aready a function. Case-Sensative")
    print()
    print("<------------------------------------------------------------------------->")

def reload_game(players, IMPcount):
    for player in players:
        a = {"clear" : False}
        b = {"alive" : True}
        c = {"IMP_percent" : round((IMPcount/len(players)) * 100, 2)}
        player.update(a)
        player.update(b)
        player.update(c)
    return players




#------------------------------------------This is the actual gameplay logic------------------------------------------------
player, num, roundNames, IMPcount = init_game()

playerStored = copy.deepcopy(player) #allows us to keep a hard copy of current players in game
IMPcountStored = IMPcount#keeps a hard copy of numImposters for when we need to reload a game

while(True):
    if IMPcount == 0:
        print("Reload Game(R) or Edit New(E)?")
        
        
    txt = input().split(" ")

    

    if txt[0] == "data":
        pull_data(player, IMPcount)
    if txt[0] == "dead":
        player = dead(player, IMPcount, txt[1])
    if txt[0] == "clear":
        player = clear(player, IMPcount, txt[1])
    if txt[0] == "confirmed":
        player, IMPcount = confirmed_eject(player, IMPcount, txt[1])
    if txt[0] == "help":
        display_help()
    if txt[0] == "R":
        player = reload_game(playerStored, IMPcountStored)
        IMPcount = IMPcountStored
    if txt[0] == "E":
        var = 1
        #redo init_game() and continue with the program, saving everyone's IMPtracker


    



