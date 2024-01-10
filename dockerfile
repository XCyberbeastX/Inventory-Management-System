FROM ubuntu:22.04

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libtiff-dev \
    libwebp-dev \
    libzbar0 \
    libzbar-dev \
    python3-serial \
    nano \
    git \
    iputils-ping \
    net-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /
RUN pip3 install -r /requirements.txt

# Optional: Packages for Raspberry Pi GPIO
COPY requirements_pi.txt /
RUN pip3 install -r /requirements_pi.txt

COPY . /server
WORKDIR /server

# Optional: Set environment variables
# the other values can be found in the config.py file
ENV LED_COUNT=68
ENV LED_PIN=18

EXPOSE 80

CMD ["python3", "app.py"]