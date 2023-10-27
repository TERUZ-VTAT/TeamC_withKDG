FROM ubuntu

RUN apt-get update
RUN apt-get install python3 python3-pip -y

RUN pip3 install flask
RUN pip3 install mysql-connector-python

RUN mkdir /app

CMD ["python3","app/flask_application/app.py"]