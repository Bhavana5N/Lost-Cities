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
        self.cards = []
        self.player1 = Player()        
        self.player2 = Player()
        self.player1.name = "Player 1"
        self.player2.name = "Player 2"        
        self.list_of_players = [self.player1,self.player2]
        self.winners = []
        self.deck = StandardDeck()        
        self.deal_hole()
        self.winner = None
        self.action_counter = 0
        self.attribute_list = ["p1", "p2"]
        
    def print_game_info(self):
        pass

    def print_round_info(self):
        print("\n")
        for player in self.list_of_players:
            print("\n")
            print(f"Name: {player.name}")
            print(f"Cards: {player.cards}")
            print(f"Player score: {player.score}")
            print("\n")
            print(f"Player open Cards 1: {player.cards1}")
            print(f"Player open Cards 2: {player.cards2}")
            print(f"Player open Cards 3: {player.cards3}")
            print(f"Player open Cards 4: {player.cards4}")
            print(f"Player open Cards 5: {player.cards5}")
        print("\n")
        print(f"Whole open Cards: {self.cards}")

    def establish_player_attributes(self):
        address_assignment = 0
        self.dealer = self.list_of_players_not_out[address_assignment]
        self.dealer.list_of_special_attributes.append("first")
        address_assignment += 1
        address_assignment %= len(self.list_of_players_not_out)
        self.small_blind = self.list_of_players_not_out[address_assignment]
        self.small_blind.list_of_special_attributes.append("second")


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
            player.list_of_special_attributes.clear()
            player.win = False
    

    def answer(self, action):
    
        player = self.list_of_players_not_out[self.turn]
        
        print(f"Current Score: {player.score}")
        print(f"Players Cards: {player.cards}")
                                
        self.turn += 1
        self.turn %= 2
        
        choson_card = player.cards[action[0]-1]
        player.cards.pop(action[0]-1)
        
        if action[1] == 1:
            player.cards1.insert(choson_card)
        if action[1] == 2:    
            player.cards2.insert(choson_card)
        if action[1] == 3:    
            player.cards3.insert(choson_card)
        if action[1] == 4:    
            player.cards4.insert(choson_card)
        if action[1] == 5:    
            player.cards5.insert(choson_card)
        
        if action[1] == 6:
            self.cards1.insert(choson_card)
        if action[1] == 7:    
            self.cards2.insert(choson_card)
        if action[1] == 8:    
            self.cards3.insert(choson_card)
        if action[1] == 9:    
            self.cards4.insert(choson_card)
        if action[1] == 10:    
            self.cards5.insert(choson_card)
            
        if action[2] == 1:
            player.cards.insert(0,self.cards1[0])
            self.cards1.pop(0)
        if action[2] == 2:
            player.cards.insert(0,self.cards2[0])
            self.cards2.pop(0)
        if action[2] == 3:
            player.cards.insert(0,self.cards3[0])
            self.cards3.pop(0)
        if action[2] == 4:
            player.cards.insert(0,self.cards4[0])
            self.cards4.pop(0)
        if action[2] == 5:
            player.cards.insert(0,self.cards5[0])
            self.cards5.pop(0)
        if action[2] == 6:
            player.cards.insert(0,self.cards[0])
            self.cards.pop(0)
        

    def score_interpreter(player):
        player.score = 0
        if len(player.card1) > 0:
            player.score += (- 20 + np.sum(player.card1.values)) * (1 + np.sum(np.where(np.array(player.card1.values) == 0,1,0)))
        if len(player.card2) > 0:
            player.score += (- 20 + np.sum(player.card2.values)) * (1 + np.sum(np.where(np.array(player.card2.values) == 0,1,0)) )
        if len(player.card3) > 0:
            player.score += (- 20 + np.sum(player.card3.values)) * (1 + np.sum(np.where(np.array(player.card3.values) == 0,1,0)) )
        if len(player.card4) > 0:
            player.score += (- 20 + np.sum(player.card4.values)) * (1 + np.sum(np.where(np.array(player.card4.values) == 0,1,0)))
        if len(player.card5) > 0:
            player.score += (- 20 + np.sum(player.card5.values)) * (1 + np.sum(np.where(np.array(player.card5.values) == 0,1,0)) )
            
        return player.score
    
    def end_game(self):
        if len(self.cards) == 0:
            return True
        else:
            return False
        
    def find_winners(self):
        s1=score_interpreter(self.player1)
        s2=score_interpreter(self.player2)
        print(f"Scores: Player1: {s1}, Player 2: {s2}")
        if s1>s2:
            print("player 1 won.")
        if s1==s2:
            print("Tie")
        if s1<s2:
            print("Player 2 won.")    
            
        
     
    def initialize (self):
        self.deck.shuffle()
        self.establish_player_attributes()
        self.deal_hole()
        self.turn = self.list_of_players_not_out.index(self.first_actor)
    
        
    def finalize (self):    
        self.score_all()       
        self.find_winners()
        self.round_ended = True
        

isEnd = True
game = Game()
game.print_round_info()


        



