"""Objects representing the state of each round"""
import abc
from enum import Enum


class ResultVars(Enum):
    """ResultVars used by the Results objects, useful in comparisons and to avoid hard coded values"""

    WIN = "Win"
    DRAW = "Draw"
    LOSE = "Lose"

    WIN_SCORE = 6
    DRAW_SCORE = 3
    LOSE_SCORE = 0


class Result(abc.ABC):
    """Result of a Round of the R/P/S Game"""

    @property
    @abc.abstractmethod
    def result(self) -> ResultVars:
        """What is the result of the round"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def result_value(self) -> int:
        """What score this result is worth"""
        raise NotImplementedError


class Win(Result):
    """You Won!"""

    @property
    def result(self) -> ResultVars:
        """I am a WIN"""
        return ResultVars.WIN

    @property
    def result_value(self) -> int:
        """What I am Worth"""
        return ResultVars.WIN_SCORE.value


class Draw(Result):
    """You Drew :/"""

    @property
    def result(self) -> ResultVars:
        """I am a DRAW"""
        return ResultVars.DRAW

    @property
    def result_value(self) -> int:
        """What I am Worth"""
        return ResultVars.DRAW_SCORE.value


class Lose(Result):
    """You Lose :("""

    @property
    def result(self) -> ResultVars:
        """I am a LOSS"""
        return ResultVars.LOSE

    @property
    def result_value(self) -> int:
        """What I am Worth"""
        return ResultVars.LOSE_SCORE.value
