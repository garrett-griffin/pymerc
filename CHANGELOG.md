# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

# [0.6.0] - 2024-06-02

### Added

- Higher level objects for building operations and recipes

### Changed

- Operations are now loaded and handled separately
- Models have been updated for the latest game release

# [0.5.0] - 2024-05-24

### Added

- Higher level objects for storehouse and transports
- Higher level objects for dealing with imports/exports
- Support for getting current operations of a building
- Several properties for performing routine calculations on items
- Support for buying, selling, and managing items across buildings/transports

### Changed

- README updated with example usage code

# [0.4.0] - 2024-05-20

### Added

- Adds support for businesses endpoint
- Adds support for buildings endpoint
- Adds support for turn endpoint
- Adds several higher level game objects to make API usage easier
- Adds towns method

### Changed

- Makes async code a bit more efficient

## [0.3.0] - 2024-05-17

### Added

- Utility function for calculating number of structures in a town

### Changed

- Minor updates to reflect latest API state


## [0.2.0] - 2024-05-14

### Added

- The filename holding static data is now determined dynamically instead of being hardcoded

### Changed

- The `towns.get_market_data` function now shows the correct return type
- All function names have been made consistent (i.e., `get_` for functions that retrieve data)

## [0.1.0] - 2024-05-14

### Added

- Initial release

[unreleased]: https://github.com/jmgilman/pymerc/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/jmgilman/pymerc/compare/v0.6.0
[0.5.0]: https://github.com/jmgilman/pymerc/compare/v0.5.0
[0.4.0]: https://github.com/jmgilman/pymerc/compare/v0.4.0
[0.3.0]: https://github.com/jmgilman/pymerc/releases/tag/v0.3.0
[0.2.0]: https://github.com/jmgilman/pymerc/releases/tag/v0.2.0
[0.1.0]: https://github.com/jmgilman/pymerc/releases/tag/v0.1.0