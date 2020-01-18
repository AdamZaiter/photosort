# photosort

photosort is a Python CLI and GUI tool for sorting and archiving photos based on EXIF tags.

## Installation

**In terminal**

```
$ python setup.py install
```

**Executable file for Windows**

You just run the photosort.exe file from the exe folder.

## Usage

**CLI**

```
$ python photosort.py source_directory destination_directory

Options:
  --help  Show help
  -x      Removes source directory
  -m      Draws a google map with markers for coordinates of the photos
          When a marker is clicked, GPS coordinates are shown.
  -v      Adds verbosity

Example:
  python photosort.py C:\\Documents\\folder1 C:\\Documents\\folder2 -x -m
```
**CLI with GUI**

```
$ python photosort.py
```

![photosort](https://user-images.githubusercontent.com/39188731/69559441-3ec24f00-0faa-11ea-88b8-4ab85d618802.png)

## Note

The executable file for Windows doesn't have the 'draw a google map' functionality
