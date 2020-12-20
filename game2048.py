import random

SIZE = 4
DIGITS = 4


class Game:

    def __init__(self, board=None, verbose=True):
        self.board = [row[:] for row in board or [[0] * SIZE] * SIZE]
        self.verbose = verbose
        self.score = 0

    def show(self):
        separator = ' -' + '-' * (DIGITS + len(' | ')) * SIZE
        print(separator)
        for row in self.board:
            print(' | ' + ' | '.join(f'{tile:{DIGITS}}' for tile in row) + ' |')
        print(separator)

    def scoring(self, tile):
        self.score += tile * 2
        if self.verbose:
            print(f'{tile}+{tile}={tile*2}')

    def move_left(self):
        moved = False
        for row in self.board:
            for left in range(SIZE - 1):
                for right in range(left + 1, SIZE):
                    if row[right] == 0:
                        continue
                    if row[left] == 0:
                        row[left] = row[right]
                        row[right] = 0
                        moved = True
                        continue
                    if row[left] == row[right]:
                        self.scoring(row[right])
                        row[left] += row[right]
                        row[right] = 0
                        moved = True
                        break
                    if row[left] != row[right]:
                        break
        return moved

    def rotate_left(self):
        self.board = [list(row) for row in zip(*self.board)][::-1]

    def rotate_right(self):
        self.board = [list(row)[::-1] for row in zip(*self.board)]

    def rotate_turn(self):
        self.board = [row[::-1] for row in self.board][::-1]

    def flick_left(self):
        moved = self.move_left()
        return moved

    def flick_right(self):
        self.rotate_turn()
        moved = self.move_left()
        self.rotate_turn()
        return moved

    def flick_up(self):
        self.rotate_left()
        moved = self.move_left()
        self.rotate_right()
        return moved

    def flick_down(self):
        self.rotate_right()
        moved = self.move_left()
        self.rotate_left()
        return moved

    def playable(self):
        return any(flick(Game(self.board, verbose=False))
                   for flick in (Game.flick_left, Game.flick_right,
                                 Game.flick_up, Game.flick_down))

    def put_tile(self):
        zeros = [(y, x)
                 for y in range(SIZE)
                 for x in range(SIZE)
                 if self.board[y][x] == 0]
        y, x = random.choice(zeros)
        self.board[y][x] = random.choice((2, 4))


def play():
    game = Game()
    game.put_tile()
    game.put_tile()
    game.show()
    key_flick = {'r': game.flick_right,
                 'l': game.flick_left,
                 'u': game.flick_up,
                 'd': game.flick_down}
    try:
        count = 0
        while game.playable():
            key = input(f'input {count}th move>>> ')
            if key not in key_flick:
                print('err')
            elif key_flick[key]():
                game.put_tile()
                game.show()
                print(f'score = {game.score}')
                count += 1
    except (KeyboardInterrupt, EOFError):
        print()
    print('#######################')
    print('Game Over')
    print(f'Final Score = {game.score}')
    print('#######################')


if __name__ == '__main__':
    play()