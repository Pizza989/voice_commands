FROM python:3.11

WORKDIR /src

COPY . /

RUN apt-get update && apt-get install -y portaudio19-dev

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]