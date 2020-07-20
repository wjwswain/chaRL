class Card:
	def __init__(self, value, suit):
		self.value = value
		self.suit = suit
		suits = {'C':0, 'H':1, 'S':2, 'D':3}
		faces = {'A':0, 'J':10, 'Q':11, 'K':12}

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
    	suit_index = suits[self.suit]
    	if self.value.isnumeric():
            value_index = int(self.value)
        else:
        	value_index = faces[self.value]
        return (4 * value_index) + suit_index

    def isAce(self):
    	return self.value == 'A'
