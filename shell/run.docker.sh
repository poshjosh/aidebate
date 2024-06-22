#!/usr/bin/env bash

cd .. || exit 1

# To log output of the build process.
export BUILDKIT_PROGRESS=plain

docker-compose -p aidebate up -d