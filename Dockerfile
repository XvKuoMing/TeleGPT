FROM python:3.9-slim-buster
WORKDIR .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt-get install --yes gcc libsndfile1
RUN python -m venv /opt/venv
RUN PATH="/opt/venv/bin:$PATH"
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-u", "main.py"]