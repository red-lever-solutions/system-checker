FROM python:3.5

MAINTAINER Johann Fuechsl <fuechsl@redlever.solutions>

VOLUME /config
VOLUME /status

WORKDIR /src
CMD ["python", "-m", "servicemonitor.app"]
