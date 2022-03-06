# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [norvyn.com](https://norvyn.com).

## [Unreleased]
## [3.5] -2021-04-07
### Fixed
- Fix Cut-Off start from Sunday instead of Monday.

## [3.4] -2021-03-01
### Changed
- 'IN' command can read machine contract start/stop date

## [3.3] -2021-02-22
### Changed
- Change main menu style

### Add
- Add 'w' to find out SSR information,
Not supported yet.

## [3.2] - 2021-02-21
### Fixed
- Fix available hours count mistake between cut-off cycle

## [3.1] - 2021-02-21
### Added
- Port specified move to the configure file, so you can connect to the host via port forward.
- Add visible process when running 'red'.
- Add Changelog to record code release.
- Once PMH has been read, just type 'z' to repeat the action.

### Changed
- Move log files to dir 'log'
- Use 'ce' to create PMH only need machine SN

### Fixed
- Fix 'red' function does not fit for year 2021
- replace('2020', '20') --> replace('20', '', 1')
- Fix machine model not been read when use 'ce' to create a PMH 

### Removed
- Nothing removed.
<include config files>

[Unreleased]: https://norvyn.com
[3.3]: https://norvyn.com
[3.2]: https://norvyn.com
[3.1]: https://norvyn.com