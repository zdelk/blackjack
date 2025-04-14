# Going to try to make a blackjack Terminal game
# What it needs
# - Players (hands and points)
# - Dealer with deck and playstyle
# - Maybe Low Level CPU
from player import Player
import random
random.seed(0)

suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
cards = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

card_to_val_dict = {"Ace": [1, 11],
                    "2": 2,
                    "3": 3,
                    "4": 4,
                    "5": 5,
                    "6" : 6,
                    "7" : 7,
                    "8" : 8,
                    "9" : 9,
                    "10" : 10,
                    "Jack" : 10,
                    "Queen" : 10,
                    "King" : 10,
                    }

def make_deck(suits, cards):
    deck = []
    for suit in suits:
        for card in cards:
            deck.append((card,suit))
    
    return deck

def shuffle_deck(deck):
    shuffled_deck = random.sample(deck, len(deck))
    return shuffled_deck

def cut_deck(deck, index):
    new_deck = deck[index:] + deck[:index]
    return new_deck

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
    
    def print_hand(self):
        output = ""
        # output = self.hand[0][0] + " of " + self.hand[0][1]
        for card in self.hand:
            output += f"{card[0]} of {card[1]} "
            
        print(output)

def calc_points(hand):
    total = 0
    for card in hand:
        if card[0] is "Ace":
            ace_val = input("Ace high or low:  ")
            if ace_val == "high":
                total += 11
            else:
                total += 1
        else:
            total += card_to_val_dict[card[0]]
    return total


test_deck = shuffle_deck(make_deck(suits, cards))

dealer = Dealer(test_deck)
player1 = Player("Zack", 100)
player_list = [dealer, player1]

def action_match(player, action):
    match action:
        case "stay":
            player.stand()
            return False
        case "hit":
            card = dealer.deal_card()
            player.hit(card)
            return True
        case _:
            return False
        
def checker(player):
    points = calc_points(player.hand)
    player.points = points
    if points > 21:
        print(f"Player {player.name} has bust")
        player.has_bust = True
    if points == 21:
        player.has_bj = True
        print(f"Player {player.name} has Blackjack")
        print(f"Player hand: {player.hand}")
    
def action_loop(player_list):
    for player in player_list:
        checker(player)
        if isinstance(player, Dealer):
            player.dealer_action()
        else:
            action = input("Player Action: ")
            action_match(player, action)
        checker(player)
    
def first_check(player_list):
    for player in player_list:
        if player.points == 21:
            print(f"{player.name} has BlackJack!")
            return True
    return False

i = 1

while True:
    for player in player_list:
        player.reset()
    
    print(f"--- Dealing Hand #{i} ---")
    dealer.deal_hands(player_list)
    print("--- Current Hands ---")
    for player in player_list:
        print(f"Player Hand: {player.name}")
        player.print_hand()
        checker(player)
        if player.has_bj:
            break
        
        if player.has_bust:
            print(f"Player {player.name} has bust")
            no_bust = False
            break
        
    # no_bust = first_check(player_list)
    # Player Loop
    player_turn = True
    while player_turn:
        player1.action = input("Player action: ")
        player_turn = action_match(player1, player1.action)
        player1.print_hand()
        checker(player1)
        if player1.has_bust:
            print(f"Player {player1.name} has bust")
            break
    
    if not player1.has_bust:
        dealer_turn = True
        while dealer_turn:
            dealer_turn = dealer.dealer_action()
            checker(dealer)
            if dealer.has_bust:
                print(f"Dealer has bust")
                break
        
    if dealer.points > player1.points or player1.has_bust == True:
        print("!!! Dealer Wins !!!")
    else:
        print("!!! Player Wins !!!")
        
    again = input("Play another hand?... ")
    if again == "n":
        break
    
    i+=1
    
    
