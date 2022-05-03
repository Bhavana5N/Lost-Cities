from django.shortcuts import render
from .models import StandardDeck, Game, Card
import os
import numpy as np
import copy
# Create your views here.


class Agent1 ():
    
    def __init__(self):
        self.belief0 =  [[1]*12,[1]*12,[1]*12,[1]*12,[1]*12]
    
    def policy (self, game):
        
        qvalue = np.zeros( (8,2,6)) # 96 actions
        
        self.belief0 = self.belief_unopened(game) # 1 for unknown card, 0 for known card, belief/sum(belief)
        
        for i in range(8):
            for j in range(2):
                for k in range(6):
                    belief = copy.deepcopy(self.belief0)
                    #print("belief1:", belief)
                    #print("belief sum1:",  sum([sum(x) for x in belief]) )
                    qvalue[i][j][k] = self.immediate_reward(game,[i+1,j+1,k+1], belief)
                    #print(i,j,k, "self.belief3: ",self.belief0)
        
                    
        loc_max = np.argmax(qvalue)
        a1 = loc_max / 12
        a1 = int(a1) 
        a2 = (loc_max % 12) / 6
        a2 = int(a2)
        a3 = (loc_max % 12) % 6
        a3 = int(a3)
        action = [a1+1,a2+1,a3+1]
        return action
    
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
    
    def immediate_reward(self, game, action, belief):
        
        card_list, count, wager_list, score_list = game.group_cards() # card_list: card list, count = [#red/#green/#white/#yellow/#blue], wager_list=[#red wager/#green wager/#white wager/#yellow wager/#blue wager]
        val_transfer = np.array([2,3,4,5,6,7,8,9,10,0,0,0]) # function from indices to values, 0,1,2~11 -> 2,3,4,~10,0
        player = game.list_of_players[game.turn] 
        turn = game.turn + 1
        turn = turn%2
        opponent = game.list_of_players[turn]
        chosen_card = player.hands[action[0]-1] # the card that the player will play with
        reward = 0 
        
        
        if action[1] == 1: # register the chosen card
            if len(player.cards[chosen_card.color]) > 0: # some cards are registered already
                if chosen_card.value < player.cards[chosen_card.color][0].value:
                    reward = -10000
                else:    
                    reward = self.reward_eval1(game, chosen_card, belief) # simple evaluation: 
            else: # no card registerd
                reward = self.reward_eval1(game, chosen_card, belief)
        elif action[1] == 2: # discard the chosen card on the discard pile
            if len(opponent.cards[chosen_card.color]) > 0:
                if opponent.cards[chosen_card.color][0].value > chosen_card.value:
                    reward = - -max(0, self.reward_eval2(game, chosen_card, belief)) # some change needed # evaluation with potential blue 2,3,4,5,6, in hands: 9, 10
                else:
                    num_wager_hands = len(np.where( np.array( opponent.cards[chosen_card.color] ) == 0 )[0])
                    reward = - max(0, self.reward_eval2(game, chosen_card, belief) ) -  (num_wager_hands + 1) * chosen_card.value ## some change needed 
            else:
                reward = - max(0, self.reward_eval2(game, chosen_card, belief)) ## some change needed 
            #print("reward action[0]:",action[0]," action[1]: ",action[1]," reward: ",reward)
        
        
                    
        #print("action1: ", action, ", reward:", reward)  
        if action[2] < 6: # taking a card from the discard pile
            if action[1] == 2 and chosen_card.color == action[2]-1:
                reward = -10000
            elif len(game.cards[action[2]-1]) > 0: # there is at least a card on the discard pile
                picked_card = game.cards[action[2]-1][0]            
                reward += self.reward_eval2(game, picked_card, belief)
            else: # no card on the discard pile
                reward = -10000
        elif action[2] == 6: # drawing a card from the draw pile
            belief_sum = sum([sum(x) for x in belief])
            temp_reward = 0 # expected value of drawing a card from the draw pile
            #print("belief: ", belief)
            #       print("belief_sum: ", belief_sum)
            if belief_sum > 0:
                for i in range(0,5):
                    for j in range(0,12):
                        random_card = Card(val_transfer[j],i) 
                        temp_reward += belief[i][j]/belief_sum * self.reward_eval2(game, random_card, belief)
                #print("temp_reward: ", temp_reward)            
                reward +=  temp_reward
        
        #print("action2: ", action, ", reward:", reward)    
        return reward
    
    # reward evaluation when a player registers a card on the corresponding expedition column
    def reward_eval1 (self, game, card, belief):
        
        
        card_list, count, wager_list, score_list = game.group_cards() # card_list: card list, count = [#red/#green/#white/#yellow/#blue], wager_list=[#red wager/#green wager/#white wager/#yellow wager/#blue wager]
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
        
        player = game.list_of_players[game.turn]
        #turn = game.turn + 1
        #turn = turn%2
        #opponent = game.list_of_players[turn]
        #chosen_card = player.hands[action[0]-1]
        reward = 0
        
        
        exped_values = [x.value for x in player.cards[card.color]] # expedition column
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
        
        # eval for losing
        for i in range(0,len(hands_values2)):
            if len(player.cards[card.color]) > 0:
                if player.cards[card.color][0].value > hands_values2[i] or card.value <= hands_values2[i]:
                    hands_values2[i] = 0
            else:
                if card.value <= hands_values2[i]:
                    hands_values2[i] = 0
                    
        # If taking the action with value = x, the unopened value cards less than x cannot be realized
        for i in range(0,9):
            if val_transfer[i] < card.value:
                val_transfer[i] = 0
                

        if len(player.cards[card.color]) > 0:
            if card.value < player.cards[card.color][0].value:
                return reward
        
        
        for i in range(0,9):
            cards_losing[i] = cards_losing[i] * belief[card.color][i]
            if len(player.cards[card.color]) > 0:
                if cards_losing[i] >= card.value or cards_losing[i] <= player.cards[card.color][0].value:
                    cards_losing[i] = 0
            else:
                if cards_losing[i] >= card.value:
                    cards_losing[i] = 0
        
        potential_reward = -20 + sum(exped_values) + sum(hands_values) + 0.35 * sum(np.multiply( belief[card.color] , val_transfer))
        
                
        
        topcard_wager = False
        if len(player.cards[card.color]) > 0  and player.cards[card.color][0].value == 0:
            topcard_wager = True
        
        if len(player.cards[card.color]) == 0 and card.value > 0:
            if potential_reward > 0:
                if sum(hands_values2) > 0:
                    reward = - 10000
                else: 
                    reward =  card.value - 0.3 * sum(cards_losing)
            else:
                reward = -10000
        elif card.value == 0:
            reward = potential_reward
        elif card.value > 0 and topcard_wager == True:
            if num_wager_hands > 0 :
                reward  = -10000
            else:
                #reward = (1 + num_wager_exped) * (card.value - sum(hands_values2) - 0.2 * sum(np.multiply( belief[card.color][(player.cards[card.color][0].value):(card.value-1)] , val_transfer[(player.cards[card.color][0].value):(card.value-1)] ) ) 
                reward = (1 + num_wager_exped - 0.15*sum(belief[card.color][9:12]) ) * (card.value - sum(hands_values2) - 0.3 * sum(cards_losing)) 
                
        elif card.value > 0 and topcard_wager == False:
            if sum(hands_values2) > 0:
                reward = - 10000
            else:    
                reward = (1 + num_wager_exped) * ( card.value - 0.3 * sum(cards_losing))   
        
        #print("val_transfer: ", val_transfer)
        #print("sum(hands_values2): ", sum(hands_values2),"sum(cards_losing): ", sum(cards_losing),  "asd: ", sum(np.multiply( belief[card.color] , val_transfer)))
            
        return reward
    
    # reward evaluation when a player get a card 
    def reward_eval2 (self, game, card, belief):
        
        belief = belief.copy()
        
        card_list, count, wager_list, score_list= game.group_cards() # card_list: card list, count = [#red/#green/#white/#yellow/#blue], wager_list=[#red wager/#green wager/#white wager/#yellow wager/#blue wager]
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
        player = game.list_of_players[game.turn]
        #turn = game.turn + 1
        #turn = turn%2
        #opponent = game.list_of_players[turn]
        #chosen_card = player.hands[action[0]-1]
        reward = 0
        
        
        exped_values = [x.value for x in player.cards[card.color]] # expedition column
        card2 = []
        for x in card_list:
            if x.color == card.color:
                card2.append(x)
        hands_values = [x.value for x in card2]  # cards in hands with the same color
        num_wager_hands = len(np.where( np.array( hands_values ) == 0 )[0]) # number of wager cards in hands
        num_wager_exped = len(np.where( np.array( exped_values ) == 0 )[0]) # number of wager cards on the expedition column
        num_wager3 = 0.2 * sum(belief[card.color][9:12])

        potential_value = -20 + sum(exped_values) + sum(hands_values) + 0.4 * sum(np.multiply( belief[card.color] , val_transfer) )

        if len(player.cards[card.color]) > 0:
            if card.value > 0: 
                if card.value < player.cards[card.color][0].value:
                    return 0
                elif player.cards[card.color][0].value > 0:
                    reward = num_wager_exped * card.value
                elif player.cards[card.color][0].value == 0:
                    reward = (num_wager_hands + num_wager_exped + num_wager3) * card.value
            elif card.value == 0:
                if card.value < player.cards[card.color][0].value:
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
        

def game(request):
    isEnd = False
    a1 = Agent1()
    a2 = Agent2()
    print(request.method, request)
    game0 = Game.is_instance()


    if "Refresh" in request.GET:
        game0 = Game.is_instance(True)

    elif "Next" in request.GET:

    #while isEnd == False:
        if len(game0.deck) > 0:
           
            if game0.returnplayer() == "Player 1":
                is_false_answer = True
                a = a1.policy(game0)
                print(a)
                is_false_answer = not game0.answer(a)  
                
            else:
                is_false_answer = True
                a = a2.policy(game0)
                print(a)
                is_false_answer = not game0.answer(a)   

            
            if game0.end_game():
                isEnd = True
        else:
            return render(request, "game.html", {'player1_c': player.cards, 'discard_cards': discard_cards,
    "player2_c": player2.cards, "player2_h": player2.hands,  "player1_h": player.hands, 
    "scores_list": scores_list, "deck_count": len(game0.deck), "turn": turn, "message": "Game is Completed"})
    elif "Playall" in request.GET:

        while len(game0.deck)>0:
            
            if game0.returnplayer() == "Player 1":
                is_false_answer = True
                a = a1.policy(game0)
                print(a)
                is_false_answer = not game0.answer(a)  
                
            else:
                is_false_answer = True
                a = a2.policy(game0)
                print(a)
                is_false_answer = not game0.answer(a)   

            
            if game0.end_game():
                isEnd = True
    game0.find_winners()
    player = game0.player1
    player2 =  game0.player2
    turn = game0.returnplayer()
    scores_list = [{"Player": "Player1", "Score": sum(game0.score_interpreter(player))},{"Player": "Player2", "Score": sum(game0.score_interpreter(player2))}]
    discard_cards = [{'color': game0.colors[i], 'values': game0.cards[i][-1] }  if len(game0.cards[i]) >0 else  {'color': game0.colors[i], 'values': game0.cards[i]}  for i in range(5)]
    return render(request, "game.html", {'player1_c': player.cards, 'discard_cards': discard_cards,
    "player2_c": player2.cards, "player2_h": player2.hands,  "player1_h": player.hands, 
    "scores_list": scores_list, "deck_count": len(game0.deck), "turn": turn})