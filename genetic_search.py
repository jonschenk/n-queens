"""
Genetic algorithm-based search for a solution to the 8-queens problem

jschenk21@georgefox.edu
"""

from state import State

BOARD_SIZE = 8;
SOLUTION = 28;


def fitness(s: State) -> int:
    """
    Fitness function for a board state in an 8-queens problem.

    The fitness score is defined here as the number of non-attacking pairs of queens.
    A solution state has a fitness score of 28 (i.e., n choose k, with n=8 and k=2).

    :param s: The state to compute the fitness score for
    :return: The fitness score for the specified state
    """
    score = 0
    for i in range(BOARD_SIZE):
        for j in range(i+1, 8):
            if s[i] != s[j] and abs(i-j) != abs(int(s[i]) - int(s[j])):
                score += 1
    
    return score


def goal(s: State) -> bool:
    """
    Goal test function.

    :param s: The state to test for the goal condition
    :return: True if the specified state is a goal, else False
    """
    return fitness(s) == SOLUTION


def print_board(s: State) -> None:
    """
    Print the board represented by the specified state.

    :param s: The state to print the board for
    """
    print('┏' + '━━━┳' * (BOARD_SIZE - 1) + '━━━┓')
    for rank in range(BOARD_SIZE):
        for file in range(BOARD_SIZE):
            if (s[file] == str(BOARD_SIZE - rank)):
                print('┃ ♛ ', end='')
            else:
                print('┃   ', end='')
        if rank != BOARD_SIZE - 1:
            print('┃\n┣' + '━━━╋' * (BOARD_SIZE - 1) + '━━━┫')
        else:
            print('┃')
    print('┗' + '━━━┻' * (BOARD_SIZE - 1) + '━━━┛')
    

# initial population is k randomly generated states
# TODO generate a much larger initial population
K = 1000
MUTATION_PROBABILITY = 0.05

print("> Generating initial population", end='\r')

population = tuple(State.generator(K))
print("\r" + " " * len("> Generating initial population"), end='\r')

hashmap = {}
for state in population:
    hashmap[state] = fitness(state)

searching = True
iterations = 0
counter = 0
searching_strings = ["> Searching   ", "> Searching.  ", "> Searching.. ", "> Searching..."]

while searching:
    print(searching_strings[counter % 4], end='\r')
    counter += 1
    sorted_population = sorted(hashmap, key=hashmap.get, reverse=True)
    maiting_pairs = sorted_population[:K]

    for i in range(K - 1):
        iterations += 1
        child = maiting_pairs[i].mate(maiting_pairs[i+1], MUTATION_PROBABILITY)
        hashmap[child] = fitness(child)

        if (goal(child)):
            golden_child = child
            searching = False

print_board(golden_child)
print("Golden child:", golden_child)
print("Took", iterations, "iterations to find solution")
