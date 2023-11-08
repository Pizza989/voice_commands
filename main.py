from voice_automatisation import detection

for buffer in detection.listen():
    print(buffer)
