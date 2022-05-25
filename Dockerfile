FROM python:3

WORKDIR /bot

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "src/bot.py" ]