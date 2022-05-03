from django.db import models
import random
import itertools
from collections import Counter
from tkinter import *
from PIL import ImageTk, Image  #  only non_standard dependency you need to DL
import threading
import queue
import time
import numpy as np
import copy

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
        values = [2,3,4,5,6,7,8,9,10,0,0,0]
        #self.cards = []
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
            location.hands.append(self.pop(0))

    def burn(self):
        self.pop(0)

class Player(object):
    def __init__(self, name=None):
        self.name = name
        self.hands = [] # hands//unobserved
        self.cards = [[],[],[],[],[]] # expedition columns red/green/white/yellow/blue
        self.score = 0
        self.win = False

    def __repr__(self):
        name = self.name
        return name

class Game(object):
    _instance = None

    def __init__(self):
        self.game_over = False
        #self.round_counter = 0
        self.cards = [[],[],[],[],[]] # discrad deck red/green/white/yellow/blue
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
        self.turn = np.random.randint(2,size=1)[0]
        self.recent_action = []
        
    def print_game_info(self):
        pass

    @staticmethod
    def is_instance(is_new=False):
        if not Game._instance or is_new:
           Game._instance = Game()
        return Game._instance
    
    def print_player_info(self):
        player =  self.list_of_players[self.turn]
        player2 =  self.list_of_players[(self.turn+1)%2]
        print("\n")
        print(f"Turn: {player.name}")
        print(f"Cards: {player.hands}")

        print("\n")
        for i in range(5):
            print("Player's Cards on the expedition columns "+ self.colors[i] +" : " + f"{player.cards[i]}")
        print("\n")
        for i in range(5):
            print("Discard deck "+ self.colors[i] +" : " + f"{self.cards[i]}")
        print("\n")
        for i in range(5):
            print("Oppenent's Cards on the expedition columns "+ self.colors[i] +" : " + f"{player2.cards[i]}")
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
            player.hands.clear()
            player.win = False

    def group_cards1(self):
        count=[0]*5
        cards_group=[]
        player = self.list_of_players[self.turn]
        wager_list=[0]*5
        score_of_cards=[0]*5
        for i in range(5):
            sorted_color_list=[]
            for cd in player.hands:
                if cd.color==i:
                    if cd.value==0:
                        wager_list[i]= wager_list[i]+1
                    sorted_color_list.append(cd)
                    count[i]=count[i]+1  
                    score_of_cards[i]=cd.value+score_of_cards[i]
            sorted_color_list.sort(key=lambda x: x.value)       
            cards_group.append(sorted_color_list)
        return cards_group, count, wager_list, score_of_cards
    
    def group_cards(self):
        count=[0]*5
        cards_group=[]
        player = self.list_of_players[self.turn]
        wager_list=[0]*5
        score_of_cards=[0]*5
        for i in range(5):
            sorted_color_list=[]
            for cd in player.hands:
                if cd.color==i:
                    if cd.value==0:
                        wager_list[i]= wager_list[i]+1
                    sorted_color_list.append(cd)
                    count[i]=count[i]+1  
                    score_of_cards[i]=cd.value+score_of_cards[i]
            sorted_color_list.sort(key=lambda x: x.value)       
            cards_group.extend(sorted_color_list)
        return cards_group, count, wager_list, score_of_cards
                
    
    def answer(self, action):
        
        action[0] = int(action[0]) 
        action[1] = int(action[1])
        action[2] = int(action[2])
        
        if action[0] not in [1,2,3,4,5,6,7,8]: # chosen card number
            print("Invalid response")
            return False
        if action[1] not in [1,2]: # 1: register, 2: discard
            print("Invalid response")
            return False
        if action[2] not in [1,2,3,4,5,6]: # 1 ~ 5: get a card from the discard pile, 6: get a card from the draw deck
            print("Invalid response")
            return False
        
            
        player = self.list_of_players[self.turn]
        chosen_card = player.hands[action[0]-1]        
        
        if action[1] == 2 and chosen_card.color == action[2] - 1:
            print("Invalid response")
            return False
        
        if action[1] == 1: # register the chosen card on an expedition column
            if len(player.cards[chosen_card.color]) > 0:
                #print(player.cards[chosen_card.color])
                if chosen_card.value < player.cards[chosen_card.color][0].value:
                    print("Invalid response")
                    return False
                else: 
                    player.cards[chosen_card.color].insert(0,chosen_card)
            else:
                player.cards[chosen_card.color].insert(0,chosen_card)
        elif action[1] == 2: # discard the chosen card on the discard pile
            self.cards[chosen_card.color].insert(0,chosen_card)
        #cards_count = [len(player.hands[0]), len(player.hands[1]), len(player.hands[2]), len(player.hands[3]),len(player.hands[4])]      
        #max_count_index = cards_count.index(max(cards_count))
        
        if action[2] < 6: 
            if len(self.cards[action[2]-1]) == 0: # trying to take a card from the discard deck with no card
                print("Invalid response")
                return False
            else:
                player.hands.append(self.cards[action[2]-1][0])
                self.cards[action[2]-1].pop(0)
        else:
            player.hands.append(self.deck[0])
            self.deck.pop(0)                
                
            #for i in range(5):
            #    #if i!=chosen_card.color:
            #        player_color_list = player.cards[i]
            #        card_color_list= self.cards[i]
            #        #print(player_color_list, card_color_list)
            #        if player_color_list and card_color_list and player_color_list[-1].value<card_color_list[-1].value:
            #            print("Pick Up Card", card_color_list[-1])
            #            player.hands.append(card_color_list[-1])
            #            self.cards[i].pop(0)
            #            break
                    
            #if len(player.cards)<8:     
            #    player.cards.append(self.deck[0])
            #    self.deck.pop(0)
        
        #player.score =  self.score_interpreter(player)
        #print(player, "'s policy: ", action) 
        #print(player, "'s score after the action: ", player.score)
        player.hands.remove(chosen_card)
        self.recent_action = action
        print( "The number of cards left in the deck: ", len(self.deck))
        print("\n")        
        self.turn += 1
        self.turn %= 2
        return True
        
        
    def returnplayer (self):
        playername = self.list_of_players[self.turn].name
        return playername
    
    def score_interpreter(self, player):
        
        score_list=[0]*5
        wager_list=[0]*5
        for j in range(5):
            player_cards=player.cards[j]
            if len(player_cards) > 0:
                score_list[j]=-20
                for i in player_cards:
                    score_list[j] += i.value
                    if i.value == 0:
                        wager_list[j] += 1 
                score_list[j] = score_list[j]*  (1+wager_list[j])
                if len(player_cards) >= 8:
                    score_list[j] += 20
                    
        return (score_list)
    
    def end_game(self):
        print(self.deck)
        if len(self.deck) == 0:
            return True
        else:
            return False
        
    def find_winners(self):
        s1 = sum(self.score_interpreter(self.player1))
        s2 = sum(self.score_interpreter(self.player2))
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
        
