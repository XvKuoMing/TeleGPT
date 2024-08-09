FROM python:3.9-slim-bookworm
WORKDIR .
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1
CMD ["python", "-u", "main.py"]