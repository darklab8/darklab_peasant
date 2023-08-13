FROM python:3.10

WORKDIR /install

COPY docker/google-chrome-stable_current_amd64.deb chrome.deb
RUN apt update && apt install -y ./chrome.deb

RUN apt install tesseract-ocr -y

COPY requirements.txt constraints.txt ./
RUN pip install -r requirements.txt -c constraints.txt

WORKDIR /code
COPY peasant peasant
COPY data data
COPY pytest.ini ./

RUN mkdir -p docker/chromedriver
COPY docker/chromedriver/114.0.5735.90 docker/chromedriver/114.0.5735.90