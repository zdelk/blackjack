
class Player():
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.points = 0
        self.action = None
        self.action_dict = {0 : "stay",
                            1 : "hit",
                            }
        self.has_bust = False
        self.has_bj = False
        self.ace_high = True
    
    # def choose_action(self, action):
    #     self.action = self.action_dict[action]
    #     print(f"Player choose to {self.action}")
    #     match self.action:
    #         case "stay":
    #             self.stand()
    #         case "hit":
    #             self.hit(card)
            
    def place_bet(self, bet):
        self.chips -= bet
        print(f"{self.name} bets {bet}")
    
    def hit(self, card):
        self.hand.append(card)
    
    def split(self):
        pass
    
    def stand(self):
        pass
    
    def double_down(self):
        pass
    
    def print_hand(self):
        output = ""
        # output = self.hand[0][0] + " of " + self.hand[0][1]
        for card in self.hand:
            output += f"|{card[0]} of {card[1]}| "
            
        print(output)
        return output
        
    def reset(self):
        self.hand = []
        self.points = 0
        self.has_bust = False
        self.has_bj = False
        self.ace_high = True
        