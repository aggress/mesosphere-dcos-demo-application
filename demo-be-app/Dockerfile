FROM python:alpine 

MAINTAINER rshaw@mesosphere.com

RUN pip install flask

COPY demo-be-app.py /demo-be-app.py

EXPOSE 5000

ENTRYPOINT ["python", "/demo-be-app.py"]

