FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -qq update && \
	apt-get install --no-install-recommends -y && \
	apt-get install --quiet --assume-yes python python-pip && \
	pip install mock

ENV  BUILD_DIR /opt/json2email
RUN mkdir -p ${BUILD_DIR}
COPY . ${BUILD_DIR}
WORKDIR ${BUILD_DIR}

RUN pip install . && \
	./run_tests.sh

CMD json2email
