import imp
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
from itertools import chain
from multiprocessing import Process
import threading 
import itertools

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
        self.recent_action = [-1,-1,-1]
        self.recent_action2 = [-1,-1,-1]
        self.recent_chosen_card = Card(-1,0)
        self.recent_cards =[[],[],[],[],[]] # discrad deck red/green/white/yellow/blue
        self.s1 = 0
        self.s2 = 0
   
    def isTerminal(self):
        if len(self.deck)==0:
            return True

    def takeAction(self, action):
         
         self.answer([action.card, action.action, action.pickup]) 
         return self  

    def getReward (self):
        if len(self.deck)==0:
            return sum(self.score_interpreter(self.player1))
        return False
    def getPossibleActions(self):
        
            card_list, count, wager_list, score_list= self.group_cards()
            #print(card_list, count, wager_list, score_list )
            player = self.list_of_players[self.turn]
            player2 =  self.list_of_players[(self.turn+1)%2]
            palyer_score_list=self.score_interpreter(player)
            #print(player.cards)
            action_list1=[]
            for i in range(5):
                action_1 = -1
                player_color_list = player.cards[i]
                #print(player_color_list)
                if (card_list[i] and player_color_list and player_color_list[0].value<=card_list[i][0].value) or (card_list[i]):
                    action_list1.append(card_list[i][0])


            action_list2=[1, 2]
            action_2=6
            action_list3=[6]
            for i in range(5):
                player_color_list = player.cards[i]
                card_color_list= self.cards[i]
                if player_color_list and card_color_list and player_color_list[0].value<card_color_list[0].value:
                    #print("Pick Up Card", card_color_list[0])
                    action_list3.append(i+1)
            #print(action_list3, action_list1)
            p = itertools.product(action_list1, action_list2, action_list3)
            q=[]
            for i in p:
                a=[0,0,0]
                if i[0].color == i[2]-1 and i[1]==2:
                    continue
                else:
                    a[0]=player.hands.index(i[0])+1
                    a[1]=i[1]
                    a[2]=i[2]
                    q.append(Action(player.name, a[0], a[1], a[2]))
            #print(q)

            
            #print(list(p))
            #print(list(q))

            return q

    def print_game_info(self):
        pass

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
            cards_group.append(sorted_color_list)
            
        return cards_group, count, wager_list, score_of_cards
    
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
            cards_group.extend(sorted_color_list)
        return cards_group, count, wager_list, score_of_cards 
    
    def group_cards2(self, hands):
        count=[0]*5
        cards_group=[]
        wager_list=[0]*5
        score_of_cards=[0]*5
        for i in range(5):
            sorted_color_list=[]
            for cd in hands:
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

        if type(action) is list:
            action[0] = int(action[0]) 
            action[1] = int(action[1])
            action[2] = int(action[2])
        else:
            action_1 = [0]*3
            action_1[0] = int(action.card)
            action_1[1] = int(action.action)
            action_1[2] = int(action.pickup)
            action = action_1
        
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
        if not self.deck:
            return False
        if action[2] < 6: 
            if len(self.cards[action[2]-1]) == 0: # trying to take a card from the discard deck with no card
                print("Invalid response")
                return False
            else:
                player.hands.append(self.cards[action[2]-1][0])
                self.recent_cards = copy.deepcopy(self.cards)
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
        print( "The number of cards left in the deck: ", len(self.deck))
        print("\n")        
        self.turn += 1
        self.turn %= 2
        
        self.recent_action2 = copy.deepcopy(self.recent_action)
        self.recent_action = copy.deepcopy(action)
        self.recent_chosen_card = chosen_card
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
        #print(self.deck)
        if len(self.deck) == 0:
            return True
        else:
            return False
        
    def isTerminal(self):
        #print(self.deck)
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
            self.winner =  1
        if s1==s2:
            print("Tied.")
            self.winner =  100
        if s1<s2:
            print("Player 2 won.")  
            self.winner =  2 
        
            
        
     
    def initialize (self):
        self.cards.shuffle()
        self.deal_hole()
        self.turn = self.list_of_players(self.first_actor)
    
        
    def finalize (self):    
        self.score_all()       
        self.find_winners()
        self.round_ended = True

    @staticmethod
    def is_instance(is_new=False):
        if (not Game._instance) or is_new:
           Game._instance = Game()
        return Game._instance

class Agent1 ():
    
    def __init__(self):
        self.belief0 =  [[1]*12,[1]*12,[1]*12,[1]*12,[1]*12]
    
    def policy (self, game, opponent_action, opponent_chosen_card):
        
        qvalue = np.zeros( (8,2,6)) # 96 actions
        
        #self.belief0 = self.belief_unopened(game) # 1 for unknown card, 0 for known card, belief/sum(belief)
        if game.recent_action[0] == -1 or game.recent_action2[0] == -1:
            self.belief0 = self.belief_unopened(game)
        
        player = game.list_of_players[game.turn]
        turn = game.turn + 1
        turn = turn%2
        opponent = game.list_of_players[turn]
        player_hands = copy.deepcopy(player.hands)
        player_cards = copy.deepcopy(player.cards)
        opponent_cards = copy.deepcopy(opponent.cards)
        
        if game.recent_action[0] == -1:
            self.belief0 = self.belief_unopened(game)
        else:
            self.belief0 = self.belief_update(game, copy.deepcopy(self.belief0), 100, opponent_action, opponent_chosen_card)
        #self.belief0 = self.belief_unopened(game)
        
        for i in range(8):
            for j in range(2):
                for k in range(6):
                    belief = copy.deepcopy(self.belief0)
                    qvalue[i][j][k] = self.immediate_reward(game, [i+1,j+1,k+1], player_hands, player_cards, opponent_cards, belief )
                    #print("action: ", [i+1,j+1,k+1],"reward: ",  qvalue[i][j][k])
                    
                    
        loc_max = np.argmax(qvalue)
        a1 = loc_max / 12
        a1 = int(a1) 
        a2 = (loc_max % 12) / 6
        a2 = int(a2)
        a3 = (loc_max % 12) % 6
        a3 = int(a3)
        action = [a1+1,a2+1,a3+1]
        return action
    
    def belief_update(self, game, belief, rep_num, opponent_action, opponent_chosen_card):
        
        #print("belief: ", belief )
        belief = copy.deepcopy(belief)
        player = game.list_of_players[game.turn]
        turn = game.turn + 1
        turn = turn%2
        opponent = copy.deepcopy(game.list_of_players[turn])
        player_hands = copy.deepcopy(player.hands)
        player_cards = copy.deepcopy(player.cards)
        game_cards = copy.deepcopy(game.cards)
        opponent_cards = copy.deepcopy(opponent.cards)
        
        if opponent_action[0] > 0:
            if opponent_action[0] == 1 and len(opponent_cards[opponent_chosen_card.color])>0:
                opponent_cards[opponent_chosen_card.color].pop(0)
            elif len(game_cards[opponent_chosen_card.color])>0:
                game_cards[opponent_chosen_card.color].pop(0)
        
        updated_belief = self.belief_unopened2(game, player_hands, player_cards, opponent_cards)
        
        if  opponent_action[0] > 0:
            if opponent_chosen_card.value > 0:
                belief[opponent_chosen_card.color][opponent_chosen_card.value-2] = 0
            else:
                if belief[opponent_chosen_card.color][9] > 0:
                    belief[opponent_chosen_card.color][9] = 0
                elif belief[opponent_chosen_card.color][10] > 0:
                    belief[opponent_chosen_card.color][10] = 0
                else:
                    belief[opponent_chosen_card.color][11] = 0
        
                    
        #print("opponent_chosen_card: ", opponent_chosen_card)
        #print("belief: ",belief)
        prob =  list(chain.from_iterable(belief))
        #rep_num = 1000
        process_list=[]
        for iter  in range(0,rep_num):
            p = threading.Thread(target=self.parallel_computation_sim, args=(opponent_chosen_card,
         game, updated_belief, opponent_cards, player_cards, opponent_action, prob,))
            p.start()
            process_list.append(p)
        #     self.parallel_computation_sim(opponent_chosen_card,
        #  game, updated_belief, opponent_cards, player_cards, opponent_action, prob)    
        for i in range(0, rep_num):
            process_list[i].join()
        
        return updated_belief

    def parallel_computation_sim(self,  opponent_chosen_card,
         game, updated_belief, opponent_cards, player_cards, opponent_action, prob):
        
            opponent_hands_index = []
            opponent_hands = [opponent_chosen_card]
            
            opponent_new_hand = []
            if opponent_action[1] < 6 and opponent_action[1] > 0:
                if len(game.recent_cards[opponent_action[1]-1]) > 0:
                    opponent_new_hand = [game.recent_cards[opponent_action[1]-1][0]]
            
            if opponent_hands[0].value == -1:
                hands_num_sum = 8
                opponent_hands = []
            else:
                hands_num_sum = 7
                
            prob_temp = copy.deepcopy(prob)
            for i in range(0,hands_num_sum):
                unique_hand = False
                while not unique_hand:
                    temp_hand = random.choices(range(0,60), weights = prob_temp, k=1)
                    if temp_hand[0] not in opponent_hands_index:
                        opponent_hands_index.append(temp_hand[0])
                        prob_temp[temp_hand[0]] = 0
                        unique_hand = True
            
            
            for hand in opponent_hands_index:
                value = hand%12
                if value > 8:
                    value = 0
                else:
                    value += 2
                opponent_hands.append(Card( value, hand//12))
            
            #print("opponent_hands: ", opponent_hands)
            
            qvalue2 =  np.zeros( (8,2,6)) # 96 actions
            
            opponent_belief = self.belief_unopened2(game, opponent_hands, opponent_cards, player_cards)
            
            for i in range(8):
                for j in range(2):
                    for k in range(6):
                        op_belief = copy.deepcopy(opponent_belief)
                        #print("belief1:", belief)
                        #print("belief sum1:",  sum([sum(x) for x in belief]) )
                        qvalue2[i][j][k] = self.immediate_reward(game, [i+1,j+1,k+1], opponent_hands, opponent_cards, player_cards, op_belief)
                        #print(i,j,k, "self.belief3: ",self.belief0)
             
            loc_max = np.argmax(qvalue2)
            a1 = loc_max / 12
            a1 = int(a1) 
            a2 = (loc_max % 12) / 6
            a2 = int(a2)
            a3 = (loc_max % 12) % 6
            a3 = int(a3)
            opponent_action_estimate = [a1+1,a2+1,a3+1]
            
            #print("opponent_hands: ", opponent_hands)            
            
            #print(opponent_action_estimate)
            
            if opponent_action_estimate == [1,opponent_action[0],opponent_action[1]]:
                opponent_hands.pop(0)
                if len(opponent_new_hand) == 0:
                    new_hand_index = random.choices(range(0,60), weights = prob_temp, k=1)[0]
                    value = new_hand_index % 12
                    if value > 8:
                        value = 0
                    else:
                        value += 2
                    opponent_hands.append(Card( value, new_hand_index//12))
                else:
                    opponent_hands.append(opponent_new_hand[0])
                
                #print("opponent_hands: ", opponent_hands)    
                for hand in opponent_hands:
                    if hand.value > 0:
                        updated_belief[hand.color][hand.value-2] += 1
                    else:
                        updated_belief[hand.color][9] += 1
            
            #print("updated_belief: ", updated_belief)
                            
                    
    def belief_unopened(self, game):
        
        player = game.list_of_players[game.turn]
        turn = game.turn + 1
        turn = turn%2
        opponent = game.list_of_players[turn]
        hands = player.hands
        belief = [[1]*12,[1]*12,[1]*12,[1]*12,[1]*12] #order: [[red 2~10,wager,wager,wager], []~] ~~~] 
               
        
        for i in range(0,8):
            if hands[i].value == 0:
                if belief[hands[i].color][9] > 0:
                    belief[hands[i].color][9] = 0
                elif belief[hands[i].color][10] > 0:
                    belief[hands[i].color][10] = 0
                else:
                    belief[hands[i].color][11] = 0
            else:
                belief[hands[i].color][ hands[i].value-2 ] = 0
                    
        for i in range(0,5):
            if len(player.cards[i]) > 0:
                for j in range(0,len(player.cards[i])):
                    if player.cards[i][j].value == 0:
                        if belief[ player.cards[i][j].color][9] > 0:
                            belief[ player.cards[i][j].color][9] = 0
                        elif belief[ player.cards[i][j].color][10] > 0:
                            belief[ player.cards[i][j].color][10] = 0
                        else:
                            belief[ player.cards[i][j].color][11] = 0
                    else:
                        belief[player.cards[i][j].color][ player.cards[i][j].value-2 ] = 0
        
        for i in range(0,5):
            if len(game.cards[i]) > 0:
                for j in range(0,len(game.cards[i])):
                    if game.cards[i][j].value == 0:
                        if belief[ game.cards[i][j].color][9] > 0:
                            belief[ game.cards[i][j].color][9] = 0
                        elif belief[ game.cards[i][j].color][10] > 0:
                            belief[ game.cards[i][j].color][10] = 0
                        else:
                            belief[ game.cards[i][j].color][11] = 0
                    else:
                        belief[game.cards[i][j].color][ game.cards[i][j].value-2 ] = 0
        
        for i in range(0,5):
            if len(opponent.cards[i]) > 0:
                for j in range(0,len(opponent.cards[i])):
                    if opponent.cards[i][j].value == 0:
                        if belief[ opponent.cards[i][j].color][9] > 0:
                            belief[ opponent.cards[i][j].color][9] = 0
                        elif belief[ opponent.cards[i][j].color][10] > 0:
                            belief[ opponent.cards[i][j].color][10] = 0
                        else:
                            belief[ opponent.cards[i][j].color][11] = 0
                    else:
                        belief[opponent.cards[i][j].color][ opponent.cards[i][j].value-2 ] = 0
                
        
        return belief
    
    def belief_unopened2(self, game, player_hands, player_cards, opponent_cards):
        
        belief = [[1]*12,[1]*12,[1]*12,[1]*12,[1]*12] #order: [[red 2~10,wager,wager,wager], []~] ~~~] 
               
        
        for i in range(0,8):
            if player_hands[i].value == 0:
                if belief[player_hands[i].color][9] > 0:
                    belief[player_hands[i].color][9] = 0
                elif belief[player_hands[i].color][10] > 0:
                    belief[player_hands[i].color][10] = 0
                else:
                    belief[player_hands[i].color][11] = 0
            else:
                belief[player_hands[i].color][ player_hands[i].value-2 ] = 0
                    
        for i in range(0,5):
            if len(player_cards[i]) > 0:
                for j in range(0,len(player_cards[i])):
                    if player_cards[i][j].value == 0:
                        if belief[ player_cards[i][j].color][9] > 0:
                            belief[ player_cards[i][j].color][9] = 0
                        elif belief[ player_cards[i][j].color][10] > 0:
                            belief[ player_cards[i][j].color][10] = 0
                        else:
                            belief[ player_cards[i][j].color][11] = 0
                    else:
                        belief[player_cards[i][j].color][ player_cards[i][j].value-2 ] = 0
        
        for i in range(0,5):
            if len(game.cards[i]) > 0:
                for j in range(0,len(game.cards[i])):
                    if game.cards[i][j].value == 0:
                        if belief[ game.cards[i][j].color][9] > 0:
                            belief[ game.cards[i][j].color][9] = 0
                        elif belief[ game.cards[i][j].color][10] > 0:
                            belief[ game.cards[i][j].color][10] = 0
                        else:
                            belief[ game.cards[i][j].color][11] = 0
                    else:
                        belief[game.cards[i][j].color][ game.cards[i][j].value-2 ] = 0
        
        for i in range(0,5):
            if len(opponent_cards[i]) > 0:
                for j in range(0,len(opponent_cards[i])):
                    if opponent_cards[i][j].value == 0:
                        if belief[ opponent_cards[i][j].color][9] > 0:
                            belief[ opponent_cards[i][j].color][9] = 0
                        elif belief[ opponent_cards[i][j].color][10] > 0:
                            belief[ opponent_cards[i][j].color][10] = 0
                        else:
                            belief[ opponent_cards[i][j].color][11] = 0
                    else:
                        belief[opponent_cards[i][j].color][ opponent_cards[i][j].value-2 ] = 0
                
        
        return belief
    
    
    
    def immediate_reward (self, game, action, hands, player_cards, opponent_cards, belief):
        
        player_cards = copy.deepcopy(player_cards)
        hands = copy.deepcopy(hands)
        game_cards = copy.deepcopy(game.cards)
        
        belief_sum = sum([sum(x) for x in belief])
        num_nonzero = 0
        for i in range(0,5):
            for j in range(0,12):
                if belief[i][j] > 0:
                    num_nonzero += 1
        
        num_sim = (belief_sum - num_nonzero)/8            
        
        belief2 =  [[1]*12,[1]*12,[1]*12,[1]*12,[1]*12]
        
        for i in range(0,5):
            for j in range(0,12):
                if belief[i][j] == 0:
                    belief2[i][j] = 0
                else:
                    belief2[i][j] = (num_sim + 2) - belief[i][j]
        
        belief_sum2 = sum([sum(x) for x in belief2])
        
        belief =  [ [j/belief_sum * num_nonzero for j in i] for i in belief]  # belief for the opponent's hands
        belief2 =  [ [j/belief_sum2 * num_nonzero for j in i] for i in belief2] # belief for the drawing pile
        
        card_list, count, wager_list, score_list = game.group_cards2(hands) # card_list: card list, count = [#red/#green/#white/#yellow/#blue], wager_list=[#red wager/#green wager/#white wager/#yellow wager/#blue wager]
        val_transfer = np.array([2,3,4,5,6,7,8,9,10,0,0,0]) # function from indices to values, 0,1,2~11 -> 2,3,4,~10,0
        
        #player = game.list_of_players[game.turn] 
        #turn = game.turn + 1
        #turn = turn%2
        
        #opponent = game.list_of_players[turn]
        
        chosen_card = hands[action[0]-1] # the card that the player will play with
        reward = 0 
        
        if action[1] == 1: # register the chosen card
            if len(player_cards[chosen_card.color]) > 0 and chosen_card.value < player_cards[chosen_card.color][0].value:
                #print("player_cards[chosen_card.color]", player_cards[chosen_card.color])                
                reward = -10000
            else:    
                reward = self.reward_eval1(game, chosen_card, hands, player_cards, game_cards, opponent_cards, belief2) # simple evaluation: 
                player_cards[chosen_card.color].insert(0,chosen_card)
        elif action[1] == 2: # discard the chosen card on the discard pile
            reward = - self.reward_eval3(game, chosen_card, hands, player_cards, game_cards, opponent_cards, belief, belief2)
            #print("reward: ", reward)
        #if len(opponent_cards[chosen_card.color]) > 0:
            #    if opponent_cards[chosen_card.color][0].value > chosen_card.value:
            #        reward = - -max(0, self.reward_eval2(game, chosen_card, hands, player_cards, game_cards, opponent_cards, belief2)) # some change needed # evaluation with potential blue 2,3,4,5,6, in hands: 9, 10
            #    else:
            #        num_wager_hands = len(np.where( np.array( opponent_cards[chosen_card.color] ) == 0 )[0])
            #        reward = - max(0, self.reward_eval2(game, chosen_card, hands, player_cards, game_cards, opponent_cards, belief2) ) -  (num_wager_hands + 1) * chosen_card.value ## some change needed 
            #elif chosen_card.value == 0:
            #    reward = 0
            #else:    
            #    reward = - max(0, self.reward_eval2(game, chosen_card, hands, player_cards, game_cards, opponent_cards, belief2)) ## some change needed 
        
        #print("reward action[0]:",action[0]," action[1]: ",action[1]," reward: ",reward)
        
        hands.pop(action[0]-1)
                    
        #print("action1: ", action, ", reward:", reward)  
        if action[2] < 6: # taking a card from the discard pile
            if action[1] == 2 and chosen_card.color == action[2]-1:
                reward = -10000
            elif len(game_cards[action[2]-1]) > 0: # there is at least a card on the discard pile
                picked_card = game.cards[action[2]-1][0]
                hands.insert(0, picked_card)
                reward += self.reward_eval2(game, picked_card, hands, player_cards, game_cards, opponent_cards, belief2)
            else: # no card on the discard pile
                reward = -10000
        elif action[2] == 6: # drawing a card from the draw pile
            belief_sum = sum([sum(x) for x in belief2])
            temp_reward = 0 # expected value of drawing a card from the draw pile
            #print("belief: ", belief)
            #       print("belief_sum: ", belief_sum)
            if belief_sum > 0:
                for i in range(0,5):
                    for j in range(0,12):
                        temp_hands = copy.deepcopy(hands)
                        random_card = Card(val_transfer[j],i)
                        temp_hands.insert(0, random_card)
                        temp_belief = copy.deepcopy(belief2)
                        temp_belief[i][j] = 0
                        temp_reward += belief2[i][j]/belief_sum * self.reward_eval2(game, random_card, temp_hands, player_cards, game_cards, opponent_cards, temp_belief)
                #print("temp_reward: ", temp_reward)            
                reward +=  temp_reward
        
        #print("action2: ", action, ", reward:", reward)    
        return reward
    
    
     
    def reward_eval1 (self, game, card, player_hands, player_cards, game_cards, opponent_cards, belief):
        
        card_list, count, wager_list, score_list = game.group_cards2(player_hands) # card_list: card list, count = [#red/#green/#white/#yellow/#blue], wager_list=[#red wager/#green wager/#white wager/#yellow wager/#blue wager]
        val_transfer = np.array([2,3,4,5,6,7,8,9,10,0,0,0])
        #belief = self.belief_unopened(game)
        
        
        #  remove the card from the unopened cars
        if card.value > 0: 
            belief[card.color][card.value-2] = 0
        elif card.value == 0:
            if belief[card.color][9] > 0:
                belief[card.color][9] = 0
            elif belief[card.color][10] > 0:
                belief[card.color][10] = 0
            else:
                belief[card.color][11] = 0
        
        #player = game.list_of_players[game.turn]
        #turn = game.turn + 1
        #turn = turn%2
        #opponent = game.list_of_players[turn]
        #chosen_card = player.hands[action[0]-1]
        reward = 0
        
        
        exped_values = [x.value for x in player_cards[card.color]] # expedition column
        card2 = []
        for x in card_list:
            if x.color == card.color:
                card2.append(x)
        hands_values = [x.value for x in card2]  # cards in hands with the same color
        hands_values2 = [x.value for x in card2]  # cards in hands with the same color
        cards_losing = np.array([2,3,4,5,6,7,8,9,10,0,0,0])
        num_wager_hands = len(np.where( np.array( hands_values ) == 0 )[0]) # number of wager cards in hands
        num_wager_exped = len(np.where( np.array( exped_values ) == 0 )[0]) # number of wager cards on the expedition column
        
        # If taking the action with value = x, the value cards in hands less than x cannot be realized
        for i in range(0,len(hands_values)):
            if i <= card.value:
                hands_values[i] = 0
        
        # evaluation of potential loss
        for i in range(0,len(hands_values2)):
            if len(player_cards[card.color]) > 0:
                if player_cards[card.color][0].value > hands_values2[i] or card.value <= hands_values2[i]:
                    hands_values2[i] = 0
            else:
                if card.value <= hands_values2[i]:
                    hands_values2[i] = 0
                    
        # If taking the action with value = x, the unopened value cards less than x cannot be realized
        for i in range(0,9):
            if val_transfer[i] < card.value:
                val_transfer[i] = 0
                

        if len(player_cards[card.color]) > 0:
            if card.value < player_cards[card.color][0].value:
                return reward
        
        
        for i in range(0,9):
            cards_losing[i] = cards_losing[i] * belief[card.color][i]
            if len(player_cards[card.color]) > 0:
                if cards_losing[i] >= card.value or cards_losing[i] <= player_cards[card.color][0].value:
                    cards_losing[i] = 0
            else:
                if cards_losing[i] >= card.value:
                    cards_losing[i] = 0
        
        potential_reward = -20 + card.value + sum(exped_values) + sum(hands_values) + 0.30 * sum(np.multiply( belief[card.color] , val_transfer))

        
        topcard_wager = False
        if len(player_cards[card.color]) > 0  and player_cards[card.color][0].value == 0:
            topcard_wager = True
        
        
        if len(player_cards[card.color]) == 0:
            if card.value == 0:
                reward = potential_reward  
            else:
                if potential_reward > 0:
                    if sum(hands_values2) > 0 or num_wager_hands > 0: # if the player has some values that must be registered before the chosen card
                        reward = - 10000
                        #print("step1")
                    else: 
                        reward =  min(potential_reward, card.value) - 0.5 * sum(cards_losing)
                else:
                    reward = -10000
                    #print("step2")
            if len(game.deck) < len(card2):
                reward  = -10000
        elif len(player_cards[card.color]) > 0:
            if card.value == 0:
                reward = potential_reward     
            else: # value> 0
                if topcard_wager == True:
                    if num_wager_hands > 0 or sum(hands_values2) > 0:
                        reward  = -10000
                        #print("step3")
                    else:
                        reward = (1 + num_wager_exped - 0.15*sum(belief[card.color][9:12]) ) * (card.value - 0.5 * sum(cards_losing)) 
                elif topcard_wager == False:
                    if sum(hands_values2) > 0:
                        reward  = -10000
                        #print("step4")
                    else:
                        reward = (1 + num_wager_exped) * ( card.value - 0.5 * sum(cards_losing))
                        
        if card.value> 0  and len(game_cards[card.color]) > 0:
            if len(player_cards[card.color]) > 0:
                if game_cards[card.color][0].value > player_cards[card.color][0].value and game_cards[card.color][0].value  < card.value:
                    reward = -10000
                    #print("step5")
            elif game_cards[card.color][0].value < card.value:
                reward = -10000
                #print("step6")
        
        return reward        

    
    
           
    # reward evaluation when a player get a card 
    def reward_eval2 (self, game, card, player_hands, player_cards, game_cards, opponent_cards, belief):
        
        
        card_list, count, wager_list, score_list= game.group_cards2(player_hands) # card_list: card list, count = [#red/#green/#white/#yellow/#blue], wager_list=[#red wager/#green wager/#white wager/#yellow wager/#blue wager]
        val_transfer = np.array([2,3,4,5,6,7,8,9,10,0,0,0])
        #belief = self.belief_unopened(game)
        
        
        #  remove the card from the unopened cars
        if card.value > 0: 
            belief[card.color][card.value-2] = 0
        elif card.value == 0:
            if belief[card.color][9] > 0:
                belief[card.color][9] = 0
            elif belief[card.color][10] > 0:
                belief[card.color][10] = 0
            else:
                belief[card.color][11] = 0
            
        #print("belief[card.color]: ", belief[card.color])
        #player = game.list_of_players[game.turn]
        #turn = game.turn + 1
        #turn = turn%2
        #opponent = game.list_of_players[turn]
        #chosen_card = player.hands[action[0]-1]
        reward = 0
        
        
        exped_values = [x.value for x in player_cards[card.color]] # expedition column
        card2 = []
        for x in card_list:
            if x.color == card.color:
                card2.append(x)
        hands_values = [x.value for x in card2]  # cards in hands with the same color
        num_wager_hands = len(np.where( np.array( hands_values ) == 0 )[0]) # number of wager cards in hands
        num_wager_exped = len(np.where( np.array( exped_values ) == 0 )[0]) # number of wager cards on the expedition column
        num_wager3 = 0.2 * len(np.where( np.array( belief[card.color][9:12] ) > 0 )[0])

        potential_value = -20 + sum(exped_values) + sum(hands_values) + 0.3 * sum(np.multiply( belief[card.color] , val_transfer) )

        if len(player_cards[card.color]) > 0:
            if card.value > 0: 
                if card.value < player_cards[card.color][0].value:
                    return 0
                elif player_cards[card.color][0].value > 0:
                    reward = num_wager_exped * card.value
                elif player_cards[card.color][0].value == 0:
                    reward = (num_wager_hands + num_wager_exped + num_wager3) * card.value
            elif card.value == 0:
                if card.value < player_cards[card.color][0].value:
                    return 0
                else:
                    reward = (num_wager_hands + num_wager_exped + num_wager3) * min(potential_value, 0)
        else:
            if card.value > 0: 
                reward = (num_wager_hands + num_wager_exped + num_wager3) * card.value
            elif card.value == 0:
                reward = (num_wager_hands + num_wager_exped + num_wager3) * min(potential_value, 0)
            
        return reward
    def reward_eval3 (self, game, card, player_hands, player_cards, game_cards, opponent_cards, belief, belief2):
        
        
        #card_list, count, wager_list, score_list= game.group_cards2(player_hands) # card_list: card list, count = [#red/#green/#white/#yellow/#blue], wager_list=[#red wager/#green wager/#white wager/#yellow wager/#blue wager]
        val_transfer = np.array([2,3,4,5,6,7,8,9,10,0,0,0])
        #belief = self.belief_unopened(game)
        
        
        #  remove the card from the unopened cards
        if card.value > 0: 
            belief[card.color][card.value-2] = 0
        elif card.value == 0:
            if belief[card.color][9] > 0:
                belief[card.color][9] = 0
            elif belief[card.color][10] > 0:
                belief[card.color][10] = 0
            else:
                belief[card.color][11] = 0
        
                    
        #print("belief[card.color]: ", belief[card.color])
        #player = game.list_of_players[game.turn]
        #turn = game.turn + 1
        #turn = turn%2
        #opponent = game.list_of_players[turn]
        #chosen_card = player.hands[action[0]-1]
        reward = 0
        
        
        exped_values = [x.value for x in opponent_cards[card.color]] # expedition column
        belief_sum = sum([sum(x) for x in belief])
        num_wager_hands = sum(belief[card.color][9:13]) / belief_sum * 8
        num_wager_exped = len(np.where( np.array( exped_values ) == 0 )[0]) # number of wager cards on the expedition column
        num_wager3 = 0.2 * len(np.where( np.array( belief2[card.color][9:12] ) > 0 )[0])

        potential_value = -20 + sum(exped_values) + sum(np.multiply( belief[card.color] , val_transfer) ) + 0.3 * sum(np.multiply( belief2[card.color] , val_transfer) )

        if len(opponent_cards[card.color]) > 0:
            if card.value > 0: 
                if card.value < opponent_cards[card.color][0].value:
                    return 0
                elif opponent_cards[card.color][0].value > 0:
                    reward = num_wager_exped * card.value
                elif opponent_cards[card.color][0].value == 0:
                    reward = (num_wager_hands + num_wager_exped + num_wager3) * card.value
            elif card.value == 0:
                if card.value < opponent_cards[card.color][0].value:
                    return 0
                else:
                    reward = (num_wager_hands + num_wager_exped + num_wager3) * min(potential_value, 0)
        else:
            if card.value > 0: 
                reward = (num_wager_hands + num_wager_exped + num_wager3) * card.value
            elif card.value == 0:
                reward = (num_wager_hands + num_wager_exped + num_wager3) * min(potential_value, 0)
            
        return reward
                


                
class Agent2 ():
    def policy (self,game):
        action = [np.random.randint(8,size=1)[0]+1,np.random.randint(2,size=1)[0]+1,6] # random action and get a card from the deck
        return action    

class Agent ():
    def policy (self, game):
        card_list, count, wager_list, score_of_cards=game.group_cards() # card_list: card list, count = [#red/#green/#white/#yellow/#blue], wager_list=[#red wager/#green wager/#white wager/#yellow wager/#blue wager]

        #print(count, card_list, wager_list)

        player = game.list_of_players[game.turn]
        player2 =  game.list_of_players[(game.turn+1)%2]
        
        action_2=6
        for i in range(5):
            player_color_list = player.cards[i]
            card_color_list= game.cards[i]
            if player_color_list and card_color_list and player_color_list[0].value<card_color_list[0].value:
               # print("Pick Up Card", card_color_list[0])
                action_2=i+1
                break
       # print(score_of_cards, "score_of_cards")
        max_score = max(score_of_cards)
        max_score_index = score_of_cards.index(max_score)
        
        max_score_player=0
        palyer_score_list=game.score_interpreter(player)
        min_score_player = min(palyer_score_list)
        min_score_index_player = palyer_score_list.index(min_score_player)
        action=[]
        #print(palyer_score_list, "palyer_score_list")
        max_value=-60
        min_value=10
        discard_card=None
        for j in range(5):
            if card_list[j]:
                chosen_card=card_list[j][0]
                discard_card = card_list[j][0]
                i=chosen_card.color
                value=chosen_card.value
                #print(chosen_card, "loop", chosen_card.color, palyer_score_list, i)
            
                if palyer_score_list[i]!=0:
                    color_list_card = player.cards[i]

                    if len(game.deck)>10:
                        if value>5:
                            continue
                    if len(color_list_card)>=1 and count[i]>=1 and color_list_card[0].value<=value:
                       # print("Adding Cards for score")
                        if palyer_score_list[i]+value> max_value:  
                            action=[chosen_card, 1, action_2]
                            max_value=palyer_score_list[i]+value    
                    elif len(color_list_card)>=1 and count[i]>=1 and color_list_card[0].value>value:
                        action=[chosen_card, 2, action_2]
                        break
                else:
                    if len(game.deck)<=10:
                        if value==0:
                            continue
                    if wager_list[i]!=0 and count[i]-wager_list[i]>=1:
                       # print("Adding wager")
                        action=[chosen_card, 1, action_2]
                        break

        if len(action)==0:
            #print("Main Two")
            action=[discard_card, 2, action_2]
        
        #print(action)
        if action[0].color==action_2-1  and action[1]==2:
            for i in range(5):
                player_color_list = player.cards[i]
                card_color_list= game.cards[i]
                if player_color_list and card_color_list and player_color_list[0].value<card_color_list[0].value and i!=card_color_list[0].color:
                    #print("Pick Up Card", card_color_list[0])
                    action_2=i+1
                    break
            action[2]=action_2
        action[0]=player.hands.index(action[0])+1
        
        return action



class Action():
    def __init__(self, player, x, y, z):
        self.player = player
        self.card = x
        self.action = y
        self.pickup = z

    def __str__(self):
        return str((self.card, self.action, self.pickup))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.card == other.card and self.action == other.action and self.player == other.player and self.pickup == other.pickup

    def __hash__(self):
        return hash((self.card, self.action, self.pickup, self.player))

from mcts import mcts
class Agent_Mcts(object):

    def policy(self, game):
        initialState = game
        searcher = mcts(timeLimit=1000)
        action = searcher.search(initialState=initialState)
        return (action)

            
            



