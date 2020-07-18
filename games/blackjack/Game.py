#https://dev.to/nexttech/build-a-blackjack-command-line-game-3o4b
import Deck
import Hand


class Game:
    def __init__(self):
        pass

    def play(self):

	    def check_for_blackjack(self):
        	b_checks = [False for hand in range(count+1)]
        	for i, hand in enumerate(self.hands):
        		if hand.get_value() == 21:
        			b_checks[i] = True
	        return b_checks

        while True:
            self.deck = Deck()
            self.deck.shuffle()

            while True:
            	bankroll = input("Starting Bankroll:")
            	try:
	            	bankroll = int(count)
	            	break
	            except ValueError:
	            	print('Not this time, Satan')
	            	continue

            while True:
	            count = input("Human Players:")
	            try:
	            	count = int(count)
	            	break
	            except ValueError:
	            	print('Not this time either, Satan')
	            	continue

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
                if True in b_checks:
                	game_over = True
                
