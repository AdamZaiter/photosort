# Photosort

Photosort is a Python CLI and GUI tool for sorting and archiving photos based on EXIF tags.

## Installation

**In terminal**

```shell
$ python setup.py install
```

**Executable file for Windows**

You just run the photosort.exe file from the exe folder.

## Usage

**CLI**

```shell
$ python photosort.py source_directory destination_directory

Options:
  --help  Show help
  -x      Removes source directory
  -m      Draws a google map with markers for coordinates of the photos

Example:
  python photosort.py C:\\Documents\\folder1 C:\\Documents\\folder2 -x -m
```
**CLI with GUI**

```shell
$ python photosort.py
```
## Note

The executable file for Windows doesn't have the 'draw a google map' functionality
