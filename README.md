# Play-Connect-4-game-using-AI
I have written a computer program to play the classic game Connect Four game to practice the AI minimax and heuristic algorithms. Connect Four is a tic-tac-toe variant played on a grid. Players alternate turns dropping coins into one of the seven different columns.As the name implies, the goal of Connect Four is to get four of your colored coins in a row, either horizontally, diagonally, or vertically. The first player to do so wins. If all locations are filled without a player getting four in a row, the game is a draw.

To run:
The Connect Four program has several different command-line switches that you can use to control how the game is played. By default, the two players are human-controlled. You can choose which AI modules to use by using the -p1 and -p2 switches to select the AIModules to use as the first and second player. For example, to pit the randomAI player against the monteCarloAI player, you could use:

python main.py -p1 randomAI -p2 monteCarloAI

My evaluation function looks like this:

def evaluation(self, board): eval =0
col = [row[3] for row in board] 
eval += col.count(self.position)*5 
col = [row[4] for row in board] 
eval += col.count(self.position)*3 
col = [row[2] for row in board] 
eval += col.count(self.position)*3
return eval

By attaching values to locations, my evaluation function is able to return a linear weighted sum that is used to order terminal nodes as the true utility would correlate with chances of winning:
eval(s) += col.count(self.position)*weight
s = board state that is being evaluated
col = the specific column from the board self.position = the current player
weight = the weight assigned to the final count
