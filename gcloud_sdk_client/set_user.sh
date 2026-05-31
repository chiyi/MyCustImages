#!/bin/bash
set -ex

echo UID=${UID}
GID=$2
USERNAME=$3
USER_GROUP=$4

# 檢查 GID 是否已存在，若不存在則創建群組
if [ ! getent group ${GID} > /dev/null];
then
 groupadd -g ${GID} ${USER_GROUP}; \
fi
# 檢查 UID 是否已存在，若不存在則創建使用者
if [ ! getent passwd ${UID} > /dev/null];
then
 useradd -m -u ${UID} -g ${GID} --create-home --home-dir /home/${USERNAME} ${USERNAME};
fi
# 將使用者加入 sudo 群組並設定免密碼權限
USER=$(getent passwd ${UID} | cut -d: -f1)
usermod -aG sudo "${USER}"
echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
