from .command import Command


def calculate_command_score(command: Command, text: str) -> float:
    score = 0
    text = text.lower()
    for keyword in command.keywords:
        if keyword.word in text:
            score += keyword.weight

    return score


def get_associated_command(
    command_list: list[Command], transcription: dict, score_threshold: float
) -> Command:
    text = transcription["text"]
    selected_command = None
    highscore = 0
    for command in command_list:
        score = calculate_command_score(command, text)
        if score > highscore and score >= score_threshold:
            selected_command = command

    return selected_command
