# debbake
## A simple build tool for .deb packages

## Usage 
- debbake `git_root_dir` `pkg_dir`

## Description 
Parses the .mak files in the `git_root_dir` (and below) and generates a deb package.
- `git_root_dir` specifies the directory where the git source files are.
- `pkg_dir` specifies the directory where the package file will be placed.

## Prerequisite
A `git_root_dir/CONTROL/control` file is required with the following minimum content:
- Package: enigma2-plugin-extensions-`plugin_name`
- Version: `x.x`
- Architecture: `architecture`
