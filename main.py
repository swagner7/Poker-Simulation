from classes import Deck, Game, Player
from poker_logic import Poker
import os

# initalize variables -------------------------------------------------------------------------------------------------
players_count = 8
initial_stack = 200
num_hands = 1

game = Game(players_count) # initialize game instance

print('\nGenerating players...')
player_objs = [Player(f'Player{i}', initial_stack) for i in range(players_count)] # generate players


# play hand ===============================================================================
while game.hand_number <= num_hands:
    print('\nHand number: ', game.hand_number)
    deck = Deck()  # generate deck
    print(deck.cards)

    print('\nShall we play a hand...?')
    player_objs = Game.rotate_positions(player_objs) # rotate positions
    game.hand_number += 1 # increment hand number

    # pre-flop --------------------------------------
    for player in player_objs: # ante up
        player.bet(1, game)

    Deck.deal_cards('around', 2, game, deck, player_objs) # deal out hole cards

    score = []
    player = []
    pos = 1
    for guy in player_objs:
        if game.players_out < (players_count - 1): # if more than 1 player remain
            if guy.in_hand is True:
                [hand_type, hand_score] = Poker.evaluate_hand(guy.name, guy.hole_cards, game.community_cards) # evaluate hand
                bet_decision = Poker.Negranu_ranges(guy.hole_cards, guy.name, len(player_objs), pos)  # use Negranu's ranges to choose to bet or not
                if bet_decision is True:
                    guy.bet(2, game)
                else:
                    guy.fold(game)

                player.append(guy.name)
                score.append(hand_score)
                pos += 1
        else:
            break
            game.hand_active = False

    scores_dict = {k: v for k, v in sorted(dict(zip(player, score)).items(), key=lambda item: item[1], reverse=True)} # organize players and scores into a dict and sort
    leader = max(scores_dict, key=scores_dict.get)
    print(f'Current leader is {leader} with {scores_dict[leader]}')

    # flop ------------------------------------------------------------------------
    Deck.deal_cards('community', 3, game, deck, player_objs) # deal out flop
    score = []
    player = []
    if game.hand_active is True:
        for guy in player_objs:
            if guy.in_hand is True:
                [hand_type, hand_score] = Poker.evaluate_hand(guy.name, guy.hole_cards, game.community_cards) # evaluate hand
                player.append(guy.name)
                score.append(hand_score)

    scores_dict = {k: v for k, v in sorted(dict(zip(player, score)).items(), key=lambda item: item[1], reverse=True)} # organize players and scores into a dict and sort
    leader = max(scores_dict, key=scores_dict.get)
    print(f'Current leader is {leader} with {scores_dict[leader]}')

    # turn ---------------------------------------------------------
    Deck.deal_cards('community', 1, game, deck, player_objs) # deal out turn
    score = []
    player = []
    if game.hand_active is True:
        for guy in player_objs:
            if guy.in_hand is True:
                [hand_type, hand_score] = Poker.evaluate_hand(guy.name, guy.hole_cards, game.community_cards) # evaluate hand
                player.append(guy.name)
                score.append(hand_score)

    scores_dict = {k: v for k, v in sorted(dict(zip(player, score)).items(), key=lambda item: item[1], reverse=True)} # organize players and scores into a dict and sort
    leader = max(scores_dict, key=scores_dict.get)
    print(f'Current leader is {leader} with {scores_dict[leader]}')

    # river -------------------------------------------------------------------
    Deck.deal_cards('community', 1, game, deck, player_objs) # deal out river
    score = []
    player = []
    if game.hand_active is True:
        for guy in player_objs:
            if guy.in_hand is True: # if the player has not folded
                [hand_type, hand_score] = Poker.evaluate_hand(guy.name, guy.hole_cards, game.community_cards) # evaluate hand
                player.append(guy.name)
                score.append(hand_score)

    scores_dict = {k: v for k, v in sorted(dict(zip(player, score)).items(), key=lambda item: item[1], reverse=True)} # organize players and scores into a dict and sort
    leader = max(scores_dict, key=scores_dict.get)
    print(f'Winner is {leader} with {scores_dict[leader]}')


    game.reset_hand(player_objs, leader) # reset for next hand


print('\nFinal stack sizes:')
for guy in player_objs:
    print(guy.name, guy.stack)