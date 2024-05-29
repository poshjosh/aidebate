#!/usr/bin/env bash

cd .. || exit 1

# Add `BUILDKIT_PROGRESS=plain` before the docker-compose command
# to log output of the build process.
docker-compose -p aidebate up -d