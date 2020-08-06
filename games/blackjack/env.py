#https://dev.to/nexttech/build-a-blackjack-command-line-game-3o4b
#https://stable-baselines.readthedocs.io/en/master/guide/custom_env.html

import numpy as np
import random
import gym
from gym import spaces

class Blackjack(gym.Env):
	metadata = {'render.modes': ['console']}

	def __init__(self, bankroll, name):
		super(Blackjack, self).__init__()

		self.bet = 0
		self.rounds = 0
		self.max_rounds = bankroll//5
		self.reset_bankroll = bankroll
		self.bankroll = bankroll
		self.name = name

		self.deck = Deck()
		self.deck.shuffle()
		self.hand = Hand()
		self.dealer = Hand()

		self.observation = np.zeros(157, dtype=np.int8)#[stage(0), deck(1-52), player's hand(53-104), dealer's hand(105-156)]
		self.reward = 0
		self.done = False
		self.info = {}

		self.action_space = spaces.MultiDiscrete([100,2])# [$5-$500 bid, hit(0)/stay(1)]
		self.observation_space = spaces.MultiBinary(157)# I hate the limitations of stable-baselines

	def reshuffle(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.observation[1:53] = 0 #deck empty

	def hit(self, hand, count, hand_start):
		if self.deck.len() < count:
			self.reshuffle()
		for i in range(count):
			idx = hand.add_card(self.deck.deal())
			self.observation[1+idx] = 1
			self.observation[hand_start+idx] = 1
		return hand

	def stand(self):
		pass

	def end_hand(self, reward):
		self.reward = reward
		self.bankroll += reward
		self.observation[0] = 0
		self.observation[53:] = 0
		if self.rounds == self.max_rounds:
			# print("Reached Maximum Rounds (" + str(self.max_rounds) + ')')
			self.done = True
		elif int(self.bankroll) < 5:
			# print("Okay champ, try again tomorrow.")
			self.done = True

	def step(self, action):
		if self.observation[0] == 0:
			self.bet = min(5*(action[0]+1), self.bankroll)
			self.hand = self.hit(Hand(), 2, 53)
			self.dealer = self.hit(Hand(), 1, 105)

			self.rounds += 1
			self.observation[0] = 1
			self.reward = 0

		elif action[1] == 0:
			self.hand = self.hit(self.hand, 1, 53)
			if self.hand.best_value > 21:
				self.end_hand(-self.bet)
			else:
				self.reward = 0

		else:
			while self.dealer.dealer_value < 17:
				self.dealer = self.hit(self.dealer, 1, 105)

			if self.dealer.dealer_value > 21 or self.hand.best_value > self.dealer.dealer_value:
				self.end_hand(1.5*self.bet)
			elif self.hand.best_value == self.dealer.dealer_value:
				self.end_hand(0)
			else:
				self.end_hand(-self.bet)

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
			if self.observation[0] == 1:
				print(self.name + "'s Bankroll: $", str(self.bankroll))
				print(self.name + "'s Bet: $" + str(self.bet))
				print()
			else:
				print(self.name + "'s Hand:")
				self.hand.display()
				print("Dealer's Hand:")
				self.dealer.display()
				print("Hand Reward:", str(self.reward))
				print("--------------------")

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
		self.values = [0]
		self.best_value = 0
		self.dealer_value = 0

	def display(self):
		for card in self.cards:
			print(card)
		print()

	def add_card(self, card):
		if card.isAce():
			self.values.append(self.values[-1]-10)
		self.cards.append(card)
		for i in range(len(self.values)):
			self.values[i] += card.get_value()
		self.best_value = self.get_best_value()
		self.dealer_value = self.get_dealer_value()
		return card.get_index()

	def get_best_value(self):
		possibles = [21 - value for value in self.values if value <= 21]
		if len(possibles) == 0:
			return self.values[-1]
		else:
			return 21 - min(possibles)

	def get_dealer_value(self):
		possibles = [value for value in self.values if value <= 21]
		if len(possibles) == 0:
			return self.values[-1]
		else:
			for value in self.values:
				if value > 17:
					return value
			return possibles[0]

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
