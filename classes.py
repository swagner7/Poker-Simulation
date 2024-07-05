import random
from itertools import cycle, islice, dropwhile

class Deck:
    def __init__(self):
        suits = ['h', 'c', 'd', 's']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

        deck = []
        for i in values: # combine suits and values
            deck.append(str(i + suits[0]))
            deck.append(str(i + suits[1]))
            deck.append(str(i + suits[2]))
            deck.append(str(i + suits[3]))

        random.shuffle(deck) # shuffle deck
        self.cards = deck

    def deal_cards(where, how_many, game, deck, player_objs):
        print('\nDealing...')

        if where == 'community':
            game.community_cards = game.community_cards + deck.cards[:how_many]
            print(f'Community cards are: {game.community_cards}')
            deck.cards = deck.cards[how_many:]

        elif where == 'around':
            for player in player_objs:
                player.hole_cards(deck.cards[:how_many])
                deck.cards = deck.cards[how_many:]

class Game:
    def __init__(self, players_count):
        print('Game started')
        self.pot = 0
        self.hand_number = 1
        self.players_out = 0
        self.community_cards = []
        self.hand_active = True

    def rotate_positions(player_objs):
        player_indexes = list(range(0, len(player_objs)))

        cycled = cycle(player_indexes)  # cycle thorugh the list 'L'
        skipped = dropwhile(lambda x: x != 1, cycled)  # drop the values until x==4
        sliced = islice(skipped, None, len(player_indexes))  # take the first 6 values

        result = list(sliced)  # create a list from iterator

        player_objs_new = []
        for i in range(0, len(result)):
            player_objs_new.append(player_objs[result[i]])

        return(player_objs_new)

    def reset_hand(self, player_objs, leader):
        for player in player_objs:  # award winner the pot and clear pot for next hand
            if player.name == leader:
                player.stack += self.pot
                self.pot = 0

        for guy in player_objs:  # clear hole cards
            del guy.hole_cards
            guy.in_hand = True  # allow everyone back into hand

        self.players_out = 0
        self.community_cards = []  # clear community cards
        return()


class Player(Game):
    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
        self.in_hand = True
        print('Hello, my name is', self.name)

    def hole_cards(self, cards):
        self.hole_cards = cards
        print(f'{self.name} has hole cards: {cards}')

    def bet(self, amount, Game):
        self.stack -= amount
        Game.pot += amount
        print(f'{self.name} bets {amount} and has {self.stack} remaining')

    def fold(self, Game):
        self.in_hand = False
        Game.players_out += 1
        print(f'{self.name} folds')

