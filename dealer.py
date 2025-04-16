
class Dealer():
    def __init__(self, deck):
        self.name = "Dealer"
        self.deck = deck
        self.hand = []
        self.seventeen_rule = None
        self.points = 0
        self.pot = 0
        self.action = None
        self.has_bust = False
        self.has_bj = False
        self.ace_high = True
    
    def deal_hands(self, player_list):
        total_out = 0
        while total_out < len(player_list) * 2:
            for player in player_list:
                player.hand.append(self.deal_card())
                total_out += 1    
    
    def deal_card(self):
        card = self.deck.pop()
        return card
    
    def dealer_action(self):
        if self.points < 17:
            print("Dealer hits...")
            card = self.deal_card()
            self.hit(card)
            return True
        else:
            print("Dealer Stays")
            return False
        
    def hit(self, card):
        self.hand.append(card)
    
    def add_to_pot(self, bet):
        self.pot = 2*bet

    def reset(self):
        self.pot = 0
        self.hand = []
        self.points = 0
        self.has_bust = False
        self.has_bj = False
        self.ace_high = True
    
    def print_hand(self):
        output = ""
        # output = self.hand[0][0] + " of " + self.hand[0][1]
        for card in self.hand:
            output += f"|{card[0]} of {card[1]}| "
            
        print(output)
        return output
    
    def print_top_card(self):
        print(f"{self.hand[0][0]} of {self.hand[0][1]}")