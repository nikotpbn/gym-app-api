FROM python:3.13-alpine3.22

WORKDIR /backend

EXPOSE 8000

COPY /requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
