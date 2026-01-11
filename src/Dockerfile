FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install  -r requirements.txt

COPY . .

#create directory to persist sqlite data on ec2 instance
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]