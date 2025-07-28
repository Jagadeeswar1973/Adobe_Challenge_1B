FROM --platform=linux/amd64 python:3.10


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY challenge1b_input.json .

CMD ["python", "app/main.py"]
