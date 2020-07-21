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
		self.deck.shuffle()
		self.hand = Hand(self.name)
		self.dealer = Hand("Dealer")

		self.observation = np.zeros(157, dtype=np.int8)#[stage(0), deck left(1-52), player's hand(53-104), dealer's hand(105-156)]
		self.observation[1:53] = 1
		self.reward = 0
		self.done = False
		self.info = {}

		self.action_space = spaces.MultiDiscrete([100,1])# [$5-$500 bid, hit(0)/stay(1)]
		self.observation_space = spaces.MultiBinary(157)# I hate the limitations of stable-baselines

	def reshuffle(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.observation[1:53] = 1 #deck left

	def step(self, action):
		if self.observation[0] == 0: #stage
			if self.deck.len() < 3:
				self.reshuffle()

			self.rounds += 1
			self.bet = max(5*(action[0]+1), self.bankroll)
			self.bankroll -= self.bet

			self.hand = Hand(self.name)
			for hand_i in range(2):
				idx = self.hand.add_card(self.deck.deal())
				self.observation[1+idx] = 0
				self.observation[53+idx] = 1

			self.dealer = Hand("Dealer")
			idx = self.hand.add_card(self.deck.deal())
			self.observation[1+idx] = 0
			self.observation[105+idx] = 1

			self.observation[0] = 1
			self.reward = 0

		elif action[1] == 0:
			if self.deck.len() == 0:
				self.reshuffle()
			idx = self.hand.add_card(self.deck.deal())
			self.observation[1+idx] = 0
			self.observation[53+idx] = 1

			if self.hand.value > 22 and self.hand.aces == 0:
				self.reward = -self.bet
				self.observation[0] = 0
				self.observation[53:] = 0
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

			self.observation[0] = 0
			self.observation[53:] = 0

			if self.rounds == 500 or self.bankroll == 0:
				self.done = True
		return self.observation, self.reward, self.done, self.info

	def reset(self):
		self.deck = Deck()
		self.deck.shuffle()

		self.observation = np.zeros(157, dtype=np.int8)
		self.observation[1:53] = 1

		return self.observation

	def render(self, mode="console"):
		if mode != "console":
			raise NotImplementedError()
		else:
			if self.observation[0] == 0:
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
		if self.name == "Dealer":
			print("?? ")
		for card in self.cards:
			print(card)

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
