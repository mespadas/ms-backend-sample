#FROM python:3.10
FROM public.ecr.aws/bitnami/python:3.10
COPY requirements.txt ./requirements.txt
COPY app.py ./app.py
COPY users.db ./users.db
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 -m venv venv
EXPOSE 5000
#EXPOSE 8000
#CMD ["flask", "run"]
CMD ["python", "app.py"]
