import Card

class Hand:
	def __init__(self, name):
		self.name = name
		self.cards = []
		self.value = 0

	def hit(self, card):
		self.cards.append(card)

    def display(self):
    	print(self.name)
    	card_list = self.cards
    	if self.name == "Dealer":
    		print("??")
    	for card in card_list:
    		print(card)
    	print("Value:", self.value)