import unittest
import main


def GetDeck():
    deck = [] 
    suits = ["h", "d", "s", "c"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    for suit in suits:
        for rank in ranks:
            deck.append(rank+suit)
    return deck
    
    
DECK = GetDeck()


class TestCard(unittest.TestCase):

    def test_two_instances_are_equal(self):
        card1 = main.Card("As")
        card2 = main.Card("As")
        self.assertEqual(card1, card2)

    def test_value(self):
        cards = DECK[:13]
        values = []
        for card_str in cards:
            card = main.Card(card_str)
            values.append(card.value)
        correct_values = list(range(2, 15))
        self.assertEqual(values, correct_values)

    def test_rank(self):
        cards = DECK[:13]
        ranks = []
        for card_str in cards:
            card = main.Card(card_str)
            ranks.append(card.rank)
        correct_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.assertEqual(ranks, correct_ranks)

    def test_suit(self):
        cards = ["8s", "10s", "As", "8c", "10c", "Ac", "8d", "10d", "Ad", "8h", "10h", "Ah"]
        suits = []
        for card_str in cards:
            card = main.Card(card_str)
            suits.append(card.suit)
        correct_suits = list("s"*3)+list("c"*3)+list("d"*3)+list("h"*3)
        self.assertEqual(suits, correct_suits)

    def test_display(self):
        cards = DECK[:13]
        displays = []
        for card_str in cards:
            card = main.Card(card_str)
            displays.append(card.display)
        correct_displays = cards
        self.assertEqual(displays, correct_displays)

    def test_init_capital_suit(self):
        card_str = "AH"
        card = main.Card(card_str)
        self.assertTrue(card.suit == "h")

    def test_init_lower_rank(self):
        card_str = "kc"
        card = main.Card(card_str)
        self.assertTrue(card.rank == "K")

    def test_init_lower_rank_capital_suit(self):
        card_str = "jD"
        card = main.Card(card_str)
        self.assertTrue(card.rank == "J" and card.suit == "d")
        

class TestHand(unittest.TestCase):
   
    def test_str_empty(self):
        hand = main.Hand()
        self.assertEqual(str(hand), "")

    def test_str_one_card(self):
        card1 = main.Card("Qc")
        hand = main.Hand([card1])
        self.assertEqual(str(hand), "Qc")

    def test_str_two_card(self):
        card1 = main.Card("Kd")
        card2 = main.Card("Js")
        hand = main.Hand([card1, card2])
        self.assertEqual(str(hand), "KdJs")

    def test_str_four_card(self):
        card1 = main.Card("Js")
        card2 = main.Card("Qc")
        card3 = main.Card("Kd")
        card4 = main.Card("Ah")
        hand = main.Hand([card1, card2, card3, card4])
        self.assertEqual(str(hand), "JsQcKdAh")


class CommunityCards(unittest.TestCase):
    
    def test_init_empty(self):
        comm_cards = main.CommunityCards()
        self.assertTrue(len(comm_cards.cards) == 0)

    def test_str_empty(self):
        comm_cards = main.CommunityCards()
        self.assertEqual(str(comm_cards), "")

    def test_get_flop_before_pushing(self):
        comm_cards = main.CommunityCards()
        self.assertEqual(comm_cards.GetFlop(), None)

    def test_get_turn_before_pushing(self):
        comm_cards = main.CommunityCards()
        self.assertEqual(comm_cards.GetTurn(), None)

    def test_get_river_before_pushing(self):
        comm_cards = main.CommunityCards()
        self.assertEqual(comm_cards.GetRiver(), None)

    def test_get_flop(self):
        flop = [main.Card("2h"), main.Card("3h"), main.Card("4h")]
        comm_cards = main.CommunityCards()
        comm_cards.PushFlop(flop)
        self.assertEqual(comm_cards.GetFlop(), flop)

    def test_push_flop(self):
        card1 = main.Card("10h")
        card2 = main.Card("Jh")
        card3 = main.Card("Qh")
        flop = [card1, card2, card3]
        comm_cards = main.CommunityCards()
        comm_cards.PushFlop(flop)
        self.assertEqual(comm_cards.cards, flop)
    
    def test_cannot_push_empty_flop(self):
        with self.assertRaises(AttributeError):
            flop = []
            comm_cards = main.CommunityCards()
            comm_cards.PushFlop(flop)

    def test_cannot_push_non_card_flop(self):
        with self.assertRaises(AttributeError):
            flop = [1, 2, 3]
            comm_cards = main.CommunityCards()
            comm_cards.PushFlop(flop)

    def test_cannot_push_flop_multiple_times(self):
        with self.assertRaises(Exception):
            card1 = main.Card("10h")
            card2 = main.Card("Jh")
            card3 = main.Card("Qh")
            flop = [card1, card2, card3]
            comm_cards = main.CommunityCards()
            comm_cards.PushFlop(flop)
            comm_cards.PushFlop(flop)

    def test_push_turn(self):
        turn_card = main.Card("Ad")
        flop_cards = [main.Card("2s"), main.Card("7h"), main.Card("8c")]
        comm_cards = main.CommunityCards()
        comm_cards.PushFlop(flop_cards)
        comm_cards.PushTurn(turn_card)
        updated_comm_cards = flop_cards
        updated_comm_cards.append(turn_card)
        self.assertEqual(comm_cards.cards, updated_comm_cards)


if __name__ == "__main__":
    unittest.main()
