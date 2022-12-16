Rock, Paper, Scissors = [0, 1, 2]

class RockPaperScissors():
    moves = {'A': Rock, 'B': Paper, 'C': Scissors,
             'X': Rock, 'Y': Paper, 'Z': Scissors}

    outcomes = {'X': "loss", 'Y': "draw", 'Z': "win"}

    scores = {Rock: 1, Paper: 2, Scissors: 3, "loss": 0, "draw": 3, "win": 6}

    def get_move(self, input_):
        return self.moves[input_]

    def get_required_outcome(self, outcome_key):
        return self.outcomes[outcome_key]

    def game_outcome(self, move1, move2):
        if move1 == move2:
            return ("draw", "draw")
        if move1 == Rock:
            if move2 == Paper:
                return ("loss", "win")
            else:
                return ("win", "loss")
        elif move1 == Paper:
            if move2 == Scissors:
                return ("loss", "win")
            else:
                return ("win", "loss")
        else:
            if move2 == Rock:
                return ("loss", "win")
            else:
                return ("win", "loss")

    def score_player(self, move, outcome):
        return self.scores[move] + self.scores[outcome]

    def force_outcome(self, move1, desired_outcome):
        if desired_outcome == "draw":
            return move1
        if desired_outcome == "win":
            if move1 == Rock:
                return Paper
            elif move1 == Paper:
                return Scissors
            else:
                return Rock
        else:
            if move1 == Rock:
                return Scissors
            elif move1 == Paper:
                return Rock
            else:
                return Paper

    def score_game(self, player1, player2):
        move1 = self.get_move(player1)
        move2 = self.get_move(player2)
        outcome = self.game_outcome(move1, move2)
        _, result = outcome
        score = self.score_player(move2, result)
        return score

    def score_forced_outcome(self, player1, player2):
        move1 = self.get_move(player1)
        desired_outcome = self.get_required_outcome(player2)
        move2 = self.force_outcome(move1, desired_outcome)
        outcome = self.game_outcome(move1, move2)
        _, result = outcome
        assert result == desired_outcome
        score = self.score_player(move2, result)
        return score

if __name__ == '__main__':
    game = RockPaperScissors()
    total = 0
    with open("input.txt") as fl:
        for line in fl:
            player1, player2 = line.rstrip().split()
            score = game.score_game(player1, player2)
            total += score
    print(f"Total (part1) = {total}")

    total = 0
    with open("input.txt") as fl:
        for line in fl:
            player1, outcome_key = line.rstrip().split()
            score = game.score_forced_outcome(player1, outcome_key)
            total += score
    print(f"Total (part 2) = {total}")

