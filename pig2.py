import random
import time
import argparse

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0

    def roll(self, die):
        roll = die.roll()
        if roll == 1:
            self.turn_total = 0
            return False
        else:
            self.turn_total += roll
            return True

    def hold(self):
        self.score += self.turn_total
        self.turn_total = 0

class HumanPlayer(Player):
    def decide(self):
        decision = input("Enter 'r' to roll or 'h' to hold: ")
        if decision.lower() == 'r':
            return True
        elif decision.lower() == 'h':
            return False
        else:
            print("Invalid input. Please enter 'r' or 'h'.")
            return self.decide()

class ComputerPlayer(Player):
    def decide(self):
        if self.turn_total >= min(25, 100 - self.score):
            return False
        else:
            return True

class Die:
    def __init__(self):
        self.seed = 0
        random.seed(self.seed)

    def roll(self):
        return random.randint(1, 6)

class PlayerFactory:
    def create_player(self, player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.die = Die()

    def play(self):
        current_player = self.player1
        while self.player1.score < 100 and self.player2.score < 100:
            print(f"\n{current_player.name}'s turn:")
            while True:
                roll = current_player.roll(self.die)
                print(f"Rolled: {self.die.roll()}")
                print(f"Turn total: {current_player.turn_total}")
                print(f"Total score: {current_player.score}")
                if isinstance(current_player, HumanPlayer):
                    decision = current_player.decide()
                else:
                    decision = current_player.decide()
                if decision:
                    if not roll:
                        break
                else:
                    current_player.hold()
                    break
            if current_player == self.player1:
                current_player = self.player2
            else:
                current_player = self.player1
        if self.player1.score >= 100:
            print(f"\n{self.player1.name} wins!")
        else:
            print(f"\n{self.player2.name} wins!")

class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play(self):
        current_player = self.game.player1
        while self.game.player1.score < 100 and self.game.player2.score < 100:
            if time.time() - self.start_time > 60:
                if self.game.player1.score > self.game.player2.score:
                    print(f"\n{self.game.player1.name} wins!")
                elif self.game.player2.score > self.game.player1.score:
                    print(f"\n{self.game.player2.name} wins!")
                else:
                    print("\nIt's a tie!")
                break
            print(f"\n{current_player.name}'s turn:")
            while True:
                roll = current_player.roll(self.game.die)
                print(f"Rolled: {self.game.die.roll()}")
                print(f"Turn total: {current_player.turn_total}")
                print(f"Total score: {current_player.score}")
                if isinstance(current_player, HumanPlayer):
                    decision = current_player.decide()
                else:
                    decision = current_player.decide()
                if decision:
                    if not roll:
                        break
                else:
                    current_player.hold()
                    break
            if current_player == self.game.player1:
                current_player = self.game.player2
            else:
                current_player = self.game.player1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", choices=["human", "computer"], default="human")
    parser.add_argument("--player2", choices=["human", "computer"], default="human")
    parser.add_argument("--timed", action="store_true")
    args = parser.parse_args()

    factory = PlayerFactory()
    player1 = factory.create_player(args.player1, "Player 1")
    player2 = factory.create_player(args.player2, "Player 2")

    game = Game(player1, player2)
    if args.timed:
        timed_game = TimedGameProxy(game)
        timed_game.play()
    else:
        game.play()

if __name__ == "__main__":
    main()