from voice_automatisation import device_selection, detection, recognition

device_index = None  # device_selection.dialog()
for segment in detection.listen(device_query=device_index):
    print(recognition.transcribe(segment))
