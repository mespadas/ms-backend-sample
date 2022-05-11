FROM python:3.10

COPY requirements.txt ./requirements.txt
COPY app.py ./app.py
COPY users.db ./users.db

RUN pip install -r requirements.txt

CMD ["flask", "run"]