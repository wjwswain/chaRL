#https://dev.to/nexttech/build-a-blackjack-command-line-game-3o4b
#https://stable-baselines.readthedocs.io/en/master/guide/custom_env.html

import numpy as np
import random
import gym
from gym import spaces

class GameEnv(gym.Env):
	metadata = {'render.modes': ['console']}

	def __init__(self):
		super(GameEnv, self).__init__()

		self.bet = 0
		self.rounds = 1
		self.bankroll = 5000
		self.name = "Example"
		
		self.deck = Deck()
		self.hand = Hand(self.name)
		self.dealer = Hand("Dealer")

		self.observation = {}
		self.reward = 0
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

	def reshuffle(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.observation["cards_left"] = np.ones(shape=52, dtype=np.int8)

	def step(self, action):
		if self.observation["stage"] == 0:
			if self.deck.len() < 3:
				self.reshuffle()

			self.rounds += 1
			self.bet = max(5*(action["bet"]+1), self.bankroll)
			self.bankroll -= self.bet

			self.hand = Hand(self.name)
			for hand_i in range(2):
				idx = self.hand.add_card(self.deck.deal())
				self.observation["cards_left"][idx] = 0
				self.observation["hand_contents"][idx] = 1
			self.observation["hand_value"] = self.hand.value

			self.dealer = Hand("Dealer")
			idx = self.hand.add_card(self.deck.deal())
			self.observation["cards_left"][idx] = 0
			self.observation["dealer_contents"][idx] = 1
			self.observation["dealer_value"] = self.dealer.value

			self.observation["stage"] = 1
			self.reward = 0

		elif action["hit_or_stand"] == 0:
			if self.deck.len() == 0:
				self.reshuffle()
			idx = self.hand.add_card(self.deck.deal())
			self.observation["cards_left"][idx] = 0
			self.observation["hand_contents"][idx] = 1
			self.observation["hand_value"] = self.hand.value

			if self.hand.value > 22 and self.hand.aces == 0:
				self.reward = -self.bet
				self.observation = {
					"stage":0,
					"cards_left":self.observation["cards_left"],
					"hand_contents":np.zeros(shape=52, dtype=np.int8),
					"hand_value":0,
					"dealer_contents":np.zeros(shape=52, dtype=np.int8),
					"dealer_value":0
				}
			else:
				self.reward = 0

		else:
			while self.dealer.value < 17:
				if self.deck.len() == 0:
					self.reshuffle()
				idx = self.dealer.add_card(self.deck.deal())

			for hand in [self.hand, self.dealer]:
				if hand.value > 21 and hand.aces != 0:
					for ace in range(1, hand.aces+1):
						pot_value = hand.value - (ace*10)
						if pot_value < 22:
							hand.value = pot_value

			if self.hand.value == self.dealer.value and self.hand.value < 22:
				self.reward = self.bet
				self.bankroll += self.reward
			elif self.hand.value > self.dealer.value and self.hand.value < 22:
				self.reward = 1.5*self.bet
				self.bankroll += self.reward
			else:
				self.reward = -self.bet

			self.observation = {
				"stage":0,
				"cards_left":self.observation["cards_left"],
				"hand_contents":np.zeros(shape=52, dtype=np.int8),
				"hand_value":0,
				"dealer_contents":np.zeros(shape=52, dtype=np.int8),
				"dealer_value":0
			}

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


class Deck:
	def __init__(self):
		values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
		suits = ['C', 'H', 'S', 'D']
		self.cards = [Card(v,s) for v in values for s in suits]

	def shuffle(self):
		random.shuffle(self.cards)

	def deal(self):
		return self.cards.pop(0)

	def len(self):
		return len(self.cards)


class Hand:
	def __init__(self, name):
		self.name = name
		self.cards = []
		self.value = 0
		self.aces = 0

	def display(self):
		print(self.name)
		card_str = " "
		if self.name == "Dealer":
			card_str += print("?? ")
		for card in self.cards:
			card_str += card + ' '
		print(card_str)

	def add_card(self, card):
		if card.isAce():
			self.aces += 1
		self.cards.append(card)
		self.value += card.get_value()
		return card.get_index()


class Card:
	def __init__(self, value, suit):
		self.value = value
		self.suit = suit

	def __repr__(self):
		return self.value + self.suit

	def get_value(self):
		if self.value.isnumeric():
			return int(self.value)
		elif self.isAce():
			return 11
		else:
			return 10

	def get_index(self):
		suits = {'C':0, 'H':1, 'S':2, 'D':3}
		faces = {'A':0, 'J':10, 'Q':11, 'K':12}
		suit_index = suits[self.suit]
		if self.value.isnumeric():
			value_index = int(self.value)
		else:
			value_index = faces[self.value]
		return (4 * value_index) + suit_index

	def isAce(self):
		return self.value == 'A'
