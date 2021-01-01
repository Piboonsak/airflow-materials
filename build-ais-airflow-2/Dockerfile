# Base Image
FROM python:3.8-slim
LABEL maintainer="MarcLamberti"

# Arguments that can be set with docker build
ARG AIRFLOW_VERSION=1.10.12
ARG AIRFLOW_HOME=/usr/local/airflow

# Export the environment variable AIRFLOW_HOME where airflow will be installed
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

# Install dependencies and tools
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \ 
    build-essential \
    ldap-utils \    
    libczmq-dev \
    curl wget git \
    libssl-dev \
    libssl1.1 \
    lsb-release \
    sudo \
    inetutils-telnet \
    bind9utils freetds-dev \
    libkrb5-dev \
    libsasl2-dev libsasl2-2 libsasl2-modules sasl2-bin \
    libffi-dev libpq-dev \
    libffi6 \
    freetds-bin build-essential \
    default-libmysqlclient-dev \
    apt-utils \
    rsync \
    zip \
    unzip \
    gcc \
    vim \
    sqlite3 unixodbc \
    htop \
    locales \
    && apt-get clean

COPY ./requirements-python3.8.txt /requirements-python3.8.txt

# Upgrade pip
# Create airflow user 
# Install apache airflow with subpackages
RUN pip install --upgrade pip==20.2.4 && \
    useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow && \
    pip install apache-airflow[crypto,celery,postgres]==${AIRFLOW_VERSION} --constraint /requirements-python3.8.txt
# Copy the entrypoint.sh from host to container (at path AIRFLOW_HOME)
COPY ./entrypoint.sh ./entrypoint.sh

# Set the entrypoint.sh file to be executable
RUN chmod +x ./entrypoint.sh

# Set root for run inside container
USER root

SHELL ["/bin/bash", "-c"]

# add airflow user
#RUN useradd -m airflow && echo "airflow:airflow" | 
RUN chpasswd && adduser airflow sudo

# Set the owner of the files in AIRFLOW_HOME to the user airflow
RUN chown -R airflow: ${AIRFLOW_HOME}

# Set the username to use
#USER airflow

# Set workdir (it's like a cd inside the container)
WORKDIR ${AIRFLOW_HOME}

# Create the dags folder which will contain the DAGs
RUN mkdir dags

# Expose ports (just to indicate that this container needs to map port)
EXPOSE 8080

# Execute the entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

    
