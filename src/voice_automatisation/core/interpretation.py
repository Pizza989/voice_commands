import math
import string

from ..types import Command


class CommandInterpreter:
    """This implements the Interpreting-Procedure. Subclass this and override its methods to change its behaviour."""

    def __init__(
        self, commands: list[Command], wake_word: str, similarity_threshold: int = 0.8
    ) -> None:
        self.commands = commands
        self.wake_word = self.format_text(wake_word)
        self.similarity_threshold = similarity_threshold

    @staticmethod
    def format_text(text) -> str:
        """Returns lowercase `text` without punctuation

        Args:
            text (_type_): the text

        Returns:
            str: `text` without punctuation and lowercase
        """
        return text.translate(str.maketrans("", "", string.punctuation)).lower()

    @staticmethod
    def get_similarity(str1: str, str2: str) -> float:
        """Calculates the jaccard-simularity of two strings

        Args:
            str1 (_type_): str1
            str2 (_type_): str2

        Returns:
            float: similarity in percent
        """
        set1 = set(str1.split())
        set2 = set(str2.split())
        intersection_size = len(set1.intersection(set2))
        union_size = len(set1.union(set2))

        return intersection_size / union_size if union_size != 0 else 0

    def calculate_word_score(self, word: str, text: str) -> float:
        """Gets the similarity for each word from text and `word` and returns the highscore

        Args:
            word (str): the word
            text (str): the transcription

        Returns:
            float: highscore
        """
        highscore = 0
        for word2 in text.split():
            similarity = self.get_similarity(word, word2)
            if similarity > highscore:
                highscore = similarity

        return highscore

    def calculate_command_score(self, command: Command, text: str) -> float:
        """Calculates the score of a command given the transcribed text by
        taking into account the weight of each keyword (synonyms are
        treated as options but they are ordered hierarchically) and its
        length. The highest scoring synonyms score + sqrt of its length
        adds to score if it is greater then similarity_threshold though

        Args:
            command (Command): the command
            text (str): the transcribed text

        Returns:
            float: the commands score as element of [0; oo[
        """
        score = 0
        for keyword in command.keywords:
            synonym_highscore = 0
            leading_synonym = None
            for synonym in keyword.synonyms:
                synonym_score = self.calculate_word_score(synonym, text)
                if synonym_score > synonym_highscore:
                    synonym_highscore = synonym_score
                    leading_synonym = synonym

            if synonym_highscore >= self.similarity_threshold:
                score += synonym_score + math.sqrt(len(leading_synonym))

        return score

    def associate(self, transcription: str, score_threshold: float = 0) -> Command:
        """Gets the command from `self.command_list` that has the highest score

        Args:
            transcription (str): the transcription
            score_threshold (float, optional): Minimum score that a command has to reach to be counted.
                                               If no command reaches the threshold `None` is returned. Defaults to 0.

        Returns:
            Command: _description_
        """
        text = self.format_text(transcription)
        selected_command = None
        highscore = 0
        for command in self.commands:
            score = self.calculate_command_score(command, text)
            if score > highscore and score >= score_threshold:
                selected_command = command

        return selected_command

    def is_wake_word(self, transcription: str):
        if (
            self.calculate_word_score(self.wake_word, self.format_text(transcription))
            >= self.similarity_threshold
        ):
            return True
        return False
