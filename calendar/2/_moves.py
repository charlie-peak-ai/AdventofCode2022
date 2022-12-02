"""All the underlying classes used in the R/P/S game"""
import abc
from enum import Enum


class ActionVars(Enum):
    """Variables used by Actions in the game, useful in comparisons and to avoid hard coded values"""

    ROCK = "Rock"
    PAPER = "Paper"
    SCISSORS = "Scissors"

    ROCK_VALUE = 1
    PAPER_VALUE = 2
    SCISSORS_VALUE = 3


class Action(abc.ABC):
    """Abstract class for a "move" in the game"""

    @property
    @abc.abstractmethod
    def move_type(self) -> ActionVars:
        """What move this is"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def weak_against(self) -> ActionVars:
        """What beats this move"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def strong_against(self) -> ActionVars:
        """What this move beats"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def move_value(self) -> int:
        """What score this move gets per round"""
        raise NotImplementedError


class Rock(Action):
    """The Mighty Rock"""

    @property
    def move_type(self) -> ActionVars:
        """I am ROCK"""
        return ActionVars.ROCK

    @property
    def weak_against(self) -> ActionVars:
        """PAPER Kills Me"""
        return ActionVars.PAPER

    @property
    def strong_against(self) -> ActionVars:
        """I Kill SCISSORS"""
        return ActionVars.SCISSORS

    @property
    def move_value(self) -> int:
        """What I am Worth"""
        return ActionVars.ROCK_VALUE.value


class Paper(Action):
    """The Unsuspecting Paper"""

    @property
    def move_type(self) -> ActionVars:
        """I am PAPER"""
        return ActionVars.PAPER

    @property
    def weak_against(self) -> ActionVars:
        """SCISSORS Kills Me"""
        return ActionVars.SCISSORS

    @property
    def strong_against(self) -> ActionVars:
        """I Kill ROCK"""
        return ActionVars.ROCK

    @property
    def move_value(self) -> int:
        """What I am Worth"""
        return ActionVars.PAPER_VALUE.value


class Scissors(Action):
    """The Crafty Scissors"""

    @property
    def move_type(self) -> ActionVars:
        """I am SCISSORS"""
        return ActionVars.SCISSORS

    @property
    def weak_against(self) -> ActionVars:
        """ROCK Kills Me"""
        return ActionVars.ROCK

    @property
    def strong_against(self) -> ActionVars:
        """I Kill PAPER"""
        return ActionVars.PAPER

    @property
    def move_value(self) -> int:
        """What I am Worth"""
        return ActionVars.SCISSORS_VALUE.value
