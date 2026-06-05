FROM ubuntu:26.04

MAINTAINER kaiyi

ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Taipei
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        sudo \
        vim \
        g++ git \
        curl ca-certificates \
        python3 python-is-python3 pip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/grok_build
ENV GROK_BIN_DIR=/app/grok_build \
    PATH="/app/grok_build:${PATH}" \
    TERM=xterm-256color \
    COLORTERM=truecolor \
    LANG=en_US.UTF-8
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
RUN usermod -aG sudo ubuntu
RUN bash -c 'echo "ubuntu ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu && chmod 0440 /etc/sudoers.d/ubuntu'
