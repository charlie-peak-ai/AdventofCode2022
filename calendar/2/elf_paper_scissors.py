"""https://adventofcode.com/2022/day/2"""
import logging
from calendar import AdventOfCode
from typing import TextIO

from _exceptions import ActionsError, ResultsError
from _moves import Action, ActionVars, Paper, Rock, Scissors
from _results import Draw, Lose, Result, ResultVars, Win

logging.basicConfig(level=logging.INFO)


class RPSSimulator(AdventOfCode):
    """Rock, Paper, Scissors Simulator"""

    def __init__(self):
        super().__init__()

        self._var_name_to_class = {
            ResultVars.LOSE: Lose(),
            ResultVars.DRAW: Draw(),
            ResultVars.WIN: Win(),
            ActionVars.ROCK: Rock(),
            ActionVars.PAPER: Paper(),
            ActionVars.SCISSORS: Scissors(),
        }

        self.main()

    def main(self) -> None:
        """Main function"""
        # self.task_one(raw_data)
        self.task_two()

    def task_one(self) -> None:
        """Task one, simulate on the assumption the XYZ values are my moves."""
        logging.info("Task 1")
        my_score = 0
        for row in self.text_file:
            them, me = row.split(" ")

            them = self._move_code_translation(them)
            me = self._move_code_translation(me)

            result = self.compare_moves(me, them)
            round_score = self.calc_score(me, result)

            my_score += round_score
            logging.debug(
                f"{me.move_type.value:8} vs {them.move_type.value:8} = {result.result.value:4} "
                f"({me.move_value} + {result.result_value} = {round_score}) Running Total: {my_score}"
            )

        logging.info(f"Total score: {my_score}")

    def task_two(self) -> None:
        """Task two, convert the XYZ to the result I need and simulate that"""
        logging.info("Task 2")
        my_score = 0
        for row in self.text_file:
            them, desired_outcome = row.split(" ")

            them = self._move_code_translation(them)
            desired_outcome = self._desired_outcome_translation(desired_outcome)
            me = self.set_action_by_desired_outcome(desired_outcome, them)

            result = self.compare_moves(me, them)
            round_score = self.calc_score(me, result)

            my_score += round_score
            logging.info(
                f"{me.move_type.value:8} vs {them.move_type.value:8} = {result.result.value:4} "
                f"({me.move_value} + {result.result_value} = {round_score}) Running Total: {my_score}"
            )

        logging.info(f"Total score: {my_score}")

    @staticmethod
    def compare_moves(
        player_one_move: Action,
        player_two_move: Action,
    ) -> Result:
        """Compares two moves and determines the outcome"""

        if player_one_move.move_type == player_two_move.move_type:
            logging.debug("Moves match; Round is a draw")
            return Draw()

        elif player_one_move.move_type == player_two_move.weak_against:
            logging.debug("Player 2 is weak against this; Round is a win")
            return Win()

        elif player_one_move.move_type == player_two_move.strong_against:
            logging.debug("Player 2 is strong against this; Round is a loss")
            return Lose()

        else:
            raise ActionsError(f"Unexpected outcome between: {player_one_move.move_type} & {player_two_move.move_type}")

    @staticmethod
    def calc_score(move: Action, result: Result) -> int:
        """Taking the move played and the outcome, find the score for that round"""
        logging.debug("Extracting score values from the Action and Result objects")
        move_score = move.move_value
        result_score = result.result_value
        total_score = move_score + result_score

        return total_score

    def set_action_by_desired_outcome(
        self,
        desired_outcome: Result,
        them: Action,
    ) -> Action:
        """Depending on what"""
        if desired_outcome.result == ResultVars.WIN:
            logging.debug("I need to Win, setting to opponent's weakness")
            me = them.weak_against

        elif desired_outcome.result == ResultVars.DRAW:
            logging.debug("I need to Draw, setting to opponent type")
            me = them.move_type

        elif desired_outcome.result == ResultVars.LOSE:
            logging.debug("I need to Lose, setting to opponent's strength")
            me = them.strong_against

        else:
            raise ResultsError(f"Unexpected Result.result value: {desired_outcome.result}")

        return self._var_name_to_class.get(me)

    def _move_code_translation(self, move_code: str) -> Action:
        """Converts a move code string to a Variable type, then returns a Result Object"""

        if move_code in ["X", "Y", "Z"]:
            move_code = self._xyz_to_abc_translation(move_code)

        logging.debug("Converting Move Code to the Action it represents")
        abc_to_var_name = {
            "A": ActionVars.ROCK,
            "B": ActionVars.PAPER,
            "C": ActionVars.SCISSORS,
        }
        a = abc_to_var_name.get(move_code)

        return self._var_name_to_class.get(a)

    @staticmethod
    def _xyz_to_abc_translation(move_code: str) -> str:
        logging.debug("Converting Player 2 code to Player 1 equivalent")
        _xyz_to_abc = {
            "X": "A",
            "Y": "B",
            "Z": "C",
        }
        move_code = _xyz_to_abc.get(move_code)
        return move_code

    def _desired_outcome_translation(self, desired_outcome_code: str) -> Result:
        """Converts a desired outcome code string to a Variable type, then returns a Result Object"""
        logging.debug("Converting the desired outcome code to a Result object")
        xyz_to_var_name = {
            "X": ResultVars.LOSE,
            "Y": ResultVars.DRAW,
            "Z": ResultVars.WIN,
        }
        desired_outcome_code = xyz_to_var_name.get(desired_outcome_code)

        return self._var_name_to_class.get(desired_outcome_code)


if __name__ == "__main__":
    obj = RPSSimulator()
