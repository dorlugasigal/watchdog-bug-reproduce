FROM amd64/python:3.10-slim-buster

WORKDIR /usr/bin/app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-u", "./main.py" ]
