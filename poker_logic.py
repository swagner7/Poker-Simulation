import heapq

class Poker:
    def evaluate_hand(player, hole, community):
        hand = hole + community
        conversion_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        def check_straight(ranks_copy1):  # function to check for straight that returns the high and range of the straight
            straight_high = 0
            straight_range = []
            straight_high_test = 0
            while len(ranks_copy1) >= 5:
                count = 0
                for j in (14, *range(2, 15)):
                    if j in ranks_copy1:
                        count += 1
                        if count == 5:
                            straight_high_test = j
                            break
                    else:
                        count = 0

                if straight_high_test > straight_high:
                    straight_high = straight_high_test

                ranks_copy1.remove(min(ranks_copy1))

            if straight_high == 5 and 6 in ranks_copy1:  # account for special case where 5-high straight and 6-high straight are present
                straight_high = 6

            straight_range = list(range(straight_high - 4, straight_high + 1))
            straight_range = sorted([14 if item == 1 else item for item in straight_range], reverse=True)  # replace 1 with 14 in range and sort
            return (straight_high, straight_range)

        def check_flush(ranks_copy2):  # function to check for flush and return flush high and ranks in flush
            flush_high = 0
            flush_ranks = []
            res_value = 0
            if max(suit_counts) >= 5:
                flush_high = max(ranks_copy2)

                indices = [i for i, x in enumerate(suit_counts) if x == max(suit_counts)]  # find indices of the flush cards
                flush_ranks = sorted([ranks[i] for i in indices], reverse=True)[:5]  # pull the top 5 ranks of the flush
                flush = max(flush_ranks)  # find the max rank of the flush cards

                res_value = 0
                for i in range(1, len(flush_ranks)):  # calculate residual value of flush
                    res_value = round(res_value + (flush_ranks[i] / (10 ** i)), 6)

            return (flush_high, flush_ranks, res_value)

        ranks = [card[0] for card in hand]  # separate ranks from cards
        suits = [card[1] for card in hand]  # separate suits from cards

        for i in range(0, len(ranks)):  # convert face cards to numericals
            try:
                ranks[i] = conversion_dict[ranks[i]]
            except:
                ranks[i] = int(ranks[i])

        rank_counts = [ranks.count(i) for i in ranks]  # count repetitions for each rank
        suit_counts = [suits.count(i) for i in suits]  # count repetitions for each suit
        ranks_copy1 = sorted(ranks)  # copy ranks list to throw into check_straight
        ranks_copy2 = sorted(ranks)  # copy ranks list to throw into check_flush

        [straight_high, straight_range] = check_straight(ranks_copy1)  # check straight and return high card of straight
        [flush_high, flush_ranks, res_value] = check_flush(ranks_copy2)  # check straight and return high card of straight

        if set([14, 13, 12, 11, 10]).issubset(ranks) and 5 in suit_counts:  # check for royal flush
            hand_type = 'royal flush'
            hand_score = 1000

        elif flush_ranks == straight_range and straight_high != 0:  # check for straight flush
            hand_type = f'straight flush - {straight_high} high'
            hand_score = 800 + straight_high

        elif 4 in rank_counts:  # check for 4
            four = ranks[rank_counts.index(4)]  # find the 4
            hand_type = f'four of a kind - {four}s'
            hand_score = 700 + four

        elif set([3, 3, 3, 2, 2]).issubset(rank_counts):  # check for boat
            indices_3 = [i for i, x in enumerate(rank_counts) if x == 3]  # find indices of the trips
            indices_2 = [i for i, x in enumerate(rank_counts) if x == 2]  # find indices of the pair
            card_3 = [ranks[i] for i in indices_3][0]  # pull value from trips
            card_2 = [ranks[i] for i in indices_2][0]  # pull value from pair
            hand_type = f'full house - {card_3}s full of {card_2}s'
            hand_score = 600 + card_3 + card_2 / 100

        elif flush_high != 0:  # check for flush
            hand_type = f'flush - {flush_high} high with {res_value} residual value'
            hand_score = 500 + flush_high + res_value

        elif straight_high != 0:  # check for straight
            hand_type = f'straight - {straight_high} high'
            hand_score = 400 + straight_high

        elif 3 in rank_counts:  # check for set
            three = ranks[rank_counts.index(3)]  # find the 3
            remaining = [x for x in ranks if x != three]  # remove the paired values to find remaining value of hand
            res_value = sum(heapq.nlargest(2, remaining))  # calculate the residual value of the next 3 highest cards

            hand_type = f'three of a kind - three {three}s with {res_value} residual value'
            hand_score = 300 + three + (res_value / 100)

        elif rank_counts.count(2) == 4:  # check for 2 pair
            pairs = []
            remaining = []

            for i in ranks:  # separate pairs from non-pairs
                if i not in remaining:
                    remaining.append(i)
                else:
                    pairs.append(i)

            for i in pairs:  # remove paired values from remaining ones
                remaining.remove(i)

            high = max(pairs)
            low = min(pairs)

            res_value = max(remaining)
            hand_type = f'two pair - {high}s and {low}s with {res_value} residual value'
            hand_score = round(200 + high + low / 10 + res_value / 100, 3)

        elif 2 in rank_counts:  # check for pair
            pair = ranks[rank_counts.index(2)]  # find the pair
            remaining = [x for x in ranks if x != pair]  # remove the paired values to find remaining value of hand
            res_value = sum(heapq.nlargest(3, remaining))  # calculate the residual value of the next 3 highest cards

            hand_type = f'pair - pair of {pair}s with {res_value} residual value'
            hand_score = 100 + pair + (res_value / 100)

        else:
            high = max(ranks)
            remaining = [x for x in ranks if x != high]  # remove the paired values to find remaining value of hand
            res_value = sum(heapq.nlargest(3, remaining))  # calculate the residual value of the next 3 highest cards

            hand_type = f'high card - {high} high with {res_value} residual value'
            hand_score = high + (res_value / 100)

        print(f'{player} has {hand_type}')
        return(hand_type, hand_score)


    def Negranu_ranges(hand, player, players, position):
        suits = [card[1] for card in hand]  # separate suits from cards
        ranks = sorted([card[0] for card in hand], reverse=True)  # separate ranks from cards
        conversion_dict = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        for i in range(0, len(ranks)):  # convert face cards to numericals
            try:
                ranks[i] = conversion_dict[ranks[i]]
            except:
                ranks[i] = int(ranks[i])

        if suits[0] == suits[1]:  # determine if cards are suited
            suited = True
        else:
            suited = False

        if position / players >= .75:
            if suited is True:
                if ranks[0] >= 7 and ranks[1] >= 6 or ranks[0] in [14, 13, 12] or (ranks[0] - ranks[1] <= 2) and \
                        ranks[0] >= 4 or ranks == [11, 5] or ranks == [11, 4] or ranks == [8, 5]:
                    bet = True
                else:
                    bet = False
            else:
                if ranks[0] >= 9 and ranks[1] >= 8 or ranks[0] == 14 and ranks[1] >= 5:
                    bet = True
                else:
                    bet = False

        elif position / players >= .40:
            if suited is True:
                if ranks[0] >= 10 and ranks[1] >= 9 or ranks[0] == 14 or (ranks[0] - ranks[1] == 1) and ranks[0] >= 8:
                    bet = True
                else:
                    bet = False
            else:
                if ranks[0] == ranks[1] and ranks[0] >= 3 or ranks[0] >= 12 and ranks[1] >= 11 or ranks == [14, 10]:
                    bet = True
                else:
                    bet = False

        else:
            if suited is True:
                if ranks[0] >= 11 and ranks[1] >= 10 or ranks == [10, 9]:
                    bet = True
                else:
                    bet = False
            else:
                if ranks[0] == ranks[1] and ranks[0] >= 6 or ranks[0] == 14 and ranks[1] >= 12:
                    bet = True
                else:
                    bet = False

        return(bet)
