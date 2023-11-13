import voice_automatisation

vad = voice_automatisation.voice_activity_detection.VADetector()
model = voice_automatisation.recognition.Model(
    r"voice_automatisation/models/vosk-model-small-de-0.15/vosk-model-small-de-0.15"
)
interpreter = voice_automatisation.interpretation.CommandInterpreter([])

for segment in vad.listen():
    transcription = model.transcribe(segment)
    if (command := interpreter.associate(transcription)) is None:
        print(f"Could not decipher that bollocks: {transcription}")
    else:
        command.callback()
        print(f"Called a command: {command.identifier}")
