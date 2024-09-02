## IMPORTS
import random
import os


## CONSTANTS
SUITS = ('Hearts','Diamonds','Spades','Clubs')
RANKS = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
VALUES = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}


## CLASSES
class Card:
    ''' Represents a card from a deck. '''
    def __init__(self,suit,ranks):
        self.suit = suit
        self.rank = ranks
        self.value = VALUES[ranks]
        
    def __str__(self):
        return f'{self.rank} of {self.suit}'
    
class Deck:
    ''' Represents a deck of cards. '''
    def __init__(self):
        self.all_cards = []
        
        for shape in SUITS:
            for num in RANKS:
                new_card = Card(shape,num)
                self.all_cards.append(new_card)
        
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    def hit(self):
         return self.all_cards.pop(0)
     
class AllParticipants:
    ''' Represents all participants playing in game. '''
    def __init__(self):
        self.hand = []
        self.total_values = 0
    
    def add_to_total(self):
        ''' Totals the values of the cards in a hand. '''
        if len(self.hand) == 2:
            self.total_values = self.total_values + self.hand[0].value + self.hand[1].value
        else:
            self.total_values = self.total_values + self.hand[-1].value
            
        return (self.total_values > 21)
        
    def held_cards(self):
        ''' Prints cards in a hand to console. '''
        for card in self.hand:
            print(card)
            
class Player(AllParticipants):
    ''' Represents the player. '''
    def __init__(self,name,balance):
        AllParticipants.__init__(self)
        self.name = name
        self.balance = balance
        self.bet_amount = 0
        
    def bet(self):
        ''' Takes input on bet amount and verifies if it is valid. '''
        while True:
            try:
                self.bet_amount = int(input("Input Bet Amount: "))
            except:
                print("invalid input, try again \n")
            else:
                if self.bet_amount <= self.balance:
                    print(f'{self.name} has bet ${self.bet_amount} \n')
                    break
                else:
                    print("over balance amount, try again")
    
    def add(self):
        ''' Adds winnings to player's money balance. '''
        winnings = int(self.bet_amount * .5)
        self.balance = self.balance + winnings
    
    def lose(self):
        ''' Subtracts loses from player's money balance. '''
        self.balance = self.balance - self.bet_amount
    
    def money(self):
        ''' Returns string stating player's current money balance. '''
        return (f'{self.name} currently has ${self.balance} \n')
    
class Dealer(AllParticipants):
    ''' Represents a card dealer. '''
    def __init__(self):
        AllParticipants.__init__(self)
    
    def hidden_hand(self):
        ''' Prints Dealer's cards when one is still hidden. '''
        print(f"Dealer's Cards: \n{self.hand[0]} \nHidden Card")


## FUNCTIONS
def start():
    '''
    Takes input from user about starting game.
    '''
    while True:
        go = input('Ready to Start?: y or n ')
        if go in ['y','Y']:
            return True
            break
        elif go in ['n','N']:
            return False
            break
        else:
            print('invalid input, try again')
            
def play_again():
    '''
    Takes input from user about whether they want to continue the game or not.
    '''
    while True:
        go = input('Want to play again?: y or n ')
        if go in ['y','Y']:
            return True
            break
        elif go in ['n','N']:
            return False
            break
        else:
            print('invalid input, try again')
            
def hit_stand_q():
    '''
    Takes input from user whether they want to hit or stand.
    '''
    while True:
        answer = input("Do you want to Hit or Stand?: ")
        
        if answer in ['hit','Hit']:
            return True
            break
        elif answer in ['stand','Stand']:
            return False
            break
        else:
            print("invalid response, try again")
            
def cls():
    '''
    Clears the terminal screen.
    https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
    '''
    os.system('cls' if os.name=='nt' else 'clear')


## MAIN GAME   
game_start = True
game_on = False

while game_start:
    cls()
    name = input("What is your name?: ")
    
    player = Player(name,500)
    dealer = Dealer()
    print(f"Welcome to BlackJack {player.name} \nYou have been given $500 to start with \n\nHow to Play: \nit's you vs the dealer, whoever gets closest to 21 without going over wins \n")
    
    game_on = start()
    dealer_deck = Deck()
    dealer_deck.shuffle()
    print("Deck is Shuffled \n")
    
    while game_on:
        cls()
        dealer.hand = []
        player.hand = []
        player.total_values = 0
        dealer.total_values = 0
        
        print(player.money())
        player.bet()
        #first deal
        win = True
        player.hand = [dealer_deck.hit(),dealer_deck.hit()]
        dealer.hand = [dealer_deck.hit(),dealer_deck.hit()]
        
        dealer.add_to_total()
        player.add_to_total()
        
        print(f"{player.name}'s Hand:")
        player.held_cards()
        dealer.hidden_hand()
        
        #naturals
        if dealer.total_values == 21 and player.total_values == 21:
            print(f"{player.name}'s Cards:")
            player.held_cards()
            print("\n Dealer's Cards:")
            dealer.held_cards()
            win = True
        elif player.total_values == 21:
            print(f"{player.name}'s Cards:")
            player.held_cards()
            win = True
        elif dealer.total_values == 21:
            print("Dealer's Cards:")
            dealer.held_cards()
            win = True
        else:
            win = False
        
        #hit or stand
        while win == False:
            while win == False:
                hs_answer = hit_stand_q()
                if hs_answer:
                    player.hand.append(dealer_deck.hit())
                    win = player.add_to_total()
                    print("Updated Cards \n")
                    player.held_cards()
                    dealer.hidden_hand()
                else:
                    break
            
            #dealer turn
            while True:
                if dealer.total_values <= 16:
                    dealer.hand.append(dealer_deck.hit())
                    dealer.add_to_total()
                else:
                    break
            win = True
        
        winnings = int(player.bet_amount * 1.5)
        
        if player.total_values == dealer.total_values > 21:
            print(" \n")
            print("Dealer's Cards:")
            dealer.held_cards()
            print("Double Bust, Money Returned \n")
        elif player.total_values > 21:
            print(f"BUST, You Lost ${player.bet_amount} \n")
            player.lose()
        elif dealer.total_values > 21:
            print(" \n")
            print("Dealer's Cards:")
            dealer.held_cards()
            print(f"Dealer Busts \nYou Win, You Get ${winnings} \n")
            player.add()
        elif player.total_values == dealer.total_values:
            print(" \n")
            print("Dealer's Cards:")
            dealer.held_cards()
            print("Draw, Money Returned")
        elif abs(player.total_values - 21) > abs(dealer.total_values - 21):
            print(" \n")
            print("Dealer's Cards:")
            dealer.held_cards()
            print(f"Sorry, {player.name}. You lose ${player.bet_amount} \n")
            player.lose()
        elif abs(player.total_values - 21) < abs(dealer.total_values - 21):
            print(" \n")
            print("Dealer's Cards:")
            dealer.held_cards()
            print(f"Congrats {player.name}! You win ${winnings} \n") 
            player.add()
        
        player.money()
        #play again?
        
        if len(dealer_deck.all_cards) < 8:
            print('Deck is Reshuffled')
            dealer_deck = Deck()
            dealer_deck.shuffle()
        else:
            pass
        if player.balance >= 1:
            game_on = play_again()
        else:
            print("You have no more money so you've been kicked out. BYE")
            game_on = False
    print(f"You left with ${player.balance}")
    game_start = False