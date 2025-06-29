FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg \
    chromium-driver chromium \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /application

COPY ./application .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
