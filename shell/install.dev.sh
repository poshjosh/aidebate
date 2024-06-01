#!/usr/bin/env bash

###############################################################################
# Run this script so that the `aidebate` package is available for test modules. #
###############################################################################

cd .. && source .venv/bin/activate || exit 1

python3 -m pip install -e .
