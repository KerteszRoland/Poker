

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
