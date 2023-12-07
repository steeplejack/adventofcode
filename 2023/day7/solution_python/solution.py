import sys
from collections import Counter

hands = {
    (1, 1, 1, 1, 1): ("high-card", 1),
    (1, 1, 1, 2): ("one-pair", 2),
    (1, 2, 2): ("two-pair", 3),
    (1, 1, 3): ("three-of-a-kind", 4),
    (2, 3): ("full-house", 5),
    (1, 4): ("four-of-a-kind", 6),
    (5,): ("five-of-a-kind", 7)
}

faces = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}

class Hand:

    def __init__(self, hand):
        hand_type, hand_rank = hands[tuple(sorted(Counter(hand).values()))]
        face_ranks = [faces[c] for c in hand]
        self.hand = hand
        self.hand_type = hand_type
        self.hand_rank = hand_rank
        self.total_rank = (hand_rank, *face_ranks)

    def __repr__(self):
        return f'Hand({self.hand})'

    def __str__(self):
        return f'{self.hand} = {self.hand_type} with rank {self.hand_rank} and sort order {self.total_rank}'

    def __lt__(self, other):
        return self.total_rank < other.total_rank 

    def __eq__(self, other):
        return self.total_rank == other.total_rank

    def __hash__(self, other):
        return hash(self.total_rank)

    def __contains__(self, c):
        if len(c) != 1:
            return False
        return c in self.hand

def optimise(hand):
    if not 'J' in hand:
        return hand
    original_hand = hand
    best_hand = hand
    for c in 'AKQT98765432':
        new_hand_string = original_hand.hand.replace('J', c)
        new_hand = Hand(new_hand_string)
        if new_hand > hand:
            best_hand = new_hand
            hand = best_hand

    original_hand.total_rank = (best_hand.total_rank[0], *original_hand.total_rank[1:])
    return original_hand

def read_cards_and_bids(infile):
    with open(infile) as fl:
        cards, bids = zip(*[line.strip().split() for line in fl])
        cards = [Hand(c) for c in cards]
        bids = [int(b) for b in bids]
    return cards, bids

def part1(infile):
    cards, bids = read_cards_and_bids(infile)
    ranked_cards = sorted(zip(cards, bids), key = lambda x: x[0])
    return sum([pos * bid for (pos, (_, bid)) in enumerate(ranked_cards, start = 1)])

def part2(infile):
    faces['J'] = 1
    cards, bids = read_cards_and_bids(infile)
    cards = [optimise(card) for card in cards]
    ranked_cards = sorted(zip(cards, bids), key = lambda x: x[0])
    return sum([pos * bid for (pos, (_, bid)) in enumerate(ranked_cards, start = 1)])

def main():
    try:
        infile = sys.argv[1]
        print(part1(infile))
        print(part2(infile))
        return 0
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
