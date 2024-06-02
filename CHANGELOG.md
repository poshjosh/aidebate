# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Sync with host time, when in docker container.

## [0.0.3] - 2024-06-01

### Added 

- `requirements.in` for locking down versions of our dependencies.

### Changed

- Replaced environment variable `DOCKER_IMAGE_TAG` with `APP_VERSION` 

## [0.0.2] - 2024-05-29

### Added

- Containerization, using docker.

### Fixed

- Deprecation warnings by using langchain 0.2 specific methods.

## [0.0.1] - 2024-05-26

### Added

- CHANGELOG file.
- README file.
- Aidebate app modules.