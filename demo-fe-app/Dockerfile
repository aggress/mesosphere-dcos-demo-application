FROM python:alpine 

MAINTAINER rshaw@mesosphere.com

RUN pip install flask

COPY demo-fe-app.py /demo-fe-app.py

EXPOSE 5000

ENTRYPOINT ["python", "/demo-fe-app.py"]