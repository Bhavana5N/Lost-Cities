from django.shortcuts import render
from .models import  Game, Agent1, Agent2, Agent, Agent_Mcts
import os
import numpy as np
import copy
# Create your views here.


def every_step(game0, a1, a2):
        game0.print_player_info()
        if game0.returnplayer() == "Player 1":
            is_false_answer = True
            a = a1.policy(game0, game0.recent_action[1:3], game0.recent_chosen_card)
            #a = a1.policy(game0)
            print(a)
            is_false_answer = not game0.answer(a)  
            
        else:
            is_false_answer = True
            a = a2.policy(game0)
            print(a)
            is_false_answer = not game0.answer(a)   

        
        if game0.end_game():
            isEnd = True  

def game(request):
    isEnd = False
    a1 = Agent1()
    a2 = Agent_Mcts()
    print(request.method, request)
    game0 = Game.is_instance()


    if "Refresh" in request.GET:
        game0 = Game.is_instance(True)

    elif "Next" in request.GET:

    #while isEnd == False:
        if len(game0.deck) > 0:
            every_step(game0, a1, a2)
        else:
            game0.find_winners()
            player = game0.player1
            player2 =  game0.player2
            turn = game0.returnplayer()
            scores_list = [{"Player": "Player1", "Score": sum(game0.score_interpreter(player))},{"Player": "Player2", "Score": sum(game0.score_interpreter(player2))}]
            discard_cards = [{'color': game0.colors[i], 'values': game0.cards[i][-1] }  if len(game0.cards[i]) >0 else  {'color': game0.colors[i], 'values': game0.cards[i]}  for i in range(5)]

            return render(request, "game.html", {'player1_c': player.cards, 'discard_cards': discard_cards,
    "player2_c": player2.cards, "player2_h": player2.hands,  "player1_h": player.hands, 
    "scores_list": scores_list, "deck_count": len(game0.deck), "turn": turn, "message": "Game is Completed"})
    elif "Playall" in request.GET:

        while len(game0.deck)>0:
            every_step(game0, a1, a2)
    game0.find_winners()
    player = game0.player1
    player2 =  game0.player2
    turn = game0.returnplayer()
    scores_list = [{"Player": "Player1", "Score": sum(game0.score_interpreter(player))},{"Player": "Player2", "Score": sum(game0.score_interpreter(player2))}]
    discard_cards = [{'color': game0.colors[i], 'values': game0.cards[i][-1] }  if len(game0.cards[i]) >0 else  {'color': game0.colors[i], 'values': game0.cards[i]}  for i in range(5)]
     
    return render(request, "game.html", {'player1_c': player.cards, 'discard_cards': discard_cards,
    "player2_c": player2.cards, "player2_h": player2.hands,  "player1_h": player.hands, 
    "scores_list": scores_list, "deck_count": len(game0.deck), "turn": turn})