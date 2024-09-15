import random

def card_value(card):
    value = card[:-1]
    return int(value)

ranks = ('14', '13', '12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2')
suits = ('D', 'H', 'S', 'C') # diamonds, hearts, spades, clubs

combinations_dict = {
    0: "High card",
    1: "One pair",
    2: "Two pair",
    3: "Three of a Kind",
    4: "Straight",
    5: "Flush",
    6: "Full House",
    7: "Four of a Kind",
    8: "Straight Flush",
    9: "Royal Flush"
}



# датасеты для теста
# sorted_cards = ['2D', '4S', '4H', '6S', '7S', '8S', '10S'] # пара
# sorted_cards = ['2D', '4S', '4H', '6S', '11D', '11H', '10S'] # две пары
# sorted_cards = ['2D', '3S', '4H', '6S', '11D', '11H', '11S'] # тройка
# sorted_cards = ['2D', '3S', '4H', '5D', '6D', '11D', '12D'] # стрит
# sorted_cards = ['2D', '3S', '4H', '5D', '6D', '7D', '14D'] # флеш
# sorted_cards = ['3D', '7H', '10S', '11S', '12S', '13S', '14S'] # роял флеш
# sorted_cards = ['2D', '4S', '5S', '6S', '7S', '8S', '10S'] # стрит флеш
# sorted_cards = ['7D', '7S', '7H', '7C', '11D', '11H', '12S'] # каре
# sorted_cards = ['2D', '4S', '4H', '6S', '6D', '6H', '10S'] # фуллхаус


# чекаем стритовые комбинации
def check_straight(cards):
    collector = []
    collector_dict = {}
    combination_power = 0

    # тут проверяем стрит, стрит флеш, роял флеш
    for index, card in enumerate(cards):
        if index > 0 and card_value(card) -1 != card_value(cards[index-1]): # чистим сборщик, если карта меньше предыдущей
            collector = []

        collector.append(card)
        if len(collector) == 5:
            last_symbols = {card[-1] for card in cards} # собираем масти

            if len(last_symbols) != 1: # если масти не одинаковые, но карты по порядку - стрит
                power = 4
                if combination_power < power: combination_power = power
            if card_value(collector[0]) == 11 and len(last_symbols) == 1: # если первая карта - валет залетный и масти одинаковые - роял флеш
                power = 9
                if combination_power < power: combination_power = power
            if card_value(collector[0]) < 11 and len(last_symbols) == 1: # если первая карта меньше валета и масти одинаковые - флеш
                power = 8
                if combination_power < power: combination_power = power
            break
    # проверка флеша
    for card in cards:
        if collector_dict.get(card[-1]) is None:
            collector_dict[card[-1]] = 1
        else:
            collector_dict[card[-1]] = collector_dict.get(card[-1]) + 1
    if sorted(collector_dict.items(), key=lambda item: item[1], reverse=True)[0][1] == 5:
        power = 5
        if combination_power < power:
            collector.clear()
            collector.append(next(iter(collector_dict)))
            combination_power = power

    return combination_power, collector

def check_pair_three_four(cards):
    collector = {}
    combination_power = 0
    # нет комбинаций
    for card in cards:
        if collector.get(card_value(card)) is None:
            collector[card_value(card)] = 1
        else:
            collector[card_value(card)] = collector.get(card_value(card)) + 1


    sorted_collector = sorted(collector.items(), key=lambda item: item[1], reverse=True)

    if sorted_collector[0][1] == 4: # каре
        power = 7
        if combination_power < power: combination_power = power

    if sorted_collector[0][1] == 3: # сет
        power = 3
        if combination_power < power: combination_power = power
        if sorted_collector[1][1] == 2: # фуллхаус
            power = 6
            if combination_power < power: combination_power = power

    if sorted_collector[0][1] == 2: # пара
        if sorted_collector[1][1] == 2: # две пары
            power = 2
            if combination_power < power: combination_power = power
        else:
            power = 1
            if combination_power < power: combination_power = power
    return combination_power, sorted_collector

# AH -> 14H
def convert_symbol_to_numeric(card):
    value = card[:-1]
    suit = card[-1]
    card_values = {
        'A': '14',
        'K': '13',
        'Q': '12',
        'J': '11'
    }

    #  если строка состоит только из цифр
    numeric_value = card_values.get(value, value)

    return f"{numeric_value}{suit}"

# 14H -> A♥ и 11 -> J
def convert_numeric_to_symbol(card):
    # определяем значения карт и масти
    card_values_reverse = {
        '14': 'A',
        '13': 'K',
        '12': 'Q',
        '11': 'J'
    }
    suits_dict = {
        'C': '♣',
        'D': '♦',
        'H': '♥',
        'S': '♠'
    }

    # если строка состоит только из цифр
    if card.isdigit():
        # преобразование значения карт
        card_symbol = card_values_reverse.get(card, card)  # если значение не найдено, оставляем как есть
        return card_symbol

    # если строка состоит из значения и масти
    value = card[:-1]
    suit = card[-1]

    # преобразование значений карт
    card_symbol = card_values_reverse.get(value, value)  # если значение не найдено, оставляем как есть

    # преобразование мастей в символы
    suit_symbol = suits_dict.get(suit, suit)  # если масть не найдена, оставляем как есть

    return f"{card_symbol}{suit_symbol}"


def main():
    while True:
        deck = []
        hand = []
        table = []
        # генерим колоду
        for suit in suits:
            for rank in ranks:
                deck.append(rank + suit)

        # тасуем колоду
        random.shuffle(deck)
        print(f'Select the scenario: \n'
              f'1. Random table and hand \n'
              f'2. Random only table and input hand \n'
              f'3. Random only hand and input table \n'
              f'4. Input table and hand')
        inputed_number = int(input())
        if inputed_number > 1:
            inputed_cards = input('Input cards: ').split(' ')
        else:
            inputed_cards = []

        match inputed_number:
            case 1: # все рандом
                for i in range(2):
                    hand.append(deck.pop())
                for i in range(5):
                    table.append(deck.pop())
            case 2: # рандом стола, рука руками
                for i in inputed_cards:
                    hand.append(convert_symbol_to_numeric(i))
                    deck.remove(convert_symbol_to_numeric(i))
                for i in range(5):
                    table.append(deck.pop())
            case 3: # рандом руки, стол руками
                for i in inputed_cards:
                    table.append(convert_symbol_to_numeric(i))
                    deck.remove(convert_symbol_to_numeric(i))
                for i in range(2):
                    hand.append(deck.pop())
            case 4: # ввод руки и стола
                for i in inputed_cards[:2]:
                    hand.append(convert_symbol_to_numeric(i))
                for i in inputed_cards[2:7]:
                    table.append(convert_symbol_to_numeric(i))
            # case 5:
            #     тут мог бы быть with open /put'/to/tvoi/file.txt as f, но неизвестно какой формат записи в файле
            case _:
                print('Incorrect input. Selected random table and hand')
                for i in range(2):
                    hand.append(deck.pop())
                for i in range(5):
                    table.append(deck.pop())

        # красиво выводим руку
        beautified_hand = ""
        for i in range(2):
            beautified_hand = beautified_hand + ' ' + convert_numeric_to_symbol(hand[i])
        print(f'Your hand:{beautified_hand}')

        # красиво выводим стол
        beautified_table = ""
        for i in range(5):
            beautified_table = beautified_table + ' ' + convert_numeric_to_symbol(table[i])
        print(f'Table:{beautified_table}')

        # собираем карты с руки и со стола
        for i in hand:
            table.append(i)
        sorted_cards = sorted(table, key=card_value)  # сортируем все карты, которые в игре

        #print(f'Sorted table {sorted_cards}') # для дебага

        combination_power1, cards1 = check_straight(sorted_cards)
        combination_power2, cards2 = check_pair_three_four(sorted_cards)
        #print(f'Combination power: {combination_power1} | {combination_power2}') # для дебага
        color_start = "\033[32m"
        color_end = "\033[0m"
        if combination_power1 >= combination_power2:
            if combination_power1 == 0:
                print(f'No combination ;( High card {convert_numeric_to_symbol(sorted_cards[-1])}')
            elif combination_power1 == 5:
                print(f'{color_start}Congratulations! Combination: {combinations_dict.get(combination_power1)} of {convert_numeric_to_symbol(cards1[0])}{color_end}')
            else:
                print(f'{color_start}Congratulations! Combination: {combinations_dict.get(combination_power1)} from {convert_numeric_to_symbol(cards1[0])} to {convert_numeric_to_symbol(cards1[-1])}{color_end}')
        else:
            if combination_power2 in [0, 1, 3, 7]:
                print(f'{color_start}Congratulations! Combination: {combinations_dict.get(combination_power2)} of {convert_numeric_to_symbol(str(cards2[0][0]))}{color_end}')
            else:
                print(f'{color_start}Congratulations! Combination: {combinations_dict.get(combination_power2)} of {convert_numeric_to_symbol(str(cards2[0][0]))} and {convert_numeric_to_symbol(str(cards2[1][0]))}{color_end}')
        print('='*20)


if __name__ == '__main__':
    main()