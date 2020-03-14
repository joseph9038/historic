FROM python:3.7.7-stretch

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD python app.py