# Insta360 Date Export Fixer

A simple Python utility to restore original creation dates for video files exported from Insta360 cameras.

## The Problem

When you export 360° videos or standard footage from the Insta360 desktop app (Insta360 Studio), the resulting `.mp4` files often lose their original "Date Created" metadata. They get a new creation date corresponding to the time of export.

This is a major headache for video editors (like DaVinci Resolve, Final Cut Pro, or Adobe Premiere) because clips appear out of order in the media pool, making it difficult to organize and edit multi-camera shoots or vacation footage.

## The Solution

This script solves the problem by:
1.  **Parsing** the original recording date and time directly from the Insta360 filename (e.g., `VID_20230815_143022_00_001.mp4` -> Aug 15, 2023, 14:30:22).
2.  **Applying** this date to all relevant metadata fields using [ExifTool](https://exiftool.org/).
3.  **Updating** the file system creation and modification dates for consistency in Finder/File Explorer.

## Prerequisites

The script requires **ExifTool** to be installed on your system.

### macOS
```bash
brew install exiftool
```

### Windows
1. Download the executable from the [ExifTool website](https://exiftool.org/).
2. Rename `exiftool(-k).exe` to `exiftool.exe`.
3. Add the folder containing `exiftool.exe` to your system PATH.

## Usage

### Option 1: Double-Click (macOS)
1.  Copy both `insta360_date_fixer.py` and `run_script_insta360_date_fixer.command` into the folder containing your video files.
2.  Double-click `run_script_insta360_date_fixer.command`.
3.  The script will automatically process all files in that folder.

### Option 2: Terminal (Any OS)
1.  Open your terminal/command prompt.
2.  Run the script providing the path to your video folder:

```bash
python insta360_date_fixer.py /path/to/your/videos
```

### Supported Formats
The script supports `.mp4`, `.mov`, `.insv`, and other common video formats used by Insta360.

## License
MIT