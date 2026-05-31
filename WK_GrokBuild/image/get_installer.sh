#!/bin/bash
set -euo pipefail

LOGFILE="get_installer.log"

curl -fsSL https://x.ai/cli/install.sh -o install-grok.sh
if [ ! -s "install-grok.sh" ];
then
 echo "錯誤：下載失敗或檔案為空！" | tee -a "$LOGFILE"
 exit 1
fi

date | awk '{printf "%s : ", $0}' >> "$LOGFILE"
md5sum install-grok.sh >> "$LOGFILE"

MAX_LINES=10000
Nlines=$(wc -l < "$LOGFILE" 2>/dev/null || echo 0)
if [ "$Nlines" -gt "$MAX_LINES" ];
then
 tail -n "$MAX_LINES" "$LOGFILE" > "${LOGFILE}.tmp"
 mv "${LOGFILE}.tmp" "$LOGFILE"
fi

chmod +x install-grok.sh
