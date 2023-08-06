# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]
### Added
- :guardswoman: QuantumMachinesManager health check shows errors and warnings.
- :guardswoman: Fetching job results indicates if there were execution errors.
- :guardswoman: Define an element with multiple input ports.

## [0.3.1]
### Fixed
- Fixed serialization of IO values.
- Support running `QuantumMachinesManager` inside ipython or jupyter notebook.
### Changed
- Removing deprecation notice from `with_timestamps` method on result streams.
- Setting `time_of_flight` or `smearing` are required if element has `outputs` and
must not appear if it does not.

## [0.3.0]
### Changed
- Support for result fetching of both versions of QM Server.
- Now the SDK supports all version of QM server.

## [0.2.1]
### Changed
- Default port when creating new `QuantumMachineManager` is now `80` and user 
config file is ignored.

## [0.2.0]
### Added
- The original QM SDK for QOP 2.

## [0.1.0]
### Added
- The original QM SDK for QOP 1.

[Unreleased]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.1...HEAD
[0.3.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/qm-labs/qm-qua-sdk/releases/tag/v0.1.0

## Legend 
* :guardswoman: Developments that help detect and solve problems early.