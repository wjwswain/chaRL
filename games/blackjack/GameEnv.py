#https://dev.to/nexttech/build-a-blackjack-command-line-game-3o4b
#https://stable-baselines.readthedocs.io/en/master/guide/custom_env.html

import Deck
import Hand
import gym
from gym import spaces

class GameEnv(gym.Env):
	metadata = {'render.modes': ['console']}

    def __init__(self):
        super(Game, self).__init__()

        self.bet = 0
        self.rounds = 1
        self.bankroll = 5000
        self.name = "Example"
        
        self.deck = Deck()
        self.hand = Hand(self.name)
        self.dealer = Hand("Dealer")

        self.observation = {}
        self.reward = -1
        self.done = False
        self.info = {}

        self.action_space = spaces.Dict({#... will ignore irrelevant moves
        	"bet":spaces.Discrete(100), #5(bet+1) = true bet (5-500) 
        	"hit_or_stand":spaces.Discrete(2) #hit=0, stand=1
        })
        self.observation_space = spaces.Dict({
        	"stage":spaces.Discrete(2),#0=bet, 1=hit_or_stand
        	"cards_left":spaces.MultiBinary(52),#deck binary array
        	"hand_contents":spaces.MultiBinary(52),#hand binary array
        	"hand_value":spaces.Discrete(21),#0, 2-21
        	"dealer_contents":spaces.MultiBinary(52),#hand binary array
        	"dealer_value":spaces.Discrete(11)#0, 2-11
        })

    def step(self, action):
    	if self.observation["stage"] == 0:
    		self.rounds += 1
    		self.bet = max(5*(action["bet"]+1), self.bankroll)
    		self.bankroll -= self.bet
    		self.reward = -1

    		
    		self.hand = Hand(self.name)
    		self.dealer = Hand("Dealer")

    		first_card = self.deck.deal()
    		second_card = self.deck.deal()
    		dealer_card = self.deck.deal()



    	elif action["hit_or_stand"] == 0:
    		pass
    	else:
	    	if self.rounds == 500 or self.bankroll == 0:
	    		self.done = True
	    return self.observation, self.reward, self.done, self.info

	def reset(self):
		self.deck = Deck()
		self.deck.shuffle()

		self.observation = {
		"stage":0,
		"cards_left":np.ones(shape=52, dtype=np.int8),
		"hand_contents":np.zeros(shape=52, dtype=np.int8),
		"hand_value":0,
		"dealer_contents":np.zeros(shape=52, dtype=np.int8),
		"dealer_value":0
		}

	    return self.observation

	def render(self, mode="console"):
		if mode != "console":
			raise NotImplementedError()
		else:
			if self.stage == 0:
				if self.rounds != 0:
					print(self.name, "bets", str(self.bet))
				else:
					print("Game Initializing...")
					print()
			else:
				print(self.name + ': ' + str(self.bankroll))
				print(self.hand.display())
				print()
				print("Dealer:", self.dealer.display())


	def close (self):
		pass

    def play(self):

	    def check_for_blackjack(self):
        	b_checks = [False for hand in range(count+1)]
        	for i, hand in enumerate(self.hands):
        		if hand.get_value() == 21:
        			b_checks[i] = True
	        return b_checks

        while True:

	        self.hands = []
	        for pnum in range(count):
	        	self.hands.append(Hand('P'+str(pnum), bankroll))
	        self.hands.append(Hand("Dealer", bankroll))

        	for hand in self.hands:
        		for i in range(2):
	                hand.hit(self.deck.deal())
	            hand.display()

	        game_over = False
            while not game_over:
                b_checks = self.check_for_blackjack()

