FROM ubuntu:22.04

MAINTAINER kaiyi

RUN apt update -y && apt-get install -y vim net-tools ssh
RUN apt-get install -y apt-transport-https ca-certificates gnupg curl sudo

ARG USERNAME
ARG USER_GROUP=${USERNAME}
ARG UID=1000
ARG GID=${UID}

RUN set -ex \
    && groupadd -g ${GID} ${USER_GROUP} \
    && useradd -m -u ${UID} -g ${GID} --create-home --home-dir /home/${USERNAME} ${USERNAME} \
    && adduser ${USERNAME} sudo \
    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

WORKDIR /home/${USERNAME}
USER ${USERNAME}

