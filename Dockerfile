FROM python:3

# Install and use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /bot

COPY . .

CMD [ "python3", "src/bot.py" ]