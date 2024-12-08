FROM python:3.10-slim

RUN pip install --upgrade pip
RUN pip install uvicorn

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./bloqit /app/bloqit
COPY ./setup.py /app/setup.py
COPY ./data /app/data
RUN pip install /app/

WORKDIR /app

CMD ["uvicorn", "--workers", "1", "--host", "0.0.0.0", "--port", "8000", "bloqit.main:app"]
