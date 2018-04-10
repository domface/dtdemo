
FROM python:3.6
MAINTAINER Dominik Andrzejczuk <dom@jawn.it>
EXPOSE 80 8000
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
COPY start.sh /app/start.sh


CMD ["/app/start.sh"]
