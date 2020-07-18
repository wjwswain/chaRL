import Card

class Hand:
	def __init__(self, name, bankroll):
		self.name = name
		self.cards = []
		self.value = 0

	def hit(self, card):
		self.cards.append(card)

	def get_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            elif card.value == 'A':
                has_ace = True
                self.value += 11
            else:
                self.value += 10
        return self.value

    def display(self):
    	print(self.name)
    	card_list = self.cards
    	if self.name == "Dealer":
    		card_list[0] == "??"
    	for card in card_list:
    		print(card)
    	print("Value:", self.value)