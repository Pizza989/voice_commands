from voice_automatisation import Assistant, Command, Interaction, Keyword


def licht_an_oder_aus(feedback: str):
    if "an" in feedback:
        an = True
    elif "aus" in feedback:
        an = False
    else:
        return Interaction(
            "Entschuldigung das habe nicht verstanden.", lambda: None, False
        )

    if "küche" in feedback:
        if an:
            return Interaction("Ich schalte das Küchenlicht an.", lambda: None, False)
        else:
            return Interaction(
                "Ich schalte das Küchenlicht aus.", lambda a: None, False
            )
    else:
        return Interaction(
            "Entschuldigung das habe nicht verstanden.", lambda: None, False
        )


commands = [
    Command(
        "licht an/aus",
        keywords=(
            Keyword(("licht", "lampe", "beleuchtung"), 3),
            Keyword(("an", "aus", "schalten"), 1),
        ),
        interaction=Interaction("", licht_an_oder_aus, False),
    )
]


assistant = Assistant(
    "Assistent",
    commands,
    model_path=r"voice_automatisation/models/vosk-model-small-de-0.15/vosk-model-small-de-0.15",
    verbose=True,
)
assistant.run()
