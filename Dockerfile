FROM python:latest

# Set the working directory
RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
COPY src /app/src

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python3", "src/server.py"]
