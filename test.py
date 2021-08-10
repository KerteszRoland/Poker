import unittest
import main


def GetDeck():
    deck = []
    suits = ["h", "d", "s", "c"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    for suit in suits:
        for rank in ranks:
            deck.append(rank + suit)
    return deck


def GetCardsByStr(str_list):
    return [main.Card(x) for x in str_list]


def GetCommCardsByStr(str_list):
    return main.CommunityCards(GetCardsByStr(str_list))


def GetHandByStr(str_list):
    return main.Hand(GetCardsByStr(str_list))


def IsFlushCorrect(flush, flush_str, suit):
    return type(flush) is main.Evaluate.Flush and str(flush) == flush_str and str(flush.suit) == suit


def IsStraightCorrect(straight, straight_str, high):
    return type(straight) is main.Evaluate.Straight and str(straight) == straight_str and str(straight.high) == high


class TestCard(unittest.TestCase):

    def test_two_instances_are_equal(self):
        card1 = main.Card("As")
        card2 = main.Card("As")
        self.assertEqual(card1, card2)

    def test_value(self):
        cards = GetDeck()[:13]
        values = []
        for card_str in cards:
            card = main.Card(card_str)
            values.append(card.value)
        correct_values = list(range(2, 15))
        self.assertEqual(values, correct_values)

    def test_rank(self):
        cards = GetDeck()[:13]
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
        correct_suits = list("s" * 3) + list("c" * 3) + list("d" * 3) + list("h" * 3)
        self.assertEqual(suits, correct_suits)

    def test_display(self):
        cards = GetDeck()[:13]
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

    def test_cannot_init_without_rank(self):
        with self.assertRaises(main.PokerExceptions.IncorrectCardString):
            main.Card("c")

    def test_cannot_init_without_suit(self):
        with self.assertRaises(main.PokerExceptions.IncorrectCardString):
            main.Card("A")

    def test_cannot_init_with_null_string(self):
        with self.assertRaises(main.PokerExceptions.IncorrectCardString):
            main.Card("")

    def test_cannot_init_with_incorrect_suit(self):
        with self.assertRaises(main.PokerExceptions.IncorrectSuit):
            main.Card("Aq")

    def test_cannot_init_with_incorrect_rank(self):
        with self.assertRaises(main.PokerExceptions.IncorrectRank):
            main.Card("Xs")


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
        hand = main.Hand([main.Card("Js"), main.Card("Qc"), main.Card("Kd"), main.Card("Ah")])
        self.assertEqual(str(hand), "JsQcKdAh")


class TestCommunityCards(unittest.TestCase):

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
        comm_cards = main.CommunityCards(flop)
        self.assertEqual(comm_cards.GetFlop(), flop)

    def test_get_turn(self):
        cards = [main.Card("2s"), main.Card("7h"), main.Card("8c")]
        turn_card = main.Card("Ad")
        cards.append(turn_card)
        comm_cards = main.CommunityCards(cards)
        self.assertEqual(comm_cards.GetTurn(), turn_card)

    def test_get_river(self):
        cards = [main.Card("2s"), main.Card("7h"), main.Card("8c"), main.Card("Ad")]
        river_card = main.Card("Jc")
        cards.append(river_card)
        comm_cards = main.CommunityCards(cards)
        self.assertEqual(comm_cards.GetRiver(), river_card)

    def test_push_flop(self):
        flop = [main.Card("10h"), main.Card("Jh"), main.Card("Qh")]
        comm_cards = main.CommunityCards()
        comm_cards.PushFlop(flop)
        self.assertEqual(comm_cards.cards, flop)

    def test_push_turn(self):
        turn_card = main.Card("Ad")
        flop_cards = [main.Card("2s"), main.Card("7h"), main.Card("8c")]
        comm_cards = main.CommunityCards(flop_cards)
        comm_cards.PushTurn(turn_card)
        updated_comm_cards = flop_cards
        updated_comm_cards.append(turn_card)
        self.assertEqual(comm_cards.cards, updated_comm_cards)

    def test_push_river(self):
        cards = [main.Card("2s"), main.Card("7h"), main.Card("8c"), main.Card("Ad")]
        river_card = main.Card("Jc")
        comm_cards = main.CommunityCards(cards)
        comm_cards.PushRiver(river_card)
        updated_comm_cards = cards
        updated_comm_cards.append(river_card)
        self.assertEqual(comm_cards.cards, updated_comm_cards)

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

    def test_cannot_push_non_card_turn(self):
        with self.assertRaises(TypeError):
            flop_cards = [main.Card("2s"), main.Card("7h"), main.Card("8c")]
            comm_cards = main.CommunityCards(flop_cards)
            comm_cards.PushTurn(5)

    def test_cannot_push_non_card_river(self):
        with self.assertRaises(TypeError):
            cards = [main.Card("2s"), main.Card("7h"), main.Card("8c"), main.Card("5h")]
            comm_cards = main.CommunityCards(cards)
            comm_cards.PushRiver(9)

    def test_cannot_push_flop_multiple_times(self):
        with self.assertRaises(Exception):
            flop = [main.Card("10h"), main.Card("Jh"), main.Card("Qh")]
            comm_cards = main.CommunityCards()
            comm_cards.PushFlop(flop)
            comm_cards.PushFlop(flop)

    def test_cannot_push_turn_multiple_times(self):
        with self.assertRaises(Exception):
            turn_card = main.Card("Ad")
            flop_cards = [main.Card("2s"), main.Card("7h"), main.Card("8c")]
            comm_cards = main.CommunityCards(flop_cards)
            comm_cards.PushTurn(turn_card)
            comm_cards.PushTurn(turn_card)

    def test_cannot_push_river_multiple_times(self):
        with self.assertRaises(Exception):
            cards = [main.Card("2s"), main.Card("7h"), main.Card("8c"), main.Card("Ad")]
            river_card = main.Card("Qc")
            comm_cards = main.CommunityCards(cards)
            comm_cards.PushRiver(river_card)
            comm_cards.PushRiver(river_card)

    def test_cannot_push_turn_before_flop(self):
        with self.assertRaises(Exception):
            comm_cards = main.CommunityCards()
            comm_cards.PushTurn(main.Card("Ad"))

    def test_cannot_push_river_before_flop(self):
        with self.assertRaises(Exception):
            comm_cards = main.CommunityCards()
            comm_cards.PushRiver(main.Card("Ah"))

    def test_cannot_push_river_before_turn(self):
        with self.assertRaises(Exception):
            flop_cards = [main.Card("2s"), main.Card("7h"), main.Card("8c")]
            river_card = main.Card("Qc")
            comm_cards = main.CommunityCards(flop_cards)
            comm_cards.PushRiver(river_card)

    def test_get_suits(self):
        cards = [main.Card("Ad"), main.Card("Qc"), main.Card("Kh"),
                 main.Card("5s"), main.Card("10c")]
        comm_cards = main.CommunityCards(cards)
        suits = comm_cards.GetSuits()
        correct_suits = [main.Suit.DIAMOND, main.Suit.CLUB, main.Suit.HEART,
                         main.Suit.SPADE, main.Suit.CLUB]
        self.assertEqual(suits, correct_suits)


class TestHandRead(unittest.TestCase):

    def test_read_flush(self):
        comm_cards = GetCommCardsByStr(["2s", "7c", "8c", "Jc", "Ah"])
        myhand = GetHandByStr(["Kc", "Qc"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(IsFlushCorrect(temp, "KcQcJc8c7c", main.Suit.CLUB))

    def test_read_non_flush(self):
        comm_cards = GetCommCardsByStr(["2s", "7c", "8c", "Jc", "Qh"])
        myhand = GetHandByStr(["Ac", "4d"])
        temp = myhand.Read(comm_cards)
        self.assertEqual(type(temp), main.Evaluate.High)

    def test_read_straight_wheel(self):
        comm_cards = GetCommCardsByStr(["2s", "3c", "8d", "5c", "Ah"])
        myhand = GetHandByStr(["Ac", "4d"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(IsStraightCorrect(temp, "Ah2s3c4d5c", "5c"))

    def test_read_straight_wheel_with_duplicates(self):
        comm_cards = GetCommCardsByStr(["2s", "3c", "2d", "Ad", "5h"])
        myhand = GetHandByStr(["Ac", "4d"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(IsStraightCorrect(temp, "Ad2s3c4d5h", "5h"))

    def test_read_non_straight_wheel(self):
        comm_cards = GetCommCardsByStr(["2s", "3c", "8d", "Kc", "Jh"])
        myhand = GetHandByStr(["Ac", "4d"])
        temp = myhand.Read(comm_cards)
        self.assertEqual(type(temp), main.Evaluate.High)

    def test_read_non_straight(self):
        comm_cards = GetCommCardsByStr(["2s", "Qs", "8d", "Kc", "Jh"])
        myhand = GetHandByStr(["Ac", "4d"])
        temp = myhand.Read(comm_cards)
        self.assertEqual(type(temp), main.Evaluate.High)

    def test_read_straight_bottom(self):
        comm_cards = GetCommCardsByStr(["5s", "Qs", "8d", "Kc", "9h"])
        myhand = GetHandByStr(["6c", "7d"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(IsStraightCorrect(temp, "9h8d7d6c5s", "9h"))

    def test_read_straight_middle(self):
        comm_cards = GetCommCardsByStr(["2s", "9s", "8d", "10c", "Ah"])
        myhand = GetHandByStr(["6c", "7d"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(IsStraightCorrect(temp, "10c9s8d7d6c", "10c"))

    def test_read_straight_top(self):
        comm_cards = GetCommCardsByStr(["2s", "3h", "10s", "9d", "6c"])
        myhand = GetHandByStr(["7c", "8d"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(IsStraightCorrect(temp, "10s9d8d7c6c", "10s"))

    def test_read_wheel_on_straight(self):
        comm_cards = GetCommCardsByStr(["2s", "4s", "5d", "6c", "7h"])
        myhand = GetHandByStr(["Ac", "3d"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(IsStraightCorrect(temp, "7h6c5d4s3d", "7h"))

    def test_read_straight_broadway(self):
        comm_cards = GetCommCardsByStr(["As", "4s", "5d", "Kc", "Qh"])
        myhand = GetHandByStr(["Jc", "10d"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(IsStraightCorrect(temp, "AsKcQhJc10d", "As"))

    def test_read_straight_on_comm(self):
        comm_cards = GetCommCardsByStr(["5h", "6s", "7d", "8c", "9h"])
        myhand = GetHandByStr(["2c", "2d"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(IsStraightCorrect(temp, "9h8c7d6s5h", "9h"))

    def test_read_flush_over_straight(self):
        comm_cards = GetCommCardsByStr(["5c", "6c", "7d", "8c", "9h"])
        myhand = GetHandByStr(["Ac", "Kc"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(IsFlushCorrect(temp, "AcKc8c6c5c", main.Suit.CLUB))

    def test_read_quads(self):
        comm_cards = GetCommCardsByStr(["Ac", "As", "Kd", "8c", "9h"])
        myhand = GetHandByStr(["Ah", "Ad"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(type(temp) == main.Evaluate.Quads and str(temp) == "AcAsAhAd+Kd")

    def test_read_threeofkind(self):
        comm_cards = GetCommCardsByStr(["Ac", "As", "Kd", "8c", "9h"])
        myhand = GetHandByStr(["Ah", "2d"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(type(temp) == main.Evaluate.ThreeOfKind and str(temp) == "AcAsAh+Kd9h")

    def test_read_fullhouse(self):
        comm_cards = GetCommCardsByStr(["Ac", "As", "Kd", "8c", "9h"])
        myhand = GetHandByStr(["Ah", "Kc"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(type(temp) == main.Evaluate.FullHouse and str(temp) == "AcAsAhKdKc")

    def test_read_twopair(self):
        comm_cards = GetCommCardsByStr(["Ac", "Js", "Kd", "8c", "9h"])
        myhand = GetHandByStr(["Ah", "Kc"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(type(temp) == main.Evaluate.TwoPair and str(temp) == "AcAhKdKc+Js")

    def test_read_pair(self):
        comm_cards = GetCommCardsByStr(["Ac", "Js", "Kd", "8c", "9h"])
        myhand = GetHandByStr(["Ah", "Qc"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(type(temp) == main.Evaluate.Pair and str(temp) == "AcAh+KdQcJs")

    def test_read_high(self):
        comm_cards = GetCommCardsByStr(["2c", "Js", "Kd", "8c", "9h"])
        myhand = GetHandByStr(["Ah", "Qc"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(type(temp) == main.Evaluate.High and str(temp) == "Ah+KdQcJs9h")

    def test_read_straightflush(self):
        comm_cards = GetCommCardsByStr(["5c", "6c", "7c", "2c", "Ac"])
        myhand = GetHandByStr(["8c", "9c"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(type(temp) == main.Evaluate.StraightFlush and str(temp) == "9c8c7c6c5c")

    def test_read_royalflush(self):
        comm_cards = GetCommCardsByStr(["5c", "6c", "10c", "Jc", "Qc"])
        myhand = GetHandByStr(["Ac", "Kc"])
        temp = myhand.Read(comm_cards)
        self.assertTrue(type(temp) == main.Evaluate.RoyalFlush and str(temp) == "AcKcQcJc10c")


class TestDeck(unittest.TestCase):
    def test_empty_deck(self):
        deck = main.Deck([])
        self.assertTrue(deck.cards == [])

    def test_generate_deck(self):
        deck = main.Deck([])
        deck.Generate()
        is_correct = len(deck.cards) == 52 and type(deck.cards[0]) is main.Card
        self.assertTrue(is_correct)

    def test_str(self):
        deck = main.Deck()
        self.assertEqual(str(deck),
                         "2h3h4h5h6h7h8h9h10hJhQhKhAh2d3d4d5d6d7d8d9d10dJdQdKdAd" +
                         "2s3s4s5s6s7s8s9s10sJsQsKsAs2c3c4c5c6c7c8c9c10cJcQcKcAc")

    def test_get_card(self):
        deck = main.Deck()
        card = deck.GetCard()
        is_correct = card not in deck.cards and type(card) is main.Card
        self.assertTrue(is_correct)

    def test_get_all_the_cards(self):
        deck = main.Deck()
        cards = []
        for i in range(52):
            cards.append(deck.GetCard())
        is_correct = deck.cards == [] and len(cards) == 52
        self.assertTrue(is_correct)

    def test_cannot_get_card_from_an_empty_deck(self):
        with self.assertRaises(Exception):
            deck = main.Deck([])
            deck.GetCard()


class TestHandvsHand(unittest.TestCase):

    def test_high_eq_2hand(self):
        comm_cards = GetCommCardsByStr(["6d", "7c", "9d", "10h", "Jh"])
        myhand = GetHandByStr(["As", "Kc"])
        herhand = GetHandByStr(["Ah", "Ks"])
        my = myhand.Read(comm_cards)
        her = herhand.Read(comm_cards)
        self.assertEqual(my, her)

    def test_high_card(self):
        comm_cards = GetCommCardsByStr(["6d", "7c", "9d", "10h", "Jh"])
        myhand = GetHandByStr(["As", "Qc"])
        herhand = GetHandByStr(["Ah", "Ks"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [herhand])

    def test_high_card_chop(self):
        comm_cards = GetCommCardsByStr(["6d", "7c", "9d", "10h", "Jh"])
        myhand = GetHandByStr(["As", "2c"])
        herhand = GetHandByStr(["Ah", "3s"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [myhand, herhand])

    def test_pair(self):
        comm_cards = GetCommCardsByStr(["Ad", "7c", "9d", "Kh", "Jh"])
        myhand = GetHandByStr(["As", "8c"])
        herhand = GetHandByStr(["Ah", "Qs"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [herhand])

    def test_pair_chop(self):
        comm_cards = GetCommCardsByStr(["Ad", "7c", "9d", "Kh", "Jh"])
        myhand = GetHandByStr(["As", "2c"])
        herhand = GetHandByStr(["Ah", "3s"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [myhand, herhand])

    def test_twopair(self):
        comm_cards = GetCommCardsByStr(["Ad", "2c", "9d", "Kh", "2h"])
        myhand = GetHandByStr(["As", "9c"])
        herhand = GetHandByStr(["Ah", "Ks"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [herhand])

    def test_twopair_chop(self):
        comm_cards = GetCommCardsByStr(["Ad", "7c", "9d", "Kh", "Jh"])
        myhand = GetHandByStr(["As", "Kc"])
        herhand = GetHandByStr(["Ah", "Ks"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [myhand, herhand])

    def test_threeofkind(self):
        comm_cards = GetCommCardsByStr(["Ad", "Ac", "3d", "Kh", "2h"])
        myhand = GetHandByStr(["As", "4c"])
        herhand = GetHandByStr(["Ah", "5s"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [herhand])

    def test_threeofkind_chop(self):
        comm_cards = GetCommCardsByStr(["Ad", "Ac", "9d", "Kh", "10h"])
        myhand = GetHandByStr(["As", "3c"])
        herhand = GetHandByStr(["Ah", "4s"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [myhand, herhand])

    def test_straight(self):
        comm_cards = GetCommCardsByStr(["Qd", "Jc", "9d", "2h", "10h"])
        myhand = GetHandByStr(["8s", "8c"])
        herhand = GetHandByStr(["Ah", "Ks"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [herhand])

    def test_straight_chop(self):
        comm_cards = GetCommCardsByStr(["Qd", "Jc", "9d", "Kh", "10h"])
        myhand = GetHandByStr(["As", "3c"])
        herhand = GetHandByStr(["Ah", "4s"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [myhand, herhand])

    def test_flush(self):
        comm_cards = GetCommCardsByStr(["Qc", "Jc", "9d", "2c", "10h"])
        myhand = GetHandByStr(["9c", "8c"])
        herhand = GetHandByStr(["Ac", "3c"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [herhand])

    def test_flush_eq(self):
        comm_cards = GetCommCardsByStr(["2c", "Qc", "9c", "7c", "4c"])
        myhand = GetHandByStr(["Jd", "3d"])
        herhand = GetHandByStr(["Kd", "4d"])
        self.assertTrue(myhand.Read(comm_cards) == herhand.Read(comm_cards))

    def test_flush_not_eq(self):
        comm_cards = GetCommCardsByStr(["Qc", "Jc", "9d", "2c", "10h"])
        myhand = GetHandByStr(["9c", "8c"])
        herhand = GetHandByStr(["10c", "3c"])
        self.assertFalse(myhand.Read(comm_cards) == herhand.Read(comm_cards))

    def test_flush_chop(self):
        comm_cards = GetCommCardsByStr(["2c", "Qc", "9c", "7c", "4c"])
        myhand = GetHandByStr(["Jd", "3d"])
        herhand = GetHandByStr(["Kd", "4d"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [myhand, herhand])

    def test_fullhouse(self):
        comm_cards = GetCommCardsByStr(["Kc", "Ad", "Ah", "As", "Qc"])
        myhand = GetHandByStr(["Qd", "3s"])
        herhand = GetHandByStr(["Kh", "2h"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [herhand])

    def test_fullhouse_chop(self):
        comm_cards = GetCommCardsByStr(["Kc", "Ad", "Ah", "As", "4c"])
        myhand = GetHandByStr(["Kh", "3s"])
        herhand = GetHandByStr(["Kd", "2h"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [myhand, herhand])

    def test_quads(self):
        comm_cards = GetCommCardsByStr(["Kc", "Ad", "Ah", "As", "Qc"])
        myhand = GetHandByStr(["Ks", "3s"])
        herhand = GetHandByStr(["Ac", "2h"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [herhand])

    def test_quads_chop(self):
        comm_cards = GetCommCardsByStr(["Kc", "Kd", "Kh", "Ks", "4c"])
        myhand = GetHandByStr(["Ah", "3s"])
        herhand = GetHandByStr(["Ad", "2h"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [myhand, herhand])

    def test_straightflush(self):
        comm_cards = GetCommCardsByStr(["5c", "6c", "7c", "8c", "9c"])
        myhand = GetHandByStr(["Kc", "4c"])
        herhand = GetHandByStr(["Ac", "10c"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [herhand])

    def test_straightflush_eq(self):
        comm_cards = GetCommCardsByStr(["5c", "6c", "7c", "8c", "9c"])
        myhand = GetHandByStr(["Kc", "4d"])
        herhand = GetHandByStr(["Ac", "10d"])
        self.assertTrue(myhand.Read(comm_cards) == herhand.Read(comm_cards))

    def test_straightflush_not_eq(self):
        comm_cards = GetCommCardsByStr(["5c", "6c", "7c", "8c", "9c"])
        myhand = GetHandByStr(["Kc", "4c"])
        herhand = GetHandByStr(["Ac", "10c"])
        self.assertFalse(myhand.Read(comm_cards) == herhand.Read(comm_cards))

    def test_straightflush_chop(self):
        comm_cards = GetCommCardsByStr(["5c", "6c", "7c", "8c", "9c"])
        myhand = GetHandByStr(["Kd", "4d"])
        herhand = GetHandByStr(["Ad", "10d"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [myhand, herhand])

    def test_royalflush(self):
        comm_cards = GetCommCardsByStr(["10c", "Jc", "Qc", "Kc", "2d"])
        myhand = GetHandByStr(["Kd", "4c"])
        herhand = GetHandByStr(["Ac", "10s"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [herhand])

    def test_royalflush_chop(self):
        comm_cards = GetCommCardsByStr(["10c", "Jc", "Qc", "Kc", "Ac"])
        myhand = GetHandByStr(["Kd", "4d"])
        herhand = GetHandByStr(["Ad", "10d"])
        self.assertEqual(main.Evaluate.GetWinnerHands(comm_cards, [myhand, herhand]), [myhand, herhand])


if __name__ == "__main__":
    unittest.main()
