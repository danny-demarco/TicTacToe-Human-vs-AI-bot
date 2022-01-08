import pygame
import random
import sys

# Initialise the Pygame module
pygame.init()

# Font type
my_font = pygame.font.SysFont('chalkduster.ttf', 45)

# Specify constants
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = 55
LINE_COLOUR = (23, 145, 135)
WINNING_LINE = (255, 0, 0)
BG_COLOUR = (28, 170, 156)
CROSS_COLOUR = (65, 65, 65)
CIRCLE_COLOUR = (239, 231, 100)

# Initialise the graphical user interface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe with AI Bot')
screen.fill(BG_COLOUR)


def draw_lines():
    """Draws the lines that denote the borders for each of the 9 sections of the board"""

    # Horizontal Top
    pygame.draw.line(screen, LINE_COLOUR, (10, 200), (590, 200), LINE_WIDTH)
    # Horizontal Bottom
    pygame.draw.line(screen, LINE_COLOUR, (10, 400), (590, 400), LINE_WIDTH)
    # Vertical Left
    pygame.draw.line(screen, LINE_COLOUR, (200, 10), (200, 590), LINE_WIDTH)
    # Vertical Right
    pygame.draw.line(screen, LINE_COLOUR, (400, 10), (400, 590), LINE_WIDTH)


def print_state(state):
    """Prints the current state of the board / visual representation of the board."""

    for row in range(len(state)):
        for col in range(len(state)):
            if state[row][col] == 'o':
                pygame.draw.circle(screen, CIRCLE_COLOUR, (int(col * 200 + 200 / 2), int(row * 200 + 200 / 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif state[row][col] == 'x':
                pygame.draw.line(screen, CROSS_COLOUR, (col * 200 + SPACE, row * 200 + 200 - SPACE),
                                 (col * 200 + 200 - SPACE, row * 200 + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOUR, (col * 200 + SPACE, row * 200 + SPACE),
                                 (col * 200 + 200 - SPACE, row * 200 + 200 - SPACE), CROSS_WIDTH)
            else:
                continue


def restart_game():
    """Following a win or a draw, the game can be reinitialised"""

    screen.fill(BG_COLOUR)
    draw_lines()
    driver()


def draw_vertical_winning_line(col):
    """Displays a red line in a column with 3 like tokens to indicate the winning condition"""

    pygame.draw.line(screen, WINNING_LINE, (col * 200 - 100, SPACE),
                     (col * 200 - 100, 600 - SPACE), LINE_WIDTH)


def draw_horizontal_winning_line(row):
    """Displays a red line in a row with 3 like tokens to indicate the winning condition"""

    pygame.draw.line(screen, WINNING_LINE, (SPACE, row * 200 - 100),
                     (600 - SPACE, row * 200 - 100), LINE_WIDTH)


def draw_ascending_diagonal():
    """Displays a red line in an ascending diagonal where 3 like tokens to indicate the winning condition"""

    pygame.draw.line(screen, WINNING_LINE, (50, 550),
                     (550, 50), LINE_WIDTH)


def draw_descending_diagonal():
    """Displays a red line in an descending diagonal where 3 like tokens to indicate the winning condition"""

    pygame.draw.line(screen, WINNING_LINE, (50, 50),
                     (550, 550), LINE_WIDTH)


def check_win(winning_player, state):
    """Check for a winning condition and if found, draw a line through the 3 tokens to indicate the win"""

    if winning_player == state[0][0] and winning_player == state[0][1] and winning_player == state[0][2]:  # Row 1
        draw_horizontal_winning_line(1)
        return True
    elif winning_player == state[1][0] and winning_player == state[1][1] and winning_player == state[1][2]:  # Row 2
        draw_horizontal_winning_line(2)
        return True
    elif winning_player == state[2][0] and winning_player == state[2][1] and winning_player == state[2][2]:  # Row 3
        draw_horizontal_winning_line(3)
        return True
    elif winning_player == state[0][0] and winning_player == state[1][0] and winning_player == state[2][0]:  # Column 1
        draw_vertical_winning_line(1)
        return True
    elif winning_player == state[0][1] and winning_player == state[1][1] and winning_player == state[2][1]:  # Column 2
        draw_vertical_winning_line(2)
        return True
    elif winning_player == state[0][2] and winning_player == state[1][2] and winning_player == state[2][2]:  # Column 3
        draw_vertical_winning_line(3)
        return True
    elif winning_player == state[0][0] and winning_player == state[1][1] and winning_player == state[2][2]:  # Diagonal
        draw_descending_diagonal()
        return True
    elif winning_player == state[0][2] and winning_player == state[1][1] and winning_player == state[2][0]:  # Diagonal
        draw_ascending_diagonal()
        return True
    # Check for a draw
    elif state[0][0] != ' ' and state[0][1] != ' ' and state[0][2] != ' ' and state[1][0] != ' ' \
            and state[1][1] != ' ' and state[1][2] != ' ' and state[2][0] != ' ' and state[2][1] != ' ' \
            and state[2][2] != ' ':
        return True
    else:
        return False


def score_end(state):
    """Used by the MINIMAX algorithm to score the branches in the hypothetical plays it produces"""

    player = {'x': 1,
              'o': -1}
    for pl, res in player.items():
        if pl == state[0][0] and pl == state[0][1] and pl == state[0][2]:  # Row 1
            return res
        elif pl == state[1][0] and pl == state[1][1] and pl == state[1][2]:  # Row 2
            return res
        elif pl == state[2][0] and pl == state[2][1] and pl == state[2][2]:  # Row 3
            return res
        elif pl == state[0][0] and pl == state[1][0] and pl == state[2][0]:  # Column 1
            return res
        elif pl == state[0][1] and pl == state[1][1] and pl == state[2][1]:  # Column 2
            return res
        elif pl == state[0][2] and pl == state[1][2] and pl == state[2][2]:  # Column 3
            return res
        elif pl == state[0][0] and pl == state[1][1] and pl == state[2][2]:  # Diagonal descending
            return res
        elif pl == state[0][2] and pl == state[1][1] and pl == state[2][0]:  # Diagonal ascending
            return res
        # Check for a draw
        elif state[0][0] != ' ' and state[0][1] != ' ' and state[0][2] != ' ' and state[1][0] != ' ' \
                and state[1][1] != ' ' and state[1][2] != ' ' and state[2][0] != ' ' and state[2][1] != ' ' \
                and state[2][2] != ' ':
            return 0
        else:
            continue
    return None


def play(state, row, col, player):
    """Returns a new board state after the most recent move has been played."""

    first_state = [[], [], []]
    [first_state[r].append(state[r][item]) for r in range(len(state)) for item in range(len(state))]
    new_state = first_state
    new_state[row][col] = player
    new_tup = tuple([tuple(elem) for elem in new_state])
    return new_tup


def moves(state):
    """Returns the list of moves that are available from the current state for use by MINIMAX."""

    emp_spots = []
    for row in range(len(state)):
        for col in range(len(state)):
            if state[row][col] == ' ':
                emp_spots.append((row, col))
            else:
                continue
    return emp_spots


def score(state, player):
    """This is the MINIMAX algorithm, the AI component. Given the game state it returns (game score, best move)"""

    # This is the break case
    if score_end(state) is not None:
        return score_end(state), None

    # Always choose the centre of the board for the bot if that space is available
    if state[1][1] == ' ' and player == 'x':
        return 1, [1, 1]

    # obtain a list of tuples with all available spaces left on the board
    pos_mov = moves(state)

    # Which player are we going to complete a recursion for on this play of the game?
    if player == 'x':
        branch_score = []  # array to keep a log of the end of branch scores
        place_played = []  # array to keep a log of the board place played

        # traverse all empty spaces on the board
        for row, col in pos_mov:
            # Returns a new state after the given move has been played
            state_new = play(state, row, col, player)
            # Next we call the recursive function with the new state and we change the player to start the route down
            # this particular branch, x is the result from the recursive function, the end score of this particular
            # branch
            x, y = score(state_new, 'o')
            # Save this branch result in a list
            branch_score.append(x)
            # Save the position we played to give this result
            place_played.append((row, col))
            # Player x wants to get the highest possible score, so we can just take a max value of our list
            best = max(branch_score)
            # find the place that was played when we obtained this maximum result
            index = branch_score.index(best)
        return best, place_played[index]

    else:
        # This is practically a copy of the above for x, but we are looking to find the minimum value for player 'o'
        branch_score = []
        place_played = []

        for row, col in pos_mov:
            state_new = play(state, row, col, player)
            x, y = score(state_new, 'x')
            branch_score.append(x)
            place_played.append((row, col))
            #print(f"o: branch :{branch_score} \n place: {place_played}")
            # Here we locate the minimum value rather than the maximum
            best = min(branch_score)
            index = branch_score.index(best)

        return best, place_played[index]


def driver():
    """Set up a clean board and pick a random player, then enter the main game loop"""

    state = ((' ', ' ', ' '), (' ', ' ', ' '), (' ', ' ', ' '))
    pick_play = random.random()
    if pick_play <= 0.5:
        player = 'x'
    else:
        player = 'o'
    print(f"The first player is: {player}")
    print_state(state)
    print('')

    game_over = False
    draw_lines()
    pygame.display.update()

    while True:
        # This is the bot player
        if player == 'x' and not game_over:
            # x returned is the likely score and y is the tuple of the move to take
            x, y = score(state, player)
            # play the move denoted by the tuple y
            state = play(state, y[0], y[1], player)
            game_over = check_win(player, state)
            print_state(state)
            player = 'o'
        # This allows for a game restart to be initiated in case player 'o' plays the last move in a draw
        elif player == 'x' and game_over:
            player = 'o'
        # This is the human player
        elif player == 'o':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Check if the human pressed the mouse on the board
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    # Get the coordinates of the chosen move
                    mouse_x = event.pos[0]  # x
                    mouse_y = event.pos[1]  # y

                    # Calculate which tile on the board the player has selected
                    chosen_row = int(mouse_y // 200)
                    chosen_col = int(mouse_x // 200)

                    if state[chosen_row][chosen_col] != ' ' and event.type == pygame.MOUSEBUTTONDOWN:
                        display = 'This is not a legal move, try again!'
                        continue

                    state = play(state, chosen_row, chosen_col, player)
                    game_over = check_win(player, state)

                    player = 'x'

                # Allow the game to be restarted with the 'r' key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart_game()

            print_state(state)
            pygame.display.update()


driver()
