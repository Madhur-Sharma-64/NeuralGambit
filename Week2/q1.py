import json
import copy  # use it for deepcopy if needed
import math  # for math.inf
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# Global variables in which you need to store player strategies (this is data structure that'll be used for evaluation)
# Mapping from histories (str) to probability distribution over actions
strategy_dict_x = {}
strategy_dict_o = {}


class History:
    def __init__(self, history=None):
        """
        # self.history : Eg: [0, 4, 2, 5]
            keeps track of sequence of actions played since the beginning of the game.
            Each action is an integer between 0-8 representing the square in which the move will be played as shown
            below.
              ___ ___ ____
             |_0_|_1_|_2_|
             |_3_|_4_|_5_|
             |_6_|_7_|_8_|

        # self.board
            empty squares are represented using '0' and occupied squares are either 'x' or 'o'.
            Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
            for board
              ___ ___ ____
             |_x_|___|_x_|
             |___|_o_|_o_|
             |___|___|___|

        # self.player: 'x' or 'o'
            Player whose turn it is at the current history/board

        :param history: list keeps track of sequence of actions played since the beginning of the game.
        """
        if history is not None:
            self.history = history
            self.board = self.get_board()
        else:
            self.history = []
            self.board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.player = self.current_player()

    def current_player(self):
        """ Player function
        Get player whose turn it is at the current history/board
        :return: 'x' or 'o' or None
        """
        total_num_moves = len(self.history)
        if total_num_moves < 9:
            if total_num_moves % 2 == 0:
                return 'x'
            else:
                return 'o'
        else:
            return None

    def get_board(self):
        """ Play out the current self.history and get the board corresponding to the history in self.board.

        :return: list Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
        """
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        for i in range(len(self.history)):
            if i % 2 == 0:
                board[self.history[i]] = 'x'
            else:
                board[self.history[i]] = 'o'
        return board

    def is_win(self):
        global board
        # check if the board position is a win for either players
        # Feel free to implement this in anyway if needed
        if self.board[0] == self.board[1] == self.board[2] and self.board[0] != '0':
            return self.board[0]
        
        elif self.board[3] == self.board[4] == self.board[5] and self.board[3] != '0':
            return self.board[3]
        
        elif self.board[6] == self.board[7] == self.board[8] and self.board[6] != '0':
            return self.board[6]
        
        elif self.board[0] == self.board[4] == self.board[8] and self.board[0] != '0':
            return self.board[0]
        
        elif self.board[2] == self.board[4] == self.board[6] and self.board[2] != '0':
            return self.board[2]
        
        elif self.board[0] == self.board[3] == self.board[6] and self.board[0] != '0':
            return self.board[0]
        
        elif self.board[1] == self.board[4] == self.board[7] and self.board[1] != '0':
            return self.board[1]
        
        elif self.board[2] == self.board[5] == self.board[8] and self.board[2] != '0':
            return self.board[2]
            
        # else
        return None

    def is_draw(self):
        # check if the board position is a draw
        # Feel free to implement this in anyway if needed
        global board
        for i in range(9):
            if self.board[i] == '0':
                return False
        return True

    def get_valid_actions(self):
        # get the empty squares from the board
        # Feel free to implement this in anyway if needed
        val = []
        for  i in range(9):
            if (self.board[i] == '0'):
                val.append(i)
        return val    

    def is_terminal_history(self):
        # check if the history is a terminal history
        # Feel free to implement this in anyway if needed
        if ( self.is_win() != None ):
            return True
        else :
            if ( self.is_draw() == True ):
                return True
            else:
                return False

    def get_utility_given_terminal_history(self):

        winner = self.is_win()
        if (winner == 'x') :
            return +1
        elif (winner == 'o') :
            return -1
        else:
            return 0


    def update_history(self, action):
        # In case you need to create a deepcopy and update the history obj to get the next history object.
        # Feel free to implement this in anyway if needed
        new_history = History(self.history + [action])
        return new_history


def backward_induction(history_obj, alpha = -math.inf, beta = math.inf):
    """
    :param history_obj: Histroy class object
    :return: best achievable utility (float) for th current history_obj
    """
    global strategy_dict_x, strategy_dict_o

    if history_obj.is_terminal_history():
        return history_obj.get_utility_given_terminal_history()
    
    valid_actions = history_obj.get_valid_actions()
    history_key = ''.join(str(a) for a in history_obj.history)

    prob_dist = {str(i): 0.0 for i in range(9)}

    if history_obj.player == 'x':  #Maxmizing Player
        maxEval = -math.inf
        best_action = None

        for action in valid_actions :
            child = history_obj.update_history(action)
            Eval = backward_induction(child, alpha, beta)

            if Eval > maxEval :
                maxEval = Eval
                best_action = action

            alpha =  max (alpha, maxEval)
            if beta <= alpha :
                break

        prob_dist[str(best_action)] = 1
        strategy_dict_x[history_key] = prob_dist
        return maxEval
        
    else : #Minimizing Player
        minEval = math.inf
        best_action = None
        
        for action in valid_actions :
            child = history_obj.update_history(action)
            Eval = backward_induction(child, alpha, beta)

            if Eval < minEval :
                minEval = Eval
                best_action = action
                 
            beta = min (beta, minEval)
            if beta <= alpha :
                break

        prob_dist[str(best_action)] = 1.0
        strategy_dict_o[history_key] = prob_dist
        return minEval


def solve_tictactoe():
    backward_induction(History())
    with open('./policy_x.json', 'w') as f:
        json.dump(strategy_dict_x, f)
    with open('./policy_o.json', 'w') as f:
        json.dump(strategy_dict_o, f)
    return strategy_dict_x, strategy_dict_o


if __name__ == "__main__":
    logging.info("Start")
    solve_tictactoe()
    logging.info("End")