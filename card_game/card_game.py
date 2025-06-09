from random import shuffle

def create_deck():
    suits = ("♣️", "♦️", "❤️", "♠️")
    values = ("A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2")
    deck = [value + suit for value in values for suit in suits] * 4
    shuffle(deck)
    return deck

def deal_cards(names, deck):
    current_deck = deck.copy()
    # print(f"დასაწყისი: დასტა შეიცავს {len(current_deck)} კარტს")
    player_cards = {}
    for player in names:
        dealt_cards = [current_deck.pop() for _ in range(5)]
        player_cards[player] = dealt_cards
    # print(f"ბოლო: დასტა შეიცავს {len(current_deck)} კარტს")
    
    return player_cards

def card_value(card):
    val = card[:-2]
    if val.isdigit(): return int(val)
    if val == 'J': return 11
    if val == 'Q': return 12
    if val == 'K': return 13
    if val == 'A': return 20

def count_same_suit(cards):
    counts = {}
    for c in cards:
        suit = c[-2:]
        counts[suit] = counts.get(suit, 0) + 1
    return max(counts.values())

def count_multiples(cards):
    counts = {}
    for c in cards:
        rank = c[:-2]
        counts[rank] = counts.get(rank, 0) + 1
    return max(counts.values())

def find_loser(hands):
    totals = {n: sum(card_value(c) for c in h) for n, h in hands.items()}
    print("\nმოთამაშეების ქულები:")
    for n, t in totals.items():
        print(f"{n}: {t}")

    worst_score = min(totals.values())
    losers = [n for n, t in totals.items() if t == worst_score]
    if len(losers) == 1:
        return losers[0]

    suits = {n: count_same_suit(hands[n]) for n in losers}
    worst_suit_count = min(suits.values())
    losers2 = [n for n, s in suits.items() if s == worst_suit_count]
    if len(losers2) == 1:
        print(f"ფრე ქულებზე: გამარჯვებული გადაწყდა მეტი ერთნაირი ფერით")
        return losers2[0]

    mults = {n: count_multiples(hands[n]) for n in losers2}
    worst_mult_count = min(mults.values())
    losers3 = [n for n, m in mults.items() if m == worst_mult_count]
    if len(losers3) == 1:
        print(f"ფრე ქულებსა და ფერებში: გამარჯვებული გადაწყდა მეტ ერთნაირ ნომერში")
        return losers3[0]

    print("ფრე – არავინ დატოვა თამაში")
    return None

def get_valid_name(prompt):
    while True:
        name = input(prompt).strip()
        if len(name) >= 3:
            return name
        print("სახელი უნდა შედგებოდეს მინიმუმ 3 ასოსგან. შეიყვანეთ თავიდან.")

def get_valid_index(prompt):
    while True:
        s = input(prompt).strip()
        if s.isdigit():
            idx = int(s)
            if 1 <= idx <= 5:
                return idx - 1
        print("გთხოვთ შეიყვანოთ ნომერი 1–5 ჩარჩოში.")

def replacement_round(hands, deck):
    for name, hand in hands.items():
        print(f"\n{name}: {', '.join(hand)}")
        if input(f"{name}, გინდათ კარტის შეცვლა? (y/n): ").strip().lower() == 'y':
            idx = get_valid_index("შესაცვლელი კარტის ნომერი (1–5): ")
            old = hand[idx]
            hand[idx] = deck.pop()
            print(f"{name} შეცვალა {old} და მიიღო {hand[idx]}")
    print()
    return hands

def main():
    names = []
    for i in range(3):
        prompt = f"გთხოვთ შეიყვანოთ მოთამაშე {i+1}-ის სახელი: "
        names.append(get_valid_name(prompt))

    while len(names) > 1:
        deck = create_deck()
        hands = deal_cards(names, deck)

        print("\nდარიგებული კარტები:")
        for n, h in hands.items():
            print(f"{n}: {', '.join(h)}")

        hands = replacement_round(hands, deck)
        loser = find_loser(hands)

        if loser:
            print(f"\nთამაშიდან გავარდა: {loser}\n")
            names.remove(loser)
        else:
            print("\nარავინ დატოვა თამაში (ფრე)\n")

    print(f"🏆 გამარჯვებულია: {names[0]}")

if __name__ == "__main__":
    main()

# test hands:

test_hand_1 = {
    "დეა": ["A♣️", "K♦️", "Q❤️", "J♠️", "10♣️"], #66
    "ვახო": ["9♦️", "8❤️", "7♠️", "K♣️", "9♦️"], #46
    "ლაშა": ["4❤️", "3♠️", "2♣️", "A♦️", "K❤️"] # 42
}
# print(find_loser(test_hand_1))  # Should return "ლაშა"

# ფრე ქულებზე
test_hand_2 = {
    'ვახო': ["10♣️","10♦️","10❤️","10♠️","2♣️"],  # 42; # ♣️×2, ♦️×1, ❤️×1, ♠️×1
    'დეა':   ["9♣️","9♣️","9♦️","9♦️","6♦️"],      # 42; ♣️×2, ♦️×3
    'ლაშა':  ["8♣️","A♦️","7❤️","7♠️","6♣️"]       # 48
}
# print(find_loser(test_hand_2))  # Should return "ვახო"

# ფრე ქულებზე და ფერებში
test_hand_3 = {
    'დეა': ["5♣️","4♦️","5❤️","6♠️","7♣️"],  # 27, # ♣️×2, ♦️×1, ❤️×1, ♠️×1, # 5×2
    'ლაშა':   ["5♣️","5♦️","5♠️","6❤️","6♦️"],  # 27, # ♦️×2, ♣️×1, ❤️×1, ♠️×1, # 5×3
    'ვახო':  ["10♣️","9♦️","8❤️","7♠️","6♣️"]  # 40
}
# print(find_loser(test_hand_3))  # Should return "დეა"

# ფრე ქულებზე, ფერებში და ერთნაირ ნომერში
test_hand_4 = {
    'ლაშა': ["K♣️","K♦️","A❤️","J♠️","9♣️"], # 66
    'დეა':   ["K♣️","K♦️","Q❤️","J♠️","4♣️"],  # 53, # ♣️×2, ♦️×1, ❤️×1, ♠️×1, # K×2
    'ვახო':  ["K❤️","K♦️","Q❤️","J♠️","4♣️"]   # 53, # ❤️×2, ♦️×1, ♣️×1, ♠️×1, # K×2
}

# print(find_loser(test_hand_4))  # Should return None 