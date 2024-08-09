FROM python:3.9-slim-bookworm
WORKDIR .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN sudo apt-get update -y && \
    sudo apt-get install --yes gcc libsndfile1
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-u", "main.py"]