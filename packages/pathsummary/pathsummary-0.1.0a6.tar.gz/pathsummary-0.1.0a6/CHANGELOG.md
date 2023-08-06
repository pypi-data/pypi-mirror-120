# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.0a6] - 2021-09-23
### Changed
- No output is given if there is no result. Output was unintentionally the
  print of an empty pandas.DataFrame

## [0.1.0a5] - 2021-09-23
### Fixed
- Error raised if used onto an empty path. 
- Wrong version number in the CHANGELOG.

## [0.1.0a4] - 2021-09-23
### Fixed
- Missing dependency to click

## [0.1.0a3] - 2021-09-23
### Added
- FileTypes.VIDEO
- Recognition of 
  - .yml & .yaml as text/yaml
  - .cine as video/vision-research-cine
  - .md as text/markdown
  - .rst as text/restructured 

### Fixed
- broken link to code repository

## [0.1.0a2] - 2021-09-01
### Added
- Class FileTypes to replace constant FILETYPES_IMAGES
- *PathSummary.select*-method to filter for certain file types and sub types.

### Changed
- Edited docstring of PathSummary.iter_by_filetype

## [0.1.0a1] - unreleased
### Added
- Added pair *application/xml* to *text/xml* in the os-independent mimetypes.

## [0.1.0a0] - unreleased
### Added
- command line tool to summarize path and count occurrences.

## [0.0.1a1] - unreleased
### Added
- *filenames* property to *PathSummary*

## [0.0.1a0] - unreleased
Start of pathsummary.
