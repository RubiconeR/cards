from __future__ import annotations
import random
import time

VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS_UNI = {
    'Spades': '♠',
    'Clubs': '♣',
    'Diamonds': '♦',
    'Hearts': '♥'
}
WAIT_TIME = 1


class Card:
    def __init__(self, value, suit):
        if value not in VALUES:
            raise ValueError("Wrong card value")
        if suit not in SUITS_UNI:
            raise ValueError("Wrong card suit")
        self.value = value  # Значение карты(2, 3... 10, J, Q, K, A)
        self.suit = SUITS_UNI[suit]  # Масть карты

    def __repr__(self):
        return f"{self.value}{self.suit}"

    def __eq__(self, other_card: Card):
        if type(other_card) != Card:
            raise TypeError(f"Expected Card, not {type(other_card)}")
        if self.suit == other_card.suit:
            return True

    def __gt__(self, other_card: Card):
        if type(other_card) != Card:
            raise TypeError(f"Expected Card, not {type(other_card)}")
        # print(f"Val:{self.value}, Index:{VALUES.index(self.value)}> Val:{other_card.value}, Index:{VALUES.index(other_card.value)}")#DEBUG
        if self == other_card:
            return VALUES.index(self.value) > VALUES.index(other_card.value)
        if self.suit == trump:
            return True
        if other_card.suit == trump:
            return False
        raise AttributeError(f"Can't compare cards {self} {other_card}")

    def __lt__(self, other_card: Card):
        return not self > other_card


# Задание: Теперь создадим колоду из 52-ух карт и реализуем все методы
class Deck:
    def __init__(self):
        # Список карт в колоде. Каждым элементом списка будет объект класса Card
        self.cards = []
        for suit in SUITS_UNI:
            for value in VALUES:
                self.cards.append(Card(value, suit))

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return f"cards[{len(self.cards)}] {self.cards}"

    def draw(self, x: int):
        if type(x) != int:
            raise TypeError("Invalid type")
        pick_up = self.cards[:x]
        self.cards = self.cards[x:]
        return pick_up

    def shuffle(self):
        random.shuffle(self.cards)

    def __getitem__(self, index: int):
        if type(index) != int:
            raise TypeError("Invalid type index")
        return self.cards[index]

    def pop(self,index:int):
        if type(index) != int:
            raise TypeError("Invalid type index")
        return self.cards.pop(index)


class Player(Deck):
    def sort(self):
        # count=0
        new_cards = []
        trump_cards = []
        for val in VALUES:
            for card in self.cards:
                # count+=1
                if card.value == val:
                    if card.suit == trump:
                        trump_cards.append(card)
                    else:
                        new_cards.append(card)
        # print(count)
        self.cards = new_cards + trump_cards

    def __init__(self, deck: Deck, name: str):
        self.turn = False
        self.name = name
        self.cards = deck.draw(10)
        self.sort()

    def to_ten(self, deck: Deck):
        if len(self) > 10:
            return
        if 10 - len(self) <= len(deck):
            self.cards += deck.draw(10 - len(self))
        else:
            self.cards += deck.draw(len(deck.cards))
        self.sort()

    def move(self) -> Card:
        return self.draw(1)[0]

    def take(self, on_table: list):
        self.cards += on_table
        self.sort()

    def find_defend(self, card: Card) -> Card:
        for hand_card in range(len(self.cards)):
            try:
                self[hand_card] > card
            except AttributeError:
                continue
            else:
                if self[hand_card] > card:
                    return self.pop(hand_card)

    def find_throw_up(self, on_table: list) -> Card:
        for table_card in on_table:
            for hand_card in range(len(self.cards)):
                if self[hand_card].value == table_card.value:
                    return self.pop(hand_card)


def show_table(on_table: list):
    switch = True
    output = ""
    for card in on_table:
        if switch:
            output += str(card)
        else:
            output += "<-" + str(card) + " "
        switch = not switch
    print(output)


if __name__ == '__main__':
    on_table = []
    deck = Deck()
    deck.shuffle()
    trump = [SUITS_UNI[i] for i in SUITS_UNI]
    trump = random.choice(trump)
    # trump='Diamonds'
    # card1=Card('2',trump)
    # card2=Card('4','Hearts')
    # trump=SUITS_UNI[trump]
    # print(f"{card1} {card2} {card1 > card2}")
    player1 = Player(deck, "Player 1")
    player2 = Player(deck, "Player 2")
    player1.turn = random.randint(0, 1)
    player2.turn = not player1.turn
    round_count=0
    while len(player1.cards) > 0 and len(player2.cards) > 0:
        round_count += 1
        print(f"\n{'=' * 20}РАУНД {round_count}{'=' * 20}\n")
        print(f"Козырь:{trump}")
        print("Remain cards in deck:", len(deck))
        print(f"\nPlayer1 {player1}\nPlayer2 {player2}\n")
        time.sleep(WAIT_TIME)
        if player1.turn:
            attacker = player1
            defender = player2
        else:
            attacker = player2
            defender = player1
        print(f"{attacker.name} ХОДИТ")
        time.sleep(WAIT_TIME)
        on_table.append(attacker.move())
        print(f"{attacker.name} сходил {on_table[0]}")
        show_table(on_table)
        time.sleep(WAIT_TIME)
        while True:
            # print(f"\nPlayer1 {player1}\nPlayer2 {player2}\n")  # DEBUG
            def_card = defender.find_defend(on_table[len(on_table) - 1])
            # print("Номер выбранной",def_card)#DEBUG
            draw = False
            if not def_card is None:
                on_table.append(def_card)
                print(f"{defender.name} отбивается {on_table[len(on_table) - 1]}")
                # print(f"\nPlayer1 {player1}\nPlayer2 {player2}\n")  # DEBUG
                show_table(on_table)
                time.sleep(WAIT_TIME)
                throw_card = attacker.find_throw_up(on_table)
                if not throw_card is None:
                    on_table.append(throw_card)
                    print(f"{attacker.name} подкинул {on_table[len(on_table) - 1]}")
                    show_table(on_table)
                    time.sleep(WAIT_TIME)
                    # print(f"\nPlayer1 {player1}\nPlayer2 {player2}\n")  # DEBUG
                else:
                    draw = True
                    break
            else:
                break
        if draw:
            print("Бито")
            on_table = []
            attacker.turn = False
            defender.turn = True
        else:
            while True:
                card = attacker.find_throw_up(on_table)
                if card is None:
                    break
                on_table.append(card)
                print(f"{attacker.name} подкинул {on_table[len(on_table) - 1]}")
                time.sleep(WAIT_TIME)
            defender.take(on_table)
            print(f"{defender.name} взял")
            time.sleep(WAIT_TIME)
            on_table = []
        print(f"\nPlayer1 {player1}\nPlayer2 {player2}\n")
        time.sleep(WAIT_TIME + 3)
        attacker.to_ten(deck)
        defender.to_ten(deck)
    if len(player1) == 0:
        print("Player1 ВЫИГРАЛ!!!")
    else:
        print("Player2 ВЫИГРАЛ!!!")

'''
создадим имитацию ходов в “Дурака без козырей”:

1. Создайте колоду из 52 карт. Перемешайте ее.
2. Первый игрок берет сверху 10 карт
3. Второй игрок берет сверху 10 карт.
4. Игрок-1 ходит:
    4.1. игрок-1 выкладывает самую маленькую карту по значению
    4.2. игрок-2 пытается бить карту, если у него есть такая же масть, но значением больше.
    4.3. Если игрок-2 не может побить карту, то он проигрывает/забирает себе(см. пункт 7)
    4.4. Если игрок-2 бьет карту, то игрок-1 может подкинуть карту любого значения, которое есть на столе.
5. Если Игрок-2 отбился, то Игрок-1 и Игрок-2 меняются местами. Игрок-2 ходит, Игрок-1 отбивается.    
6. Выведите в консоль максимально наглядную визуализацию данных ходов.
7* Реализовать возможность добрать карты из колоды после того, как один из игроков отбился/взял в руку
'''