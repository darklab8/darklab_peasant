# Define custom function directory
ARG FUNCTION_DIR="/function"

FROM python:3.10

WORKDIR /install

COPY docker/google-chrome-stable_current_amd64.deb chrome.deb
RUN apt update && apt install -y ./chrome.deb

RUN apt install tesseract-ocr -y

RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin

COPY requirements.txt constraints.txt ./
RUN pip install -r requirements.txt -c constraints.txt

# Include global arg in this stage of the build
ARG FUNCTION_DIR
RUN pip install awslambdaric

WORKDIR /code
RUN mkdir -p docker/chromedriver
COPY docker/chromedriver/114.0.5735.90 docker/chromedriver/114.0.5735.90

COPY peasant peasant
COPY data data
COPY pytest.ini ./


# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "peasant.lambda_function.handler" ]