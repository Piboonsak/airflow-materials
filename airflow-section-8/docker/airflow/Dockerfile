# VERSION 1.10.7
# AUTHOR: Matthieu "Puckel_" Roisil
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t puckel/docker-airflow .
# SOURCE: https://github.com/puckel/docker-airflow

FROM python:3.8-slim
LABEL maintainer="Piboonsak.262@gmail.com"

# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_UID
ARG AIRFLOW_GID

ARG AIRFLOW_VERSION=1.10.12
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

COPY ./requirements-python3.8.txt /requirements-python3.8.txt

# Disable noisy "Handling signal" log messages:
# ENV GUNICORN_CMD_ARGS --log-level WARNING

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        python3-dev \
        libsasl2-dev \
        libssl-dev \
        libexpat1-dev \
        libffi-dev \
        libgdbm-dev \
        libpq-dev \
        libbz2-dev \
        libczmq-dev \
        libsqlite3-dev \
        liblzma-dev \
        libncursesw5-dev \
        libreadline-dev \
        libc6-dev \
        zlib1g-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        krb5-user libpam-krb5 \
        net-tools inetutils-telnet iputils-ping libvips-tools iptotal \
        dnsutils bind9utils \
        ldap-utils libsasl2-modules-gssapi-mit \
        openssh-server adcli sssd sudo \
        gcc curl wget vim zip unzip \
        rsync vim htop \
        netcat \
        lsb-release \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install paramiko \
    && pip install sshtunnel \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install apache-airflow[crypto,celery,postgres,hdfs,hive,jdbc,mysql,docker,redis,ldap,slack,webhdfs,statsd,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} --constraint /requirements-python3.8.txt \
    && pip install 'redis==3.2' \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

# Set root for run inside container
USER root
SHELL ["/bin/bash", "-c"]

RUN chown -R airflow: ${AIRFLOW_USER_HOME}
RUN mkdir -p ${AIRFLOW_USER_HOME}/logs
RUN chmod -R 777 ${AIRFLOW_USER_HOME}
RUN chmod -R 755 /entrypoint.sh

EXPOSE 22 443 8443 8080 5555 8793

WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
