from copy import deepcopy


def rotate(board, n_rotations):
    """
    Is recursion really the fastest way to do this?
    Almost certainly not. But it is very readable though.
    """

    n_rotations = n_rotations % 4
    if n_rotations == 0:
        return board

    else:

        new_board = deepcopy(board)
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                new_i = j
                new_j = 4 - i
                new_board[new_i][new_j] = val

        return rotate(new_board, n_rotations - 1)


def reflect(board, n_reflections):

    if n_reflections % 2 == 0:
        return board

    else:

        new_board = deepcopy(board)
        for i, row in enumerate(board):
            for j, val in enumerate(row):
                new_i = j
                new_j = i
                new_board[new_i][new_j] = val

        return new_board


def make_symetry_functions():
    # returns a list of 8 functions, each returning a symetry of the board
    # and the inverse of each function
    sym_funcs = []
    inv_sym_funcs = []
    for reflections in range(2):  # reflection about the diagonal
        for rotations in range(4):
            sym_funcs.append(lambda x, ref=reflections, rot=rotations: rotate(reflect(x, ref), rot))
            inv_sym_funcs.append(lambda x, ref=reflections, rot=rotations: reflect(rotate(x, -rot), -ref))

    return sym_funcs, inv_sym_funcs


def flatten(board):
    return [x for xs in board for x in xs]


def tern2int(int_ls):
    """
    Converts a list of numbers representing digits in a ternary number to a number in base 10
    """
    b10_sum = 0
    for i, num in enumerate(reversed(int_ls)):
        b10_sum += num * (3 ** i)
    return b10_sum


def argmin(ls):
    return min(range(len(ls)), key=ls.__getitem__)


def board2state(board, symetry_funcs, inv_symetry_funcs):
    """
    Converts a board into a state (another board)
    All symmetrical boards will map to the same state,
    this reduces the number of states our agent needs to learn about

    It also returns the function that will convert an action in the state back into the original board coordinates
    """
    syms = [f(board) for f in symetry_funcs]  # all the symmetries
    flats = [flatten(sym) for sym in syms]  # flatten out the list of lists
    nums = [tern2int(flat) for flat in flats]  # treat each list as a ternary number, and convert to base10
    i = argmin(nums)  # find where the minimum is
    state = syms[i]  # return one of the symmetries as the state

    return state, inv_symetry_funcs[i]  # include the appropriate inverse function


if __name__ == "__main__":

    tst_ls = [[i + (j * 5) for i in range(5)] for j in range(5)]

    # testing rotation
    assert rotate(tst_ls, 0) == rotate(tst_ls, 4) == rotate(tst_ls, -4) == tst_ls
    assert rotate(tst_ls, 1) == rotate(tst_ls, 5) == rotate(tst_ls, -3)
    assert rotate(tst_ls, 3)[2][2] == tst_ls[2][2]

    # testing reflection
    assert reflect(tst_ls, 0) == reflect(tst_ls, 2) == reflect(tst_ls, -2) == tst_ls
    assert reflect(tst_ls, 1) == reflect(tst_ls, 3)
    new_ls = reflect(tst_ls, 1)
    for i, (og, new) in enumerate(zip(tst_ls, new_ls)):
        for j, (o, n) in enumerate(zip(og, new)):
            if i == j:
                assert o == n

    tst_board = [[(i + (j * 5)) % 3 for i in range(5)] for j in range(5)]

    # testing board2state
    sym_funcs, inv_sym_funcs = make_symetry_functions()
    state1, state2board = board2state(tst_board, sym_funcs, inv_sym_funcs)
    assert state2board(state1) == tst_board
    state2, _ = board2state(rotate(tst_board, -1), sym_funcs, inv_sym_funcs)
    state3, _ = board2state(reflect(tst_board, -1), sym_funcs, inv_sym_funcs)
    assert state1 == state2 == state3

    '''
    example of use:
    state, state2board = board2state(board, sym_funcs, inv_sym_funcs)
    action_in_state = agent.act(state)
    action_in_board = state2board(action_in_state)
    board = [i+j for i,j in zip(action_in_board, board)]
    '''
