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
        self.player1 = Player()        
        self.player2 = Player()
        self.player1.name = "Player 1"
        self.player2.name = "Player 2"        
        self.list_of_players = [self.player1,self.player2]
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
        print(f"Player score: {player.score}")
        print("\n")
        print(f"Player open Cards Red    : {player.cards1}")
        print(f"Player open Cards Green  : {player.cards2}")
        print(f"Player open Cards White  : {player.cards3}")
        print(f"Player open Cards Yellow : {player.cards4}")
        print(f"Player open Cards Blue   : {player.cards5}")
        print("\n")
        print(f"Whole open Cards Red    : {self.cards1}")
        print(f"Whole open Cards Green  : {self.cards2}")
        print(f"Whole open Cards White  : {self.cards3}")
        print(f"Whole open Cards Yellow : {self.cards4}")
        print(f"Whole open Cards Blue   : {self.cards5}")
        print("\n")
        print(f"The other Player open Cards Red    : {player2.cards1}")
        print(f"The other Player open Cards Green  : {player2.cards2}")
        print(f"The other Player open Cards White  : {player2.cards3}")
        print(f"The other Player open Cards Yellow : {player2.cards4}")
        print(f"The other Player open Cards Blue   : {player2.cards5}")
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
    

    def answer(self, action):
        player = self.list_of_players[self.turn]
        chosen_card = player.cards[action[0]-1]
        
        player.cards.pop(action[0]-1)
        
        if chosen_card.color == (action[2]-1):
            print("Invalid response")            
        else:
            if action[1] == 1:
                if chosen_card.color == 0:
                    player.cards1.insert(0,chosen_card)
                elif chosen_card.color == 1:    
                    player.cards2.insert(0,chosen_card)
                elif chosen_card.color == 2:    
                    player.cards3.insert(0,chosen_card)
                elif chosen_card.color == 3:    
                    player.cards4.insert(0,chosen_card)
                elif chosen_card.color == 4:    
                    player.cards5.insert(0,chosen_card)
            elif action[1] == 2:
                if chosen_card.color == 0:
                    self.cards1.insert(0,chosen_card)
                elif chosen_card.color == 1:    
                    self.cards2.insert(0,chosen_card)
                elif chosen_card.color == 2:    
                    self.cards3.insert(0,chosen_card)
                elif chosen_card.color == 3:    
                    self.cards4.insert(0,chosen_card)
                elif chosen_card.color == 4:    
                    self.cards5.insert(0,chosen_card)
                    
            if action[2] == 1:
                player.cards.insert(0,self.cards1[0])
                self.cards1.pop(0)
            elif action[2] == 2:
                player.cards.insert(0,self.cards2[0])
                self.cards2.pop(0)
            elif action[2] == 3:
                player.cards.insert(0,self.cards3[0])
                self.cards3.pop(0)
            elif action[2] == 4:
                player.cards.insert(0,self.cards4[0])
                self.cards4.pop(0)
            elif action[2] == 5:
                player.cards.insert(0,self.cards5[0])
                self.cards5.pop(0)
            elif action[2] == 6:            
                player.cards.insert(0,self.deck[0])
                self.deck.pop(0)
        
        player.score =  self.score_interpreter(player)
        print(player, "'s policy: ", action) 
        print(player, "'s score after the action: ", player.score) 
        print( "The number of cards left in the deck: ", len(self.deck))
        print("\n")        
        self.turn += 1
        self.turn %= 2
        
        
    def returnplayer (self):
        playername = self.list_of_players[self.turn].name
        return playername
    
    def score_interpreter(self, player):
        score = 0
        score1 = -20
        score2 = -20
        score3 = -20
        score4 = -20
        score5 = -20
        num_wager1 = 0
        num_wager2 = 0
        num_wager3 = 0
        num_wager4 = 0
        num_wager5 = 0
        
        if len(player.cards1) > 0:
            for i in range(0,len(player.cards1)):
                score1 += player.cards1[i].value
                if player.cards1[i].value == 0:
                    num_wager1 += 1                    
            score += score1 * (1 + num_wager1)
            
        if len(player.cards2) > 0:
            for i in range(0,len(player.cards2)):
                score2 += player.cards2[i].value
                if player.cards2[i].value == 0:
                    num_wager2 += 1                    
            score += score2 * (1 + num_wager2)            

        if len(player.cards3) > 0:
            for i in range(0,len(player.cards3)):
                score3 += player.cards3[i].value
                if player.cards3[i].value == 0:
                    num_wager3 += 1                    
            score += score3 * (1 + num_wager3)   
        if len(player.cards4) > 0:
            for i in range(0,len(player.cards4)):
                score4 += player.cards4[i].value
                if player.cards4[i].value == 0:
                    num_wager4 += 1                    
            score += score4 * (1 + num_wager4)   
        if len(player.cards5) > 0:
            for i in range(0,len(player.cards5)):
                score5 += player.cards5[i].value
                if player.cards5[i].value == 0:
                    num_wager5 += 1
            score += score5 * (1 + num_wager5)   
        
        return score
    
    def end_game(self):
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
    def policy (self):
        action = [np.random.randint(8,size=1)[0]+1,np.random.randint(2,size=1)[0]+1,6] # random action and get a card from the deck
        return action    
        
    

isEnd = False
a1 = Agent()
a2 = Agent()
game0 = Game()

while isEnd == False:
    game0.print_player_info()
    
    if game0.returnplayer() == "Player 1":
        a = a1.policy()
        game0.answer(a)
           
    else:
        a = a2.policy()
        game0.answer(a)
        
    if game0.end_game():
        isEnd = True
    
game0.find_winners()    



