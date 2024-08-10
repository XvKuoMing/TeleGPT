FROM python:3.9-slim-buster
WORKDIR .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt-get install --yes build-essential gcc-8 g++-8 libstdc++-8-dev libsndfile1
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . .
RUN pip install ffmpeg
RUN pip install -r requirements.txt
CMD ["python", "-u", "main.py"]