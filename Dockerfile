FROM python:3.12-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

COPY src/ .

CMD ["python", "main.py"]
