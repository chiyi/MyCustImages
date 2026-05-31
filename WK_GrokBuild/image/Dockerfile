FROM ubuntu:26.04

MAINTAINER kaiyi

ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Taipei
RUN apt update -y && apt install -y vim g++ git curl ca-certificates && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/grok_build
ENV GROK_BIN_DIR=/app/grok_build
ENV PATH="/app/grok_build:${PATH}"
COPY install-grok.sh /app/grok_build/

WORKDIR /app/grok_build

# Rebuild if grok update new version / podman image rm wk_grokbuild

RUN /app/grok_build/install-grok.sh && \
    rm -f grok agent && \
    cp -f /root/.grok/downloads/grok-linux-x86_64 grok && \
    cp -f /root/.grok/downloads/grok-linux-x86_64 agent && \
    chmod 755 grok agent && \
    ls -l && \
    ./grok --version && \
    echo "✅ Grok CLI 已成功安裝到 /app/grok_build"

RUN mkdir /work-dir

