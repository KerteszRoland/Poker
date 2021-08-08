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
        flush = ev.Flush.IsFlush(comm_cards, self)
        straight = ev.Straight.IsStraight(comm_cards, self)
        if flush:
            return flush
        elif straight:
            return straight
        else:
            return None


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
                    cards_in_flush = [x for x in all_cards if x.suit == suit]
                    high = sorted(cards_in_flush, key=lambda card: card.value)[-1]
                    return Evaluate.Flush(cards_in_flush, high)
            return False

    class Straight(PokerHand):
        def __init__(self, cards, high):
            self.cards = cards
            self.high = high

        @staticmethod
        def IsStraight(comm_cards, hand):
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
