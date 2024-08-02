FROM python:3.9-slim-bookworm
WORKDIR .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-u", "main.py"]