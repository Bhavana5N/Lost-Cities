from models import  Game, Agent1, Agent2, Agent, Agent_Mcts

def every_step(game0, a1, a2):
        #game0.print_player_info()
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
dual_list=[]
mcts_list=[]
random_list=[]
greedy_list=[]
winners_list=[]
for i in range(100):
    try:
        isEnd = False
        a1 = Agent1()
        a2 = Agent2()
        game0 = Game()
        while len(game0.deck)>0:
                every_step(game0, a1, a2)
        game0.find_winners()
        print(game0.winner, "rrrr")
        winners_list.append(game0.winner)
    except:
        winners_list.append(0)

import matplotlib.pyplot as plt
plt.plot(list(range(100)), winners_list)
plt.show()



