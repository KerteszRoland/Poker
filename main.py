class Suit:
    HEART = "h"
    DIAMOND = "d"
    SPADE = "s"
    CLUB = "c"
    SUITS = [HEART, DIAMOND, SPADE, CLUB]


class Card:
    def __init__(self, card_string):
        self.suit = card_string[-1].lower()
        self.rank = "".join(card_string[:-1]).upper()
        self.display = self.rank+self.suit
        self.value = self.GetValue()
        
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.display == other.display
        return False

    def __repr__(self):
        return self.display

    def GetValue(self):
        rank = self.rank
        if rank.isnumeric():
            return int(rank)
        if rank == "J":
            return 11
        if rank == "Q":
            return 12
        if rank == "K":
            return 13
        if rank == "A":
            return 14


class Hand:
    
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

    def __repr__(self):
        return "".join([x.display for x in self.cards])

    def Read(self, comm_cards):
        ev = Evaluate()

        royalflush = ev.RoyalFlush.IsRoyalFlush(comm_cards, self)
        straightflush = ev.StraightFlush.IsStraightFlush(comm_cards, self)
        quads = ev.Quads.IsQuads(comm_cards, self)
        fullhouse = ev.FullHouse.IsFullHouse(comm_cards, self)
        flush = ev.Flush.IsFlush(comm_cards, self)
        straight = ev.Straight.IsStraight(comm_cards, self)
        threeofkind = ev.ThreeOfKind.IsThreeOfKind(comm_cards, self)
        twopair = ev.TwoPair.IsTwoPair(comm_cards, self)
        pair = ev.Pair.IsPair(comm_cards, self)
        high = ev.High.IsHigh(comm_cards, self)

        if royalflush:
            return royalflush
        elif straightflush:
            return straightflush
        elif quads:
            return quads
        elif fullhouse:
            return fullhouse
        elif flush:
            return flush
        elif straight:
            return straight
        elif threeofkind:
            return threeofkind
        elif twopair:
            return twopair
        elif pair:
            return pair
        else:
            return high


class CommunityCards:
    
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

    def __repr__(self):
        return "".join([x.display for x in self.cards])

    def GetFlop(self):
        if len(self.cards) < 3:
            return None
        return self.cards[:3]

    def GetTurn(self):
        if len(self.cards) < 4:
            return None
        return self.cards[3]

    def GetRiver(self):
        if len(self.cards) < 5:
            return None
        return self.cards[4]

    def PushFlop(self, card_list):
        card_list_types = [x for x in card_list if type(x) != Card]
        wrong_type = bool(card_list_types)
        if len(card_list) != 3 or wrong_type:
            raise AttributeError("Flop should contain 3 cards!")
        if len(self.cards) != 0:
            raise Exception("Flop already pushed!")
        self.cards.extend(card_list)

    def PushTurn(self, card):
        if type(card) != Card:
            raise TypeError("You must pass a card type to this function!")
        if len(self.cards) == 0:
            raise Exception("Can't push Turn before Flop!")
        if len(self.cards) > 3:
            raise Exception("Turn already pushed!")
        self.cards.append(card)

    def PushRiver(self, card):
        if type(card) != Card:
            raise TypeError("You must pass a card type to this function!")
        if len(self.cards) < 4:
            raise Exception("Can't push River before Turn or Flop!")
        if len(self.cards) > 4:
            raise Exception("Turn already pushed!")
        self.cards.append(card)

    def GetSuits(self):
        return [x.suit for x in self.cards]


class Evaluate:

    class PokerHand:
        def __repr__(self):
            return "".join([x.display for x in self.cards])

    class RoyalFlush(PokerHand):
        def __init__(self, cards):
            self.cards = cards
            self.suit = cards[0].suit

        @staticmethod
        def IsRoyalFlush(comm_cards, hand):
            straightflush = Evaluate.StraightFlush.IsStraightFlush(comm_cards, hand)
            if straightflush:
                cards = straightflush.cards
                if [x.rank for x in cards] == ["A", "K", "Q", "J", "10"]:
                    return Evaluate.RoyalFlush(cards)
            return False

    class StraightFlush(PokerHand):
        def __init__(self, cards):
            self.cards = cards
            self.high = cards[0]
            self.suit = cards[0].suit

        @staticmethod
        def IsStraightFlush(comm_cards, hand):
            flush = Evaluate.Flush.IsFlush(comm_cards, hand)
            if flush:
                cards = flush.cards
                straight = Evaluate.Straight.IsStraight(CommunityCards(cards))
                if straight:
                    return Evaluate.StraightFlush(straight.cards)
            return False

    class Quads(PokerHand):
        def __init__(self, cards, kicker_card):
            self.cards = cards
            self.card = cards[0]
            self.kicker_card = kicker_card

        def __repr__(self):
            return f"{''.join([x.display for x in self.cards])}+{self.kicker_card}"

        @staticmethod
        def IsQuads(comm_cards, hand):
            all_cards = comm_cards.cards+hand.cards
            all_cards_value = [x.value for x in all_cards]
            for card in all_cards:
                if all_cards_value.count(card.value) == 4:
                    quad_cards = [x for x in all_cards if x.value == card.value]
                    other_cards = [x for x in all_cards if x not in quad_cards]
                    kicker_card = sorted(other_cards, key=lambda x: x.value, reverse=True)[0]
                    return Evaluate.Quads(quad_cards, kicker_card)
            return False

    class FullHouse(PokerHand):
        def __init__(self, threeofkind, pair):
            self.threeofkind = threeofkind
            self.pair = pair

        def __repr__(self):
            cards = self.threeofkind+self.pair
            return "".join([x.display for x in cards])

        @staticmethod
        def IsFullHouse(comm_cards, hand):
            all_cards = sorted(comm_cards.cards+hand.cards, key=lambda x: x.value, reverse=True)
            all_cards_value = [x.value for x in all_cards]
            for card in all_cards:
                if all_cards_value.count(card.value) == 3:
                    three_cards = [x for x in all_cards if x.value == card.value]
                    other_cards = [x for x in all_cards if x not in three_cards]
                    other_cards_values = [x.value for x in other_cards]
                    for card2 in other_cards:
                        if other_cards_values.count(card2.value) == 2:
                            pair_cards = [x for x in other_cards if x.value == card2.value]
                            return Evaluate.FullHouse(three_cards, pair_cards)
            return False

    class Flush(PokerHand):
        def __init__(self, cards, high):
            self.cards = cards
            self.high = high
            self.suit = high.suit

        @staticmethod
        def IsFlush(comm_cards, hand):
            comm_suits = comm_cards.GetSuits()
            hand_suits = [x.suit for x in hand.cards]
            all_suits = comm_suits + hand_suits
            all_cards = comm_cards.cards + hand.cards
            for suit in Suit.SUITS:
                if all_suits.count(suit) >= 5:
                    cards_in_flush = sorted([x for x in all_cards if x.suit == suit], key=lambda x: x.value, reverse=True)
                    high = cards_in_flush[0]
                    return Evaluate.Flush(cards_in_flush, high)
            return False

    class Straight(PokerHand):
        def __init__(self, cards, high):
            self.cards = cards
            self.high = high

        @staticmethod
        def IsStraight(comm_cards, hand=None):
            if hand is None:
                hand = Hand()
            all_cards = comm_cards.cards + hand.cards
            wo_duplicates_cards = []

            for card in all_cards:
                if card.value not in [x.value for x in wo_duplicates_cards]:
                    wo_duplicates_cards.append(card)

            sorted_cards_rev = sorted(wo_duplicates_cards, key=lambda x: x.value, reverse=True)
            temp_cards = []
            for i, card in enumerate(sorted_cards_rev):
                if len(temp_cards) == 5:
                    return Evaluate.Straight(temp_cards, temp_cards[0])

                if i != len(sorted_cards_rev) - 1:
                    if card.value - 1 == sorted_cards_rev[i + 1].value:
                        temp_cards.append(card)
                        if len(temp_cards) == 4:
                            temp_cards.append(sorted_cards_rev[i + 1])
                    else:
                        temp_cards.clear()

            sorted_cards = sorted(wo_duplicates_cards, key=lambda x: x.value)
            is_wheel = False
            if sorted_cards[-1].value == 14:
                for i in range(3):
                    if sorted_cards[i].value + 1 == sorted_cards[i + 1].value:
                        if i == 2:
                            is_wheel = True
                            break
                        else:
                            continue
                    else:
                        break

            if is_wheel:
                return Evaluate.Straight([sorted_cards[-1]] + sorted_cards[:4], sorted_cards[3])

            return False

    class ThreeOfKind(PokerHand):
        def __init__(self, cards, kicker_cards):
            self.cards = cards
            self.card = cards[0]
            self.kicker_cards = kicker_cards

        def __repr__(self):
            return f"{''.join([x.display for x in self.cards])}+{''.join([x.display for x in self.kicker_cards])}"

        @staticmethod
        def IsThreeOfKind(comm_cards, hand):
            all_cards = comm_cards.cards+hand.cards
            all_cards_value = [x.value for x in all_cards]
            for card in all_cards:
                if all_cards_value.count(card.value) == 3:
                    three_cards = [x for x in all_cards if x.value == card.value]
                    kicker_cards = sorted([x for x in all_cards if x not in three_cards],
                                          key=lambda x: x.value, reverse=True)[:2]
                    return Evaluate.ThreeOfKind(three_cards, kicker_cards)
            return False

    class TwoPair(PokerHand):
        def __init__(self, pair1, pair2, kicker):
            self.pair1 = pair1
            self.pair2 = pair2
            self.kicker = kicker

        def __repr__(self):
            return ''.join([x.display for x in self.pair1])+''.join([x.display for x in self.pair2])+"+"+str(self.kicker)

        @staticmethod
        def IsTwoPair(comm_cards, hand):
            all_cards = sorted(comm_cards.cards+hand.cards, key=lambda x: x.value, reverse=True)
            all_cards_value = [x.value for x in all_cards]
            for card in all_cards:
                if all_cards_value.count(card.value) == 2:
                    pair1 = [x for x in all_cards if x.value == card.value]
                    other_cards = [x for x in all_cards if x not in pair1]
                    other_cards_values = [x.value for x in other_cards]
                    for card2 in other_cards:
                        if other_cards_values.count(card2.value) == 2:
                            pair2 = [x for x in other_cards if x.value == card2.value]
                            kicker = [x for x in other_cards if x not in pair2][0]
                            return Evaluate.TwoPair(pair1, pair2, kicker)
            return False

    class Pair(PokerHand):
        def __init__(self, pair, kicker_cards):
            self.pair = pair
            self.kicker_cards = kicker_cards

        def __repr__(self):
            return "".join([x.display for x in self.pair])+"+"+"".join([x.display for x in self.kicker_cards])

        @staticmethod
        def IsPair(comm_cards, hand):
            all_cards = sorted(comm_cards.cards+hand.cards, key=lambda x: x.value, reverse=True)
            all_cards_values = [x.value for x in all_cards]
            for card in all_cards:
                if all_cards_values.count(card.value) == 2:
                    pair = [x for x in all_cards if x.value == card.value]
                    kicker_cards = [x for x in all_cards if x not in pair][:3]
                    return Evaluate.Pair(pair, kicker_cards)
            return False

    class High(PokerHand):
        def __init__(self, high, kicker_cards):
            self.high = high
            self.kicker_cards = kicker_cards

        def __repr__(self):
            return str(self.high)+"+"+"".join([x.display for x in self.kicker_cards])

        @staticmethod
        def IsHigh(comm_cards, hand):
            all_cards = sorted(comm_cards.cards+hand.cards, key=lambda x: x.value, reverse=True)
            high = all_cards[0]
            kicker_cards = all_cards[1:5]
            return Evaluate.High(high, kicker_cards)
