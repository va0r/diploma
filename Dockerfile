FROM python:3.11-slim

RUN mkdir /code
WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY AnalyticsModule/ AnalyticsModule/
COPY ApplicationModule/ ApplicationModule/
RUN mkdir CSVData
COPY FixedVariables/ FixedVariables/
COPY LoguruModule/ LoguruModule/
COPY PostgresDBModule/ PostgresDBModule/
COPY TelegramMessengerModule/ TelegramMessengerModule/
COPY .env .env
COPY .env.docker .env.docker
COPY app.py app.py
