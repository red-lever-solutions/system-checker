FROM python:3.5

MAINTAINER Johann Fuechsl <fuechsl@redlever.solutions>

VOLUME /config
VOLUME /status
VOLUME /logs

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

WORKDIR /src
CMD ["python", "-m", "systemchecker.app"]
