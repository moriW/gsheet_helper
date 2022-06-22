FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt ./

RUN apk add --no-cache git g++ musl-dev libffi-dev

RUN pip3 install -U pip

RUN pip3 install -U -r requirements.txt

COPY . .

EXPOSE 8888

CMD ["python", "app.py"]