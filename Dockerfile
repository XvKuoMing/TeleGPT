FROM python:3.9-slim-bookworm
WORKDIR .
RUN python -m venv venv && source venv/bin/activate
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1
CMD ["python", "-u", "main.py"]