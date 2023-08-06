# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]
### Added
- :guardswoman: QuantumMachinesManager health check shows errors and warnings.
- :guardswoman: Fetching job results indicates if there were execution errors.
- :guardswoman: Define an element with multiple input ports.

## [0.3.1] - 2021-09-13
### Fixed
- Fixed serialization of IO values.
- Support running `QuantumMachinesManager` inside ipython or jupyter notebook.
### Changed
- Removing deprecation notice from `with_timestamps` method on result streams.
- Setting `time_of_flight` or `smearing` are required if element has `outputs` and
must not appear if it does not.

## [0.3.0] - 2021-09-03
### Changed
- Support for result fetching of both versions of QM Server.
- Now the SDK supports all version of QM server.

## [0.2.1] - 2021-09-01
### Changed
- Default port when creating new `QuantumMachineManager` is now `80` and user 
config file is ignored.

## [0.2.0] - 2021-08-31
### Added
- The original QM SDK for QOP 2.

## [0.1.0] - 2021-08-31
### Added
- The original QM SDK for QOP 1.

[Unreleased]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.1...HEAD
[0.3.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/qm-labs/qm-qua-sdk/releases/tag/v0.1.0

## Legend 
* :guardswoman: Features that are server specific and depend on capabilities and version