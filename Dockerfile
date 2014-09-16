FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y python3-setuptools nodejs nodejs-legacy npm git

RUN easy_install3 pip
RUN npm install -g grunt-cli

ADD . /src
RUN pip install -r src/requirements.txt
RUN cd src; npm install
RUN cd src; grunt

EXPOSE 5000

CMD ["python3", "/src/application.py"]
