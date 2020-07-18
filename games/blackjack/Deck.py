import random
import Card

class Deck:
	def __init__(self):
		values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
		suits = ['C', 'H', 'S', 'D']
		self.cards = [Card(v,s) for s in suits for v in values]

	def shuffle(self):
		random.shuffle(self.cards)

	def deal(self):
		return self.cards.pop(0)
