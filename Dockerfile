FROM tensorflow/tensorflow:2.13.0-gpu

RUN sed -i 's/archive.ubuntu.com/mirrors.cloud.tencent.com/g' /etc/apt/sources.list \
    && sed -i 's/security.ubuntu.com/mirrors.cloud.tencent.com/g' /etc/apt/sources.list \
    && apt-get update -y && apt-get install -y poppler-utils vim

RUN apt-get install -y vim wget gcc make automake libtool tk-dev libssl-dev libglib2.0-dev libsm6 libxrender1 libxext-dev libreadline-dev
RUN apt-get install -y libsqlite3-dev libbz2-dev liblzma-dev

COPY Python-3.10.12.tgz /opt
WORKDIR /opt
RUN tar -zxvf Python-3.10.12.tgz && cd Python-3.10.12 \
    && ./configure --prefix=/usr/local/python3.10.12 --enable-optimizations \
    && make -j16 install \
    && rm /usr/bin/python \
    && ln -s /usr/local/python3.10.12/bin/python3.10 /usr/bin/python3.10 \
    && ln -s /usr/local/python3.10.12/bin/pip3.10 /usr/bin/pip3.10

ADD . /ocsr
WORKDIR /ocsr
RUN pip3.10 config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
    && pip3.10 config set install.trusted-host mirrors.cloud.tencent.com \
    && pip3.10 install -r requirements.txt