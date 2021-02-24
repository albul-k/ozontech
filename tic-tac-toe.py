"""
КРЕСТИКИ-НОЛИКИ
Написать реализацию для игры в крестики-нолики без графического интерфейса.
Спросить у игрока, кто ходит первым (игрок или компьютер). После этого игрок и компьютер указывают координаты клеток от A1 до C3. Если игрок ходит на занятое или несуществующее поле, то выводить ошибку и предложить указать другое поле. Если компьютер выиграл, то сообщить об этом и завершить текущую игру. Если закончились свободные клетки и компьютер не выиграл, то объявить ничью и завершить текущую игру.
Компьютер не должен проигрывать.

Пример игры:
Крестики нолики. Кто ходит первым? 1 игрок, 2 компьютер
> 2
К A1
> B2
K C3
> C4
указано неверное поле
> C1
К A3
> A2
И B3
Компьютер выиграл
"""

class TicTacToe():

    def __init__(self, columns: list, rows: list) -> None:
        """[summary]

        Args:
            columns (list): column names of game field
            rows (list): row names of game field
        """

        self.columns = columns
        self.rows = rows
        self.combinations = self.collect_win_combinations()
        self.fields_available = self.collect_cells()
        self.moves = set()
        self.game_is_over = False
    
    def collect_win_combinations(self) -> list:
        """Collecting all win combinations

        Returns:
            list: list of win combinations, each combination is Dict, where the key is move, value is weight (default 0)
        """
        
        combinations = []

        # each column, e.g. ['A1', 'A2', 'A3']
        for col in self.columns:
            combination = {}
            for row in self.rows:
                combination[str(col) + str(row)] = 0
            combinations.append(combination)
        
        # each row, e.g. ['A1', 'B1', 'C1']
        for row in self.rows:
            combination = {}
            for col in self.columns:
                combination[str(col) + str(row)] = 0
            combinations.append(combination)

        # major diagonal - ['A3', 'B2', 'C1']
        _row = len(self.rows) + 1
        combination = {}
        for col in self.columns:
            _row -= 1
            combination[str(col) + str(_row)] = 0
        combinations.append(combination)    

        # minor diagonal - ['A1', 'B2', 'C3']
        _row = 0
        combination = {}
        for col in self.columns:
            _row += 1
            combination[str(col) + str(_row)] = 0
        combinations.append(combination)

        return combinations

    def collect_cells(self) -> set:
        """Collect all cells of the game field

        Returns:
            set: Set with cell names, e.g. {'A1', 'A2', ...}
        """
        cells = {str(col) + str(row) for col in self.columns for row in self.rows}
        return cells

    def make_move(self, move: str, is_computer_move: bool = False) -> set:
        """Processing a move

        Args:
            move (str): cell name, e.g. 'A1'
            is_computer_move (bool, optional): is computer or player move. Defaults to False.

        Returns:
            set: all made moves
        """
        for combination in self.combinations:
            if move in combination:
                # the key of combination Dict is weights of moves
                # 1 for computer and 10 for player
                combination[move] = 1 if is_computer_move else 10
                weight = sum(combination.values())
                
                # if weight is equal len(self.columns) it means that computer made win combination
                # either if weight is equal len(self.columns)*10 means that player made win combination
                if weight == len(self.columns) or weight == len(self.columns) * 10:
                    self.game_is_over = True
                    break
        
        self.moves.add(move)
        return self.moves

    def make_computer_move(self) -> set:
        """Processing a computer move

        Returns:
            set: all made moves
        """
        move = None
        max_weight = 0
        for combination in self.combinations:
            combination_weights = combination.values()
            
            # skip ended combinations
            if min(combination_weights) != 0:
                continue

            weight = sum(combination_weights)

            # next move is win move
            if weight == len(self.columns) - 1:
                for move in combination:
                    if combination[move] == 0:
                        break
                break
            
            # make move in combination with the greatest weight
            if weight >= max_weight:
                max_weight = weight
                for move in combination:
                    if combination[move] == 0:
                        break
        
        if move is None:
            self.game_is_over = True
        else:
            self.make_move(move, True)
        return self.moves, move
    
    @staticmethod
    def run():
        turn = None
        while turn is None:
            try:
                turn = int(input('Tic Tac Toe. Who goes first? 1 - player (P), 2 - computer (C)\n'.format()))
                if turn != 1 and turn != 2:
                    raise ValueError
            except ValueError:
                print('Incorrect value. Repeat the enter: 1 or 2')
                turn = None

        moves = set()
        while True:
            # if turn has odd value - move of the player
            if turn & 1 == 1:
                try:
                    move = input('P '.format()).upper()
                    if not move in game.fields_available:
                        raise ValueError('Incorrect field name')
                    if move in moves:
                        raise ValueError('Such a move has already been')
                except ValueError as e:
                    print(e)
                    continue
                
                moves = game.make_move(move, False)
            else:
                moves, move = game.make_computer_move()
                print('C {}'.format(move))
            
            if len(moves) == len(game.fields_available):
                print('Draw')
                break
            elif game.game_is_over:
                print('The player won' if turn & 1 else 'The computer won')
                break

            turn += 1

if __name__ == "__main__":
    game = TicTacToe(
        columns=['A', 'B', 'C'],
        rows=[1, 2, 3],
    )
    game.run()
