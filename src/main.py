from voice_automatisation import Assistant

assistant = Assistant(
    "Söder",
    [],
    model_path=r"voice_automatisation/models/vosk-model-small-de-0.15/vosk-model-small-de-0.15",
    verbose=True,
)
assistant.run()
