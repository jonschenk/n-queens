import itertools
import random
from typing import Any, Generator, Union


class State:
    """
    A representation of a board state in an 8-queens problem.

    Each state is represented by a digit string, with one digit per file.
    For each file, the digit indicates which rank the queen is located in.

    For example, a board state of '12345678' represents a board with
    queens in positions a1, b2, c3, d4, e5, f6, g7, and h8,
    where the letters a through h indicate the file (column), and
    the numbers 1 through 8 indicate the rank (row).
    See https://en.wikipedia.org/wiki/Algebraic_notation_(chess) for details.

    You can use standard Python indexing and slicing notation to retrieve
    portions of the state's digit string, for example:
    >>> s = State('12345678')
    >>> s[0]  # get the 0th digit, which is '1'
    >>> s[:4]  # get the first 4 digits, which is '1234'

    You can also use file letters as keys to retrieve individual entries:
    >>> s['c']  # get the digit for file 'c', which is '3'

    You can also convert a state to a tuple containing all the digits:
    >>> tuple(s)  # returns ('1', '2', '3', '4', '5', '6', '7', '8')
    """

    _VALID_DIGITS = '12345678'
    _N = len(_VALID_DIGITS)
    _FILES = 'abcdefgh'
    _state_gen = itertools.product(_VALID_DIGITS, repeat=_N)
    _possible_states = None

    def __init__(self, digits: str) -> None:
        assert len(digits) == self._N, f"invalid number of digits, expected {self._N} but found {len(digits)}"
        for i, digit in enumerate(digits):
            assert 1 <= int(digit or 0) <= self._N, f"invalid digit value '{digit}' found at position {i + 1}"
        self._digits: str = digits

    def __getitem__(self, key: Union[int, slice, str]):
        if isinstance(key, (int, slice)):
            return self._digits[key]
        elif isinstance(key, str):
            assert key in self._FILES, f"invalid file '{key}' specified"
            return self._digits[self._FILES.index(key)]
        else:
            raise TypeError(f"unsupported key of type {type(key)}")

    def __str__(self) -> str:
        return self._digits

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self._digits}')"

    def mate(self, other: 'State', mutation_probability: float = 0.0) -> 'State':
        """
        Mate the state with another state, creating a new successor state.

        The crossover point is chosen at random, and each location in the successor
        state is subject to random mutation with some small probability.

        :param other: The other state in the mating pair
        :param mutation_probability: The probability of random mutation [0.0, 1.0)
        :return: The resulting successor state
        """
        assert 0.0 <= mutation_probability < 1.0, f"mutation probability should fall in range [0.0, 1.0)"

        # randomly choose crossover point
        c = random.randint(0, self._N - 1)

        # generate new digits by combining self with other, cutting at crossover point
        digits = f"{self[:c]}{other[c:]}"

        # for each digit, mutate with some small probability
        if mutation_probability > 0:
            digits = list(digits)
            for i in range(len(digits)):
                if random.random() < mutation_probability:
                    digits[i] = random.choice(self._VALID_DIGITS)
            digits = ''.join(digits)

        # create successor state from resulting digits
        return self.__class__(digits=digits)

    @classmethod
    def generator(cls, num_states: int) -> Generator['State', Any, None]:
        """
        Create a generator that yields the specified number of random board states.

        :param num_states: The number of states to generate
        :return: The generator
        """
        assert num_states > 0, f"invalid number of states: {num_states}"

        # lazily load the N^N possible board states
        if cls._possible_states is None:
            # using tuple() here forces the generator to actually generate
            # all possible states, so that we can randomly choose from them
            cls._possible_states = tuple(cls._state_gen)

        # yield one random state at a time
        for s in random.sample(cls._possible_states, k=num_states):
            yield cls(digits=''.join(s))
