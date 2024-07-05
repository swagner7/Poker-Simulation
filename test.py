hand = ['8c', '2c']
position = 6
players = 6

suits = [card[1] for card in hand]  # separate suits from cards
ranks = sorted([card[0] for card in hand], reverse = True)  # separate ranks from cards
conversion_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
for i in range(0, len(ranks)):  # convert face cards to numericals
    try:
        ranks[i] = conversion_dict[ranks[i]]
    except:
        ranks[i] = int(ranks[i])

print(ranks)
if suits[0] == suits[1]: # determine if cards are suited
    suited = True
else:
    suited = False

print('suited', suited)

print([14,13,12])
if position/players >= .75:
    print('late position')
    if suited is True:
        if ranks[0] >= 7 and ranks[1] >= 6 or ranks[0] in [14,13,12] or (ranks[0] - ranks[1] <= 2) and ranks[0] >= 4 or ranks == [11,5] or ranks == [11,4] or ranks == [8,5]:
            bet = True
        else:
            bet = False
    else:
        if ranks[0] >= 9 and ranks[1] >= 8 or ranks[0] == 14 and ranks[1] >= 5:
            bet = True
        else:
            bet = False

elif position/players >= .40:
    print('middle position')
    if suited is True:
        if ranks[0] >= 10 and ranks[1] >= 9 or ranks[0] == 14 or (ranks[0] - ranks[1] == 1) and ranks[0] >= 8:
            bet = True
        else:
            bet = False
    else:
        if ranks[0] == ranks[1] and ranks[0] >= 3 or ranks[0] >= 12 and ranks[1] >= 11 or ranks == [14,10]:
            bet = True
        else:
            bet = False

else:
    print('early position')
    if suited is True:
        if ranks[0] >= 11 and ranks[1] >= 10 or ranks == [10,9]:
            bet = True
        else:
            bet = False
    else:
        if ranks[0] == ranks[1] and ranks[0] >= 6 or ranks[0] == 14 and ranks[1] >= 12:
            bet = True
        else:
            bet = False


print('bet',bet)