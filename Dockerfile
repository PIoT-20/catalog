FROM python:3.11-slim

WORKDIR /app

copy . /app

# Create virtual environment
RUN python -m venv ./venv


RUN pip3 install --no-cache-dir .
EXPOSE 8080

CMD ["python3", "-m", "src.api"]
