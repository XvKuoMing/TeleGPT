FROM python:3.9-slim-bookworm
WORKDIR .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update -y && \
    apt-get install -y --no-install-recomends gcc libsndfile1
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-u", "main.py"]