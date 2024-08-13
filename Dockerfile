FROM python:3.9-slim-bookworm
WORKDIR .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-u", "main.py"]