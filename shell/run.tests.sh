#!/usr/bin/env bash

cd .. && source .venv/bin/activate || exit 1

printf "\nExporting environment\n"

set -a
source .env.test
set +a

export PYTHONUNBUFFERED=1

printf "\nWorking from: %s\n" "$(pwd)"

printf "\nStarting tests\n\n"

python3 -m unittest discover -s test/aidebate/app -p "*_test.py"
