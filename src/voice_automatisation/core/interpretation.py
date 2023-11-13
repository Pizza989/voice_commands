import math
import string

from ..command import Command


def remove_punctuation(text) -> str:
    return text.translate(str.maketrans("", "", string.punctuation))


def jaccard_similarity(str1, str2) -> float:
    set1 = set(str1.split())
    set2 = set(str2.split())
    intersection_size = len(set1.intersection(set2))
    union_size = len(set1.union(set2))

    return intersection_size / union_size if union_size != 0 else 0


def calculate_synonym_score(synonym: str, text: str) -> float:
    highscore = 0
    for word in text.split():
        similarity = jaccard_similarity(synonym, word)
        if similarity > highscore:
            highscore = similarity

    return highscore


def calculate_command_score(
    command: Command, text: str, similarity_threshold: float = 0.8
) -> float:
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
    text = text.lower()
    for keyword in command.keywords:
        synonym_highscore = 0
        leading_synonym = None
        for synonym in keyword.synonyms:
            synonym_score = calculate_synonym_score(synonym, text)
            if synonym_score > synonym_highscore:
                synonym_highscore = synonym_score
                leading_synonym = synonym

        if synonym_highscore > similarity_threshold:
            score += synonym_score + math.sqrt(len(leading_synonym))

    return score


def get_associated_command(
    command_list: list[Command], transcription: dict, score_threshold: float = 0
) -> Command:
    text = remove_punctuation(transcription).lower()
    selected_command = None
    highscore = 0
    for command in command_list:
        score = calculate_command_score(command, text)
        if score > highscore and score >= score_threshold:
            selected_command = command

    return selected_command
