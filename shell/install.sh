#!/usr/bin/env bash

set -euo pipefail

#@echo off

printf "\nCreating virtual environment\n"
python3 -m venv .venv

printf "\nActivating virtual environment\n"
source .venv/bin/activate

printf "\nInstalling dependencies\n"
python3 -m pip install --upgrade pip
python3 -m pip install -U langchain
python3 -m pip install arxiv
python3 -m pip install wikipedia
python3 -m pip install duckduckgo-search
python3 -m pip install -U langsmith
python3 -m pip install openai
python3 -m pip install google-search-results
python3 -m pip install -U langchain-community
python3 -m pip install -U langchain-openai
python3 -m pip install "pyu @ git+https://github.com/poshjosh/pyu@v0.1.2"

printf "\nSaving dependencies to requirements.txt\n"
pip freeze > src/aidebate/requirements.txt