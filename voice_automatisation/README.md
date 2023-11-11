# Voice Automatisation
This is a project implementing a speech based command system to automate whatever with python functions. The purpose of this is to have an offline voice assistant (like alexa, siri etc.).

## Specifications
This uses a volume threshold for voice activity detection, openai's whisper model for transcription and a score based command selection system.

## Limitations
Interactivity and Text-To-Speech are not yet supported but will be implemented soon.

## Config
Configuration is done in the config package voice_automatisation. The `config.json` defines global standards:
+ **"samplerate"**: what samplerate to use universally for audio data within the package
+ **"noise_level"**: this is the peak volume (no unit) of noise that was determined by `config/calibration.py`
+ **"speech_level"**: this is the peak volume (no unit) of speech that was determined by `config/calibration.py`
+ **"min_speech_volume_ration"**: this is used to determine when someone is speaking. the default of 0.2 means that speech is detected at 20% of the `speech_level`

## Request Cycle
Whenever `core/detection.py` detects speech it will wait for the person to finish and then return an audio segment. This segment goes the the Request Cycle.

1. It gets transcribed
2. The transcription is interpreted and associated with a command
3. The selected command is executed
4. Go back to detecting

Some steps are taken in their respective modules:
+ `core/detection.py`
+ `core/recognition.py`
+ `core/interpretation.py`
