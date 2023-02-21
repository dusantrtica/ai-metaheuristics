BOARD_SIZE = 3
REWARD = 10


class TicTacToe:
    def __init__(self, board):
        self.board = board
        self.player = 'O'
        self.computer = 'X'

    def run(self):
        print('Computer starts...')
        while True:
            # use minimax algorithm in order to decide the optimal
            self.move_computer()
            self.move_player()

    def print_board(self):
        print(self.board[1] + '|' + self.board[2] + '|' + self.board[3])
        print('-+-+-')
        print(self.board[4] + '|' + self.board[5] + '|' + self.board[6])
        print('-+-+-')
        print(self.board[7] + '|' + self.board[8] + '|' + self.board[9])
        print('\n')

    def move_player(self):
        position = int(input('Enter the position for O: '))
        self.update_player_position(self.player, position)

    def update_player_position(self, player, position):
        if self.is_cell_free(position):
            self.board[position] = player
            self.check_game_state()
        else:
            print("Can't insert there!")
            self.move_player()

    def is_cell_free(self, position):
        return self.board[position] == ' '

    def check_game_state(self):
        self.print_board()
        if self.is_draw():
            print("Draw!")
            exit()

        if self.is_winning(self.player):
            print("Player wins!")
            exit()

        if self.is_winning(self.computer):
            print("Computer wins!")
            exit()

    def is_draw(self):
        for position in self.board.keys():
            if self.board[position] == ' ':
                return False
        return True

    def is_winning(self, player):
        # checking the diagonal
        if self.board[1] == player and self.board[5] == player and self.board[9] == player:
            return True

        if self.board[3] == player and self.board[5] == player and self.board[7] == player:
            return True

        # check rows and columns
        for i in range(BOARD_SIZE):
            if self.board[3 * i + 1] == player and self.board[3 * i + 2] == player and self.board[3 * i + 3] == player:
                return True
            if self.board[i + 1] == player and self.board[i + 4] == player and self.board[i + 7] == player:
                return True

        return False

    def move_computer(self):
        best_score = -float('inf')
        # best position (best next move) for the computer
        best_move = 0
        # the computer considers all the empty cells on the board and
        # calculates the minimax score (10, -10, 0)
        for position in self.board.keys():
            if self.board[position] == ' ':
                self.board[position] = self.computer
                score = self.minimax(0, False)
                self.board[position] = ' '

                if score > best_score:
                    best_score = score
                    best_move = position

        # make the next move according to the minimax algorithm result
        self.board[best_move] = self.computer
        self.check_game_state()

    def minimax(self, depth, is_maximizer):
        if self.is_winning(self.computer):
            return REWARD - depth

        if self.is_winning(self.player):
            return -REWARD + depth

        if self.is_draw():
            return 0

        if is_maximizer:
            best_score = -float('inf')
            for position in self.board.keys():
                if self.board[position] == ' ':
                    self.board[position] = self.computer
                    score = self.minimax(depth + 1, False)
                    self.board[position] = ' '

                    if score > best_score:
                        best_score = score

            return best_score
        else:
            best_score = float('inf')
            for position in self.board.keys():
                if self.board[position] == ' ':
                    self.board[position] = self.player
                    score = self.minimax(depth + 1, True)
                    self.board[position] = ' '

                    if score < best_score:
                        best_score = score

            return best_score


if __name__ == '__main__':
    board = {num: ' ' for num in range(1, 10)}

    game = TicTacToe(board)
    game.run()
