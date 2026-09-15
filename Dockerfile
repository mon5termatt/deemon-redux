FROM ubuntu:22.04

WORKDIR /app

COPY requirements.txt setup.py MANIFEST.in README.md ./
COPY deemon ./deemon
COPY docker/entrypoint.sh /entrypoint.sh

# Build deps needed for pycryptodomex (no wheel on some arches); removed after install.
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-dev \
        gcc \
        build-essential \
        tzdata && \
    chmod +x /entrypoint.sh && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir . && \
    apt-get purge -y --auto-remove gcc build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /config /deemix /downloads /import /root/.config && \
    ln -s /config /root/.config/deemon-redux && \
    ln -s /deemix /root/.config/deemix

VOLUME /config /downloads /import /deemix

ENV TZ=UTC

ENTRYPOINT ["/entrypoint.sh"]
CMD ["--help"]
