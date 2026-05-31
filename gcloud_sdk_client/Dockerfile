FROM ubuntu:26.04

LABEL org.opencontainers.image.authors="kaiyi"

RUN apt update -y && apt-get install -y vim net-tools ssh
RUN apt-get install -y apt-transport-https ca-certificates gnupg curl sudo

ARG USERNAME
ARG USER_GROUP=${USERNAME}
ARG UID=1000
ARG GID=${UID}

ADD set_user.sh /root/set_user.sh
RUN chmod +x /root/set_user.sh
RUN /root/set_user.sh ${UID} ${GID} ${USERNAME} ${USER_GROUP}
RUN getent passwd ${UID} | cut -d: -f1 > /root/build_user

WORKDIR /home/${USERNAME}
USER ${USERNAME}
