# Going to try to make a blackjack Terminal game
# What it needs
# - Players (hands and points)
# - Dealer with deck and playstyle
# - Maybe Low Level CPU
from player import Player
from dealer import Dealer
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


def calc_points(player):
    hand = player.hand
    total = 0
    for card in hand:
        if card[0] == "Ace":
            if player.ace_high:
                total += 11
            else:
                total += 1
            # ace_val = input("Ace high or low:  ")
            # if ace_val == "high":
            #     total += 11
            # else:
            #     total += 1
        else:
            total += card_to_val_dict[card[0]]
    return total

def action_match(player, dealer, action):
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
    points = calc_points(player)
    player.points = points
    if points > 21:
        print(f"Player {player.name} has bust")
        player.has_bust = True
    if points == 21:
        player.has_bj = True
        print(f"Player {player.name} has Blackjack")
        print(f"Player hand: {player.hand}")
    
def action_loop(player_list, dealer):
    for player in player_list:
        checker(player)
        if isinstance(player, Dealer):
            player.dealer_action()
        else:
            action = input("Player Action: ")
            action_match(player, dealer, action)
        checker(player)
    
def first_check(player_list):
    for player in player_list:
        if player.points == 21:
            player.has_bj = True
            print(f"{player.name} has BlackJack!")
            return True
    return False

def place_bets(player, dealer, bet):
    player.place_bet(bet)
    dealer.add_to_pot(bet)
    print(f"The pot sits at {dealer.pot}")
    

test_deck = shuffle_deck(make_deck(suits, cards))

dealer = Dealer(test_deck)
player1 = Player("Zack", 100)
player_list = [dealer, player1]
i = 1

while True:
    #1. Resetting the Table
    for player in player_list:
        player.reset()
    
    #2. Placing bets
    print(f"--- How much are you betting?? ---")
    while True:
        try:
            bet = int(input("Bet Amount: "))
            if bet > player1.chips:
                print("Cannot bet more than you have!!!")
            else:
                break
        except ValueError:
            print("Bet has to be an int!!!")
     
    place_bets(player1, dealer, bet)
    
    #3. Dealing Hands to all Players
    print(f"--- Dealing Hand #{i} ---")
    dealer.deal_hands(player_list)
    
    print("--- Current Hands ---")
    # 4. Checking for BlackJack on starting Hands
    flag = False
    for player in player_list:
        if flag:
            break
        
        print(f"Player Hand: {player.name}")
        player.print_hand()
        checker(player)
        if player.has_bj:
            flag = True
            break
        player.ace_high = False

    print("------------------")
    # no_bust = first_check(player_list)
    #5. Player Loop
    player_turn = True
    while player_turn:
        player1.action = input("Player action: ")
        player_turn = action_match(player1, dealer, player1.action)
        player1.print_hand()
        checker(player1)
        if player1.has_bust:
            break
    
    print("------------------")
    #6. Dealer Turn
    if not player1.has_bust:
        dealer_turn = True
        while dealer_turn:
            dealer_turn = dealer.dealer_action()
            checker(dealer)
            if dealer.has_bust:
                break
        
    print("------------------")
    #7. Checking Winner
    if dealer.points > player1.points or player1.has_bust == True:
        print("!!! Dealer Wins !!!")
        print(f"Dealer's Hand: {dealer.print_hand()}")
        print(f"Dealer's Total: {dealer.points}")
        print(f"{player1.name}'s Hand: {player1.print_hand()}")
        print(f"{player1.name}'s Total: {player1.points}")
        print(f"{player1.name}'s Chips: {player1.chips}")
    else:
        print("!!! Player Wins !!!")
        print(f"Dealer's Hand: {dealer.print_hand()}")
        print(f"Dealer's Total: {dealer.points}")
        print(f"{player1.name}'s Hand: {player1.print_hand()}")
        print(f"{player1.name}'s Total: {player1.points}")
        player1.chips += dealer.pot
        print(f"{player1.name}'s Chips: {player1.chips}")
    
    print("------------------")
    #8. Player's current chips
    if player1.chips <= 0:
        print(f"--- {player1.name} has no more chips!!! ---")
        print("--- GAME OVER ---")
        break
    
    #9. Play Again
    again = input("Play another hand?... ")
    if again == "n":
        break
    
    i+=1
    
    
