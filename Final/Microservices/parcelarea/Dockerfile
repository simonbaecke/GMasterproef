FROM python:3.9-alpine

ENV FLASK_APP=flaskr
ENV FLASK_DEBUG=1

WORKDIR /app
COPY . /app

RUN pip install --editable .
EXPOSE 3000

CMD [ "flask", "run", "--host=0.0.0.0" ]