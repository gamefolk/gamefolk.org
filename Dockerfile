FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y python3-setuptools python3-mysql.connector nodejs nodejs-legacy npm git

RUN easy_install3 pip
RUN npm install -g grunt-cli

ADD . /src

WORKDIR /src
RUN pip install -r requirements.txt
RUN npm install
RUN grunt

EXPOSE 5000

CMD ["python3", "application.py"]
