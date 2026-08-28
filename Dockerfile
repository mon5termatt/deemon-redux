FROM ubuntu:22.04

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt setup.py MANIFEST.in ./
COPY deemon ./deemon

RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir . && \
    mkdir -p /config /deemix /downloads /import /root/.config && \
    ln -s /config /root/.config/deemon-redux && \
    ln -s /deemix /root/.config/deemix

VOLUME /config /downloads /import /deemix

ENTRYPOINT ["deemon"]
CMD ["--help"]
