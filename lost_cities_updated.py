import random
import itertools
from collections import Counter
from tkinter import *
from PIL import ImageTk, Image  #  only non_standard dependency you need to DL
import threading
import queue
import time
import numpy as np


class Card(object):
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.showing = True

    def __repr__(self):
        value_name = ""
        color_name = ""
        if self.showing:
            if self.value == 2:
                value_name = "Two"
            if self.value == 3:
                value_name = "Three"
            if self.value == 4:
                value_name = "Four"
            if self.value == 5:
                value_name = "Five"
            if self.value == 6:
                value_name = "Six"
            if self.value == 7:
                value_name = "Seven"
            if self.value == 8:
                value_name = "Eight"
            if self.value == 9:
                value_name = "Nine"
            if self.value == 10:
                value_name = "Ten"
            if self.value == 0:
                value_name = "Wager"
            if self.color == 0:
                color_name = "Red"
            if self.color == 1:
                color_name = "Green"
            if self.color == 2:
                color_name = "White"
            if self.color == 3:
                color_name = "Yellow"
            if self.color == 4:
                color_name = "Blue"    
            return value_name + " of " + color_name
        else:
            return "[CARD]"

class StandardDeck(list):
    def __init__(self):
        super().__init__()
        colors = list(range(5))
        values = [0,0,0,2,3,4,5,6,7,8,9,10]
        self.cards = []
#         for i in values:
#             for j in colors:
#                 a=Card(i, j)
#                 self.cards.append(a)
#         #self.cards=
        [[self.append(Card(i, j)) for j in colors] for i in values]
    def __repr__(self):
        return f"Standard deck of cards\n{len(self)} cards remaining"

    def shuffle(self):
        random.shuffle(self)
        print("\n\n--deck shuffled--")

    def deal(self, location, times=1):
        for i in range(times):
            location.cards.append(self.pop(0))

    def burn(self):
        self.pop(0)

class Player(object):
    def __init__(self, name=None):
        self.name = name
        self.cards = [] # hands//unobserved
        self.cards1 = [] # red on the board
        self.cards2 = [] # green on the board
        self.cards3 = [] # white on the board
        self.cards4 = [] # yellow on the board
        self.cards5 = [] # blue on the board
        self.score = 0
        self.win = False

    def __repr__(self):
        name = self.name
        return name

class Game(object):
    def __init__(self):
        self.game_over = False
        self.possible_responses1 = list(range(0,8))
        self.possible_responses2 = list(range(0,10))
        self.possible_responses3 = list(range(0,6))
        self.round_counter = 0
        self.cards = [] # open whole cards
        self.cards1 = [] # red on the board
        self.cards2 = [] # green on the board
        self.cards3 = [] # white on the board
        self.cards4 = [] # yellow on the board
        self.cards5 = [] # blue on the board
        self.colors = ['Red','Green', 'White', 'Yellow', 'Blue']
        self.player1 = Player()        
        self.player2 = Player()
        self.player1.name = "Player 1"
        self.player2.name = "Player 2"        
        self.list_of_players = [self.player1, self.player2]
        self.winners = []
        self.deck = StandardDeck()        
        self.deck.shuffle()        
        self.deal_hole()
        self.winner = None
        self.action_counter = 0
        self.turn = np.random.randint(2,size=1)[0]
        
    def print_game_info(self):
        pass

    def print_player_info(self):
        player =  self.list_of_players[self.turn]
        player2 =  self.list_of_players[(self.turn+1)%2]
        print("\n")
        print(f"Turn: {player.name}")
        print(f"Cards: {player.cards}")

        print("\n")
        for i in range(5):
            print("Player one open Cards "+ self.colors[i] +" : " + f"{eval('self.player1.cards'+str(i+1))}")
        print("\n")
        for i in range(5):
            print("Whole one open Cards "+ self.colors[i] +" : " + f"{eval('self.cards'+str(i+1))}")
        print("\n")
        for i in range(5):
            print("Player Two open Cards "+ self.colors[i] +" : " + f"{eval('self.player2.cards'+str(i+1))}")
        print("\n")
        


    def deal_hole(self):
        for player in self.list_of_players:
            self.deck.deal(player, 8)


    def clear_board(self):
        self.possible_responses.clear()
        self.cards.clear()
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.winners.clear()
        self.list_of_scores_from_eligible_winners.clear()
        self.list_of_scores_eligible.clear()
        self.round_ended = False
        for player in self.list_of_players:
            player.score.clear()
            player.cards.clear()
            player.win = False

    
    def group_cards(self):
        count=[0]*5
        cards_group=[]
        player = self.list_of_players[self.turn]
        wager_list=[0]*5
        for i in range(5):
            sorted_color_list=[]
            for cd in player.cards:
                if cd.color==i:
                    if cd.value==0:
                        wager_list[i]= wager_list[i]+1
                    sorted_color_list.append(cd)
                    count[i]=count[i]+1  
            sorted_color_list.sort(key=lambda x: x.value)       
            cards_group.extend(sorted_color_list)
        return cards_group, count, wager_list
                
    
    def answer(self, action):
        player = self.list_of_players[self.turn]
        chosen_card =action[0]
        
        player.cards.remove(action[0])
        
        if chosen_card.color>4:
            print("Invalid response")            
        else:
            if action[1] == 1:
                eval("player.cards"+str(chosen_card.color+1)+".append(chosen_card)")

            elif action[1] == 2:
                eval("self.cards"+str(chosen_card.color+1)+".append(chosen_card)")
            cards_count = [len(player.cards1), len(player.cards2), len(player.cards3), len(player.cards4),len(player.cards5)]      
            max_count_index = cards_count.index(max(cards_count))
            for i in range(5):
                #if i!=chosen_card.color:
                    player_color_list= eval("player.cards"+str(i+1))
                    card_color_list= eval("self.cards"+str(i+1))
                    #print(player_color_list, card_color_list)
                    if player_color_list and card_color_list and player_color_list[-1].value<card_color_list[-1].value:
                        print("Pick Up Card", card_color_list[-1])
                        player.cards.append(card_color_list[-1])
                        eval("self.cards"+str(i+1)+".pop(0)")
                        break
                    
            if len(player.cards)<8:     
                player.cards.append(self.deck[0])
                self.deck.pop(0)
        
        #player.score =  self.score_interpreter(player)
        #print(player, "'s policy: ", action) 
        #print(player, "'s score after the action: ", player.score) 
        print( "The number of cards left in the deck: ", len(self.deck))
        print("\n")        
        self.turn += 1
        self.turn %= 2
        
        
    def returnplayer (self):
        playername = self.list_of_players[self.turn].name
        return playername
    
    def score_interpreter(self, player):
        score = 0
        score_list=[0]*5
        wager_list=[0]*5
        for j in range(5):
            player_cards=eval("player.cards"+str(j+1))
            if len(player_cards) > 0:
                score_list[j]=-20
                for i in player_cards:
                    score_list[j] += i.value
                    if i.value == 0:
                        wager_list[j] += 1 
                score_list[j] = score_list[j]*  (1+wager_list[j])  
        return sum(score_list)
    
    def end_game(self):
        print(self.deck)
        if len(self.deck) == 0:
            return True
        else:
            return False
        
    def find_winners(self):
        s1 = self.score_interpreter(self.player1)
        s2 = self.score_interpreter(self.player2)
        print(f"Scores: Player1: {s1}, Player 2: {s2}")
        if s1>s2:
            print("Player 1 won.")
        if s1==s2:
            print("Tied.")
        if s1<s2:
            print("Player 2 won.")    
            
        
     
    def initialize (self):
        self.cards.shuffle()
        self.deal_hole()
        self.turn = self.list_of_players(self.first_actor)
    
        
    def finalize (self):    
        self.score_all()       
        self.find_winners()
        self.round_ended = True
        

class Agent ():
    def policy (self, game):
        #action = [np.random.randint(8,size=1)[0]+1,np.random.randint(2,size=1)[0]+1,6] # random action and get a card from the deck
        #return action 
        card_list, count, wager_list=game.group_cards()

        print(count, card_list)

        
        card_chosen_min=card_list[0]
        card_chosen_max=card_list[0]
        player = game.list_of_players[game.turn]
        
        
        #First Choice is already wager is registered
        
        for i in range(5):
                color_list_card = eval("player.cards"+str(i+1))
                if i==0:
                    index=0
                else:
                    index=sum(count[0:i])
                    if index==8:
                        index=7
                    print(color_list_card, index, "updating scoring", count[0:i], i )
                if len(color_list_card)>=1 and count[i]>=1 and color_list_card[-1].value<=card_list[index].value and (color_list_card[-1].value>=4 or card_list[index].value<5):
                    action=[card_list[index], 1, 6]
                    return action
                
        # Last stage of game just accumulating cards to score if already wager is set 
        if len(game.deck)<=15:
            for i in range(5):
                color_list_card = eval("player.cards"+str(i+1))
                if len(color_list_card)>=1 and count[i]>=1 and color_list_card[-1].value<=card_list[sum(count[0:i+1])-1].value:
                    action=[card_list[sum(count[0:i+1])-1], 1, 6]
                    return action
        max_value = max(count)
        max_index = count.index(max_value) 
        min_value = 10
        for i in range(5):
            if count[i]!=0 and min_value>count[i]:
                min_value=count[i]
                min_index = i
        
        if max_index!=0:
            print("Max list index", sum(count[0:max_index+1])-1, max_index)
            card_chosen_max=card_list[sum(count[0:max_index+1])-1]
        if min_index!=0:
            card_chosen_min=card_list[sum(count[0:min_index+1])-1]
            print("Min list index", sum(count[0:min_index+1])-1, min_index)
        card_min_list = eval("player.cards"+str(card_chosen_min.color+1))
        card_max_list = eval("player.cards"+str(card_chosen_max.color+1))
        print(card_min_list, "card min list", min_index)
        print(card_min_list, "card max list", max_index)
        action=[]
        
        # Registering wagers for first few turns till len of deck is >15 if we have extra card along with wager
        if sum(wager_list)>0:
            for i in range(len(wager_list)):
                if wager_list[i] and count[i]-wager_list[i]>=1:
                    color_list_card = eval("player.cards"+str(i+1))
                    print("In wager list", color_list_card, sum(count[0:i]), wager_list[i], i)
                    if len(color_list_card)==0 or (len(color_list_card)<3 and color_list_card[-1].value==0):
                        action=[card_list[sum(count[0:i])], 1, 6]
                        return action                
        
                
        # Keep on registering if count is more than 2 and minimum value is less than 5 till deck length is greater than 15
        if count[max_index]>=2:
            if card_max_list and card_max_list[-1].value<=card_chosen_max.value and (card_max_list[-1].value>=4 or card_chosen_max.value<5):
                action=[card_chosen_max, 1, 6]  
            elif card_chosen_max.value==0:
                action=[card_chosen_max, 1, 6]  
            print("Max")
        print(action, "after max")
        if len(action)==0 and (min_value>=1 or card_chosen_min.value==0 or card_min_list):
            if card_min_list:
                if card_min_list[-1].value<=card_chosen_min.value:
                    print("Min one")
                    action=[card_chosen_min, 1, 6]  
                else:
                    print("Min two")
                    action=[card_chosen_min, 2, 6]
            elif card_chosen_min.value==0:
                action=[card_chosen_min, 1, 6] 
            else:
                print("Min not wager")
                action=[card_chosen_min, 2, 6]
       
        if len(action)==0:
            print("Main Two")
            action=[card_chosen_min, 2, 6]
        
        #print(action)
        
        return action
            

isEnd = False
a1 = Agent()
a2 = Agent()
game0 = Game()

while isEnd == False:
   
    game0.print_player_info()
    if game0.returnplayer() == "Player 1":
        a = a1.policy(game0)
        print(a)
        game0.answer(a)   
    else:
        a = a2.policy(game0)
        print(a)
        game0.answer(a)
        
    if game0.end_game():
        isEnd = True

game0.find_winners()    


