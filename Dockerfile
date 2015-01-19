FROM ubuntu:latest

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3-setuptools \
    libpython3-dev \
    python3-mysql.connector \
    libpcre3-dev \
    nodejs \
    nodejs-legacy \
    npm \
    git

RUN easy_install3 pip
RUN npm install -g bower

ADD . /src

WORKDIR /src
RUN pip install -r requirements.txt
RUN npm install
RUN bower install --allow-root

EXPOSE 5000

CMD ["python3", "application.py"]
