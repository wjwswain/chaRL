#https://dev.to/nexttech/build-a-blackjack-command-line-game-3o4b
#https://stable-baselines.readthedocs.io/en/master/guide/custom_env.html

import numpy as np
import random
import gym
from gym import spaces

class GameEnv(gym.Env):
	metadata = {'render.modes': ['console']}

	def __init__(self, bankroll, name):
		super(GameEnv, self).__init__()

		self.bet = 0
		self.rounds = 1
		self.max_rounds = bankroll//5 + 1
		self.reset_bankroll = bankroll
		self.bankroll = bankroll
		self.name = name

		self.deck = Deck()
		self.deck.shuffle()
		self.hand = Hand()
		self.dealer = Hand()

		self.observation = np.zeros(157, dtype=np.int8)#[stage(0), deck left(1-52), player's hand(53-104), dealer's hand(105-156)]
		self.observation[1:53] = 1
		self.reward = 0
		self.done = False
		self.info = {}

		self.action_space = spaces.MultiDiscrete([100,2])# [$5-$500 bid, hit(0)/stay(1)]
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
			self.bet = min(5*(action[0]+1), self.bankroll)
			self.bankroll -= self.bet

			self.hand = Hand()
			for hand_i in range(2):
				idx = self.hand.add_card(self.deck.deal())
				self.observation[1+idx] = 0
				self.observation[53+idx] = 1

			self.dealer = Hand()
			idx = self.dealer.add_card(self.deck.deal())
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

			if self.hand.value[-1] > 21:
				self.reward = -self.bet
				self.observation[0] = 0
				self.observation[53:] = 0
				if self.rounds == self.max_rounds or int(self.bankroll) < 5:
					self.done = True
			else:
				self.reward = 0

		else:
			while self.dealer.value[0] < 17:
				if self.deck.len() == 0:
					self.reshuffle()
				idx = self.dealer.add_card(self.deck.deal())

			for hand in [self.hand, self.dealer]:
				if len(hand.value) > 1:
					adj_hand_vals = [21-val for val in hand.value if val < 22]
					if len(adj_hand_vals) == 0:
						hand.best_val = hand.value[0]
					else:
						hand.best_val = 21 - min(adj_hand_vals)
				else:
					hand.best_val = hand.value[0]
			if self.hand.best_val == self.dealer.best_val:
				self.reward = 0
				self.bankroll += self.bet
			elif self.hand.best_val > self.dealer.best_val or self.dealer.best_val > 21:
				self.reward = 10*self.bet
				self.bankroll += 1.5*self.bet
			else:
				self.reward = -self.bet

			self.observation[0] = 0
			self.observation[53:] = 0

			if self.rounds == self.max_rounds or int(self.bankroll) < 5:
				self.done = True
		return self.observation, self.reward, self.done, self.info

	def reset(self):
		self.deck = Deck()
		self.deck.shuffle()

		self.bankroll = self.reset_bankroll
		self.rounds = 1
		self.done = False

		self.observation = np.zeros(157, dtype=np.int8)
		self.observation[1:53] = 1

		return self.observation

	def render(self, mode="console"):
		if mode != "console":
			raise NotImplementedError()
		else:
			if self.observation[0] == 0:
				if self.rounds > 1:
					print("Round Reward:", self.reward)
					print()
				print(self.name + ': ' + str(self.bankroll))
			else:
				print(self.name, "bet", str(self.bet) + ':')
				if len(self.hand.cards) > 0:
					self.hand.display()
					print()
					print("Dealer:")
					print("??")
					self.dealer.display()
					print()

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
	def __init__(self):
		self.cards = []
		self.value = [0]
		self.best_val = 0

	def display(self):
		for card in self.cards:
			print(card)

	def add_card(self, card):
		if card.isAce():
			self.value.append(self.value[-1]-10)
		self.cards.append(card)
		for i in range(len(self.value)):
			self.value[i] += card.get_value()
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
