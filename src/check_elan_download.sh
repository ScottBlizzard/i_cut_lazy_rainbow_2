#!/usr/bin/env bash
set -u

cd /workspace/thymic_project/paper/iclr_2/outputs || exit 1

urls=(
  "https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh"
  "https://gh.llkk.cc/https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh"
  "https://ghproxy.net/https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh"
  "https://mirror.ghproxy.com/https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh"
)

for u in "${urls[@]}"; do
  echo "URL: $u"
  if timeout 20 wget -q -O elan-init-test.sh "$u"; then
    wc -c elan-init-test.sh
    head -1 elan-init-test.sh
    exit 0
  fi
  echo "failed"
done

exit 1

