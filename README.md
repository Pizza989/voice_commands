# Voice Automatisation

This is a project implementing a speech based command system to automate whatever with python functions. The purpose of this is to have an offline voice assistant (like alexa, siri etc.).

## Specifications

This uses a volume threshold for voice activity detection, vosk-based speech recognition and a score based command selection system.

## Limitations

Text-To-Speech is not yet supported but will be implemented in the future.

## Config

Configuration is done in the config package of voice_automatisation. The `config.json` must define "input_device_query" and will be populated with "input_device_info" and "vad":

- **"input_device_info/rate"**: what samplerate to use universally for audio data within the package
- **"input_device_info/noise_level"**: this is the peak volume (no unit) of noise that was determined by `config/__init__.py:make_default_config`
- **"input_device_info/speech_level"**: this is the peak volume (no unit) of speech that was determined by `config/__init__.py:make_default_config`
- **"input_device_info/min_speech_volume_ration"**: this is used to determine when someone is speaking. the default of 0.2 means that speech is detected at 20% of the `speech_level`
- **"vad/noise_level"** will be populated by `config/__init__.py:make_default_config`
- **"vad/speech_level"** will be populated by `config/__init__.py:make_default_config`
- **"vad/min_speech_volume_ratio"** user defined but defaults to 0.2 if left out: the threshold of when audio is classified as speech is set as follows: threshhold = min_speech_volume_ratio \* (speech_level - noise_level)

_(Im using slashed to depict membership of the right side to the left)_\

## Usage

The `Assistant` class defines high level access to the packages functions. It can be given a wake word a list of commands and the path to the vosk model. This Path has to be a raw string literal an must point to a directory containing a directory with the model files. I don't know why.

Example

```python
from voice_automatisation import Assistant

assistant = Assistant(wake_word="test", commands=[], model_path=r"", verbose=True)
assistant.run()
```

Furthermore the class `Assistant` provides events that can be overriden when subclassing it. For more information see `voice_automatisation/assistant.py:Assistant`

## How it works

### Assistant.run()

Upon calling `assistant.run()` it will start waiting for the voice activity detection to give it an audio segment, once that happens it gives this segment to the model which returns a transcription. This transcription is then passed to the command-interpreter which returns the associated command or None:

- In the first case the command will be run
- In the second case nothing happens besides calling the fitting event

## Executing and defining Commands

`voice_automatisation/dataclasses.py` defines three structures:

```python
@dataclass
class Keyword:
    synonyms: tuple[str]
    weight: float


@dataclass
class Command:
    identifier: str
    keywords: tuple[Keyword]
    interaction: Interaction


@dataclass
class Interaction:
    text: str
    callback: Callable

```

An example command could look like this:

```python
command = Command(
    identifier="play/pause",
    keywords=(Keyword(("play", "pause"), 1), Keyword(("playback",), 3))
    interaction=Interaction(
        "I'll start playing", callback=lambda: subprocess.call(["xdotool", "key", "XF86AudioPlay"])
    )
)
```
