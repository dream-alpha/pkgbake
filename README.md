# pkgbake
## A simple build tool for .ipk and .deb packages

## Usage 
- pkgbake `package_type` `git_root_dir` `package_dir`

## Description 
Parses the .mak files in the `git_root_dir` (and below) and generates an ipk or deb package
- `package_type` specifies the type of package ("deb" or "ipk")
- `git_root_dir` specifies the directory where the git source files are.
- `package_dir` specifies the directory where the package file will be placed.

## Prerequisite
A `git_root_dir/CONTROL/control` file is required with the following minimum content:
- Package: enigma2-plugin-extensions-`plugin_name`
- Version: `x.x`
- Architecture: `architecture`
