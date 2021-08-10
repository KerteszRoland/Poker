import random


class PokerExceptions(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

    class IncorrectSuit(Exception):
        pass

    class IncorrectRank(Exception):
        pass

    class IncorrectCardString(Exception):
        pass


class Suit:
    HEART = "h"
    DIAMOND = "d"
    SPADE = "s"
    CLUB = "c"
    SUITS = [HEART, DIAMOND, SPADE, CLUB]


class Card:
    def __init__(self, card_string):
        if type(card_string) is not str or len(card_string) < 2:
            raise PokerExceptions.IncorrectCardString("Cannot create a card with this card_string")
        self.suit = card_string[-1].lower()
        self.rank = "".join(card_string[:-1]).upper()
        if self.suit not in Suit.SUITS:
            raise PokerExceptions.IncorrectSuit("Cannot create card without a correct suit!")
        if self.rank not in ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]:
            raise PokerExceptions.IncorrectRank("Cannot create card without a correct rank!")
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
    @staticmethod
    def GetWinnerHands(comm_cards, hands):
        best_hand = hands[0]
        winner_hands = []
        for hand in hands:
            hand_pokerhand = hand.Read(comm_cards)
            best_hand_pokerhand = best_hand.Read(comm_cards)

            if hand_pokerhand > best_hand_pokerhand:
                best_hand = hand
                winner_hands.clear()
                winner_hands.append(hand)
            elif hand_pokerhand == best_hand_pokerhand:
                winner_hands.append(hand)

        return winner_hands

    class PokerHand:
        def __repr__(self):
            return "".join([x.display for x in self.cards])

    class RoyalFlush(PokerHand):
        def __init__(self, cards):
            self.cards = cards
            self.suit = cards[0].suit
            self.value = 10

        def GetName(self):
            return "RoyalFlush"

        def __gt__(self, other):
            if isinstance(other, Evaluate.PokerHand):
                return not isinstance(other, Evaluate.RoyalFlush)
            return False

        def __eq__(self, other):
            if isinstance(other, Evaluate.RoyalFlush):
                return self.cards == other.cards
            return False

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
            self.value = 9

        def GetName(self):
            return f"{self.high.rank} high StraightFlush"

        def __gt__(self, other):
            if isinstance(other, Evaluate.PokerHand):
                if isinstance(other, Evaluate.StraightFlush):
                    return self.high.value > other.high.value
                else:
                    return self.value > other.value
            return False

        def __eq__(self, other):
            if isinstance(other, Evaluate.StraightFlush):
                return self.cards == other.cards
            return False

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
        def __init__(self, quad_cards, kicker_card):
            self.quad_cards = quad_cards
            self.kicker_card = kicker_card
            self.value = 8

        def __repr__(self):
            return f"{''.join([x.display for x in self.quad_cards])}+{self.kicker_card}"

        def GetName(self):
            return f"{self.quad_cards[0].rank} Quads + {self.kicker_cards.rank}"

        def __gt__(self, other):
            if isinstance(other, Evaluate.PokerHand):
                if isinstance(other, Evaluate.Quads):
                    if self.quad_cards[0].value == other.quad_cards[0].value:
                        return self.kicker_card.value > other.kicker_card.value
                    else:
                        return self.quad_cards[0].value > other.quad_cards[0].value
                else:
                    return self.value > other.value
            return False

        def __eq__(self, other):
            if isinstance(other, Evaluate.Quads):
                return self.quad_cards[0].value == other.quad_cards[0].value \
                       and self.kicker_card.value == other.kicker_card.value
            return False

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
            self.value = 7

        def __repr__(self):
            cards = self.threeofkind+self.pair
            return "".join([x.display for x in cards])

        def __gt__(self, other):
            if isinstance(other, Evaluate.PokerHand):
                if isinstance(other, Evaluate.FullHouse):
                    if self.threeofkind[0].value == other.threeofkind[0].value:
                        return self.pair[0].value > other.pair[0].value
                    else:
                        return self.threeofkind[0].value > other.threeofkind[0].value
                else:
                    return self.value > other.value
            return False

        def __eq__(self, other):
            if isinstance(other, Evaluate.FullHouse):
                return self.threeofkind[0].value == other.threeofkind[0].value \
                       and self.pair[0].value == other.pair[0].value
            return False

        def GetName(self):
            return f"{self.threeofkind[0].rank} {self.pair[0].rank} FullHouse"

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
            self.value = 6

        def GetName(self):
            return f"{self.high.rank} high Flush + {''.join([x.rank for x in self.cards[1:5]])}"

        def __gt__(self, other):
            if isinstance(other, Evaluate.PokerHand):
                if isinstance(other, Evaluate.Flush):
                    hand_cards_values = [x.value for x in self.cards]
                    other_cards_values = [x.value for x in other.cards]
                    for i in range(len(self.cards)):
                        if hand_cards_values[i] > other_cards_values[i]:
                            return True
                        elif hand_cards_values[i] < other_cards_values[i]:
                            return False
                    return False
                else:
                    return self.value > other.value
            return False

        def __eq__(self, other):
            if isinstance(other, Evaluate.Flush):
                return [x.value for x in self.cards[:5]] == [x.value for x in other.cards[:5]]
            return False

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
            self.value = 5

        def __gt__(self, other):
            if isinstance(other, Evaluate.PokerHand):
                if isinstance(other, Evaluate.Straight):
                    return self.high.value > other.high.value
                else:
                    return self.value > other.value
            return False

        def __eq__(self, other):
            if isinstance(other, Evaluate.Straight):
                return self.high.value == other.high.value
            return False

        def GetName(self):
            return f"{self.high.rank} high Straight"

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
        def __init__(self, three_cards, kicker_cards):
            self.three_cards = three_cards
            self.kicker_cards = kicker_cards
            self.value = 4

        def __repr__(self):
            return f"{''.join([x.display for x in self.three_cards])}+{''.join([x.display for x in self.kicker_cards])}"

        def __gt__(self, other):
            if isinstance(other, Evaluate.PokerHand):
                if isinstance(other, Evaluate.ThreeOfKind):
                    if self.three_cards[0].value == other.three_cards[0].value:
                        if self.kicker_cards[0].value == other.kicker_cards[0].value:
                            return self.kicker_cards[1].value > other.kicker_cards[1].value
                        else:
                            return self.kicker_cards[0].value > other.kicker_cards[0].value
                    else:
                        return self.three_cards[0].value > other.three_cards[0].value
                else:
                    return self.value > other.value
            return False

        def __eq__(self, other):
            if isinstance(other, Evaluate.ThreeOfKind):
                return self.three_cards[0].value == other.three_cards[0].value and \
                       [x.value for x in self.kicker_cards] == [x.value for x in other.kicker_cards]
            return False

        def GetName(self):
            return f"{self.three_cards[0].rank} Three of a kind + {''.join([x.rank for x in self.kicker_cards])}"

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
            self.value = 3

        def __repr__(self):
            return ''.join([x.display for x in self.pair1])+''.join([x.display for x in self.pair2])+"+"+str(self.kicker)

        def __gt__(self, other):
            if isinstance(other, Evaluate.PokerHand):
                if isinstance(other, Evaluate.TwoPair):
                    if self.pair1[0].value == other.pair1[0].value:
                        if self.pair2[0].value == other.pair2[0].value:
                            return self.kicker.value > other.kicker.value
                        else:
                            return self.pair2[0].value > other.pair2[0].value
                    else:
                        return self.pair1[0].value > other.pair1[0].value
                else:
                    return self.value > other.value
            return False

        def __eq__(self, other):
            if isinstance(other, Evaluate.TwoPair):
                return self.pair1[0].value == other.pair1[0].value and self.pair2[0].value == other.pair2[0].value \
                       and self.kicker == other.kicker
            return False

        def GetName(self):
            return f"{self.pair1[0].rank} {self.pair2[0].rank} Two Pair + {self.kicker.rank}"

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
            self.value = 2

        def __repr__(self):
            return "".join([x.display for x in self.pair])+"+"+"".join([x.display for x in self.kicker_cards])

        def __gt__(self, other):
            if isinstance(other, Evaluate.PokerHand):
                if isinstance(other, Evaluate.Pair):
                    if self.pair[0].value == other.pair[0].value:
                        hand_cards_values = [x.value for x in self.kicker_cards]
                        other_cards_values = [x.value for x in other.kicker_cards]
                        for i in range(len(self.kicker_cards)):
                            if hand_cards_values[i] > other_cards_values[i]:
                                return True
                            elif hand_cards_values[i] < other_cards_values[i]:
                                return False
                        return False
                    else:
                        return self.pair[0].value > other.pair[0].value
                else:
                    return self.value > other.value
            return False

        def __eq__(self, other):
            if isinstance(other, Evaluate.Pair):
                return self.pair[0].value == other.pair[0].value \
                       and [x.value for x in self.kicker_cards] == [x.value for x in other.kicker_cards]
            return False

        def GetName(self):
            return f"{self.pair[0].rank} Pair + {''.join([x.rank for x in self.kicker_cards])}"

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
            self.cards = [high]+kicker_cards
            self.high = high
            self.kicker_cards = kicker_cards
            self.value = 1

        def __gt__(self, other):
            if isinstance(other, Evaluate.PokerHand):
                if isinstance(other, Evaluate.High):
                    hand_cards_values = [x.value for x in self.cards]
                    other_cards_values = [x.value for x in other.cards]
                    for i in range(len(self.cards)):
                        if hand_cards_values[i] > other_cards_values[i]:
                            return True
                        elif hand_cards_values[i] < other_cards_values[i]:
                            return False
                    return False
                else:
                    return self.value > other.value
            return False

        def __eq__(self, other):
            if isinstance(other, Evaluate.High):
                return [x.value for x in self.cards] == [x.value for x in other.cards]
            return False

        def __repr__(self):
            return str(self.high)+"+"+"".join([x.display for x in self.kicker_cards])

        def GetName(self):
            return f"{self.high.rank} High + {''.join([x.rank for x in self.kicker_cards])}"

        @staticmethod
        def IsHigh(comm_cards, hand):
            all_cards = sorted(comm_cards.cards+hand.cards, key=lambda x: x.value, reverse=True)
            high = all_cards[0]
            kicker_cards = all_cards[1:5]
            return Evaluate.High(high, kicker_cards)


class Deck:
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
            self.Generate()
        else:
            self.cards = cards

    def __repr__(self):
        return "".join([str(x) for x in self.cards])

    def Generate(self):
        deck = []
        suits = ["h", "d", "s", "c"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        for suit in suits:
            for rank in ranks:
                deck.append(Card(rank + suit))
        self.cards = deck

    def GetCard(self):
        if len(self.cards) == 0:
            raise Exception("Can't get a card, because the deck is empty")
        random_number = random.randint(0, len(self.cards)-1)
        random_card = self.cards[random_number]
        del self.cards[random_number]
        return random_card


def GetRandomCommunityCards(deck):
    cards = []
    for i in range(5):
        cards.append(deck.GetCard())
    comm_cards = CommunityCards(cards)
    return comm_cards


deck = Deck()
comm_cards = GetRandomCommunityCards(deck)
print("Comm: "+str(comm_cards))

hand = Hand([deck.GetCard(), deck.GetCard()])
print("Hand1: "+str(hand))
evaled_hand = hand.Read(comm_cards)
print(evaled_hand.GetName())

hand2 = Hand([deck.GetCard(), deck.GetCard()])
print("Hand2: "+str(hand2))
evaled_hand2 = hand2.Read(comm_cards)
print(evaled_hand2.GetName())

if Evaluate.GetWinnerHands(comm_cards, [hand, hand2]) == [hand, hand2]:
    print("Split Pot")
elif Evaluate.GetWinnerHands(comm_cards, [hand, hand2]) == [hand]:
    print("Hand 1 won!")
else:
    print("Hand 2 won!")
