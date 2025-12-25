#!/usr/bin/env python3
"""
Insta360 Date Fixer
Restores original creation dates for video files exported from Insta360 cameras.

Author: Ilia
Usage: python insta360_date_fixer.py <folder_path>
"""

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def parse_filename_date(filename):
    """
    Parses date and time from filename format: VID_YYYYMMDD_HHMMSS_*.mp4
    Returns a datetime object or None if parsing fails.
    """
    # Pattern to extract date and time: VID_YYYYMMDD_HHMMSS
    pattern = r'VID_(\d{8})_(\d{6})'
    match = re.match(pattern, filename)
    
    if match:
        date_str = match.group(1)  # YYYYMMDD
        time_str = match.group(2)  # HHMMSS
        
        try:
            # Convert to datetime object
            year = int(date_str[:4])
            month = int(date_str[4:6])
            day = int(date_str[6:8])
            hour = int(time_str[:2])
            minute = int(time_str[2:4])
            second = int(time_str[4:6])
            
            return datetime(year, month, day, hour, minute, second)
        except ValueError as e:
            print(f"Error parsing date for file {filename}: {e}")
            return None
    return None

def set_video_metadata_date(file_path, target_datetime):
    """
    Sets the creation date in video metadata using ExifTool.
    Updates critical date fields read by video editors like DaVinci Resolve.
    """
    try:
        # Format date for ExifTool (YYYY:MM:DD HH:MM:SS)
        formatted_date = target_datetime.strftime("%Y:%m:%d %H:%M:%S")
        
        # ExifTool command to update important date fields
        # -overwrite_original: do not create backup files
        # -api QuickTimeUTC: handle timezone correctly for QuickTime files
        cmd = [
            'exiftool',
            '-overwrite_original',
            '-api', 'QuickTimeUTC',
            f'-CreateDate={formatted_date}',
            f'-ModifyDate={formatted_date}',
            f'-MediaCreateDate={formatted_date}',
            f'-MediaModifyDate={formatted_date}',
            f'-TrackCreateDate={formatted_date}',
            f'-TrackModifyDate={formatted_date}',
            f'-QuickTime:CreateDate={formatted_date}',
            f'-QuickTime:ModifyDate={formatted_date}',
            str(file_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Also update file system date for consistency
            set_file_creation_date(file_path, target_datetime)
            return True
        else:
            print(f"ExifTool error for {file_path}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Exception while setting metadata for {file_path}: {e}")
        return False

def set_file_creation_date(file_path, target_datetime):
    """
    Sets the file creation and modification dates at the file system level.
    This ensures consistency in Finder (macOS) and File Explorer.
    """
    try:
        # Use ExifTool to set FileCreateDate and FileModifyDate
        formatted_date = target_datetime.strftime("%Y:%m:%d %H:%M:%S")
        
        cmd = [
            'exiftool',
            '-overwrite_original',
            f'-FileCreateDate={formatted_date}',
            f'-FileModifyDate={formatted_date}',
            str(file_path)
        ]
        
        subprocess.run(cmd, capture_output=True, text=True)
        return True
        
    except Exception as e:
        print(f"Error setting file system date for {file_path}: {e}")
        return False

def check_exiftool_installed():
    """
    Checks if ExifTool is installed and accessible in the system path.
    """
    try:
        result = subprocess.run(['exiftool', '-ver'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"ExifTool found (version {result.stdout.strip()})")
            return True
        return False
    except FileNotFoundError:
        return False

def process_video_files(folder_path):
    """
    Processes all supported video files in the specified folder.
    """
    if not os.path.exists(folder_path):
        print(f"Directory {folder_path} does not exist.")
        return
    
    # Supported video file extensions
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.m4v', '.insv'}
    
    processed_count = 0
    error_count = 0
    
    print(f"Processing folder: {folder_path}")
    print("-" * 50)
    
    # Convert to Path object for easier handling
    dir_path = Path(folder_path)
    
    for file_path in dir_path.iterdir():
        # Check if it's a file and has a supported extension
        if file_path.is_file() and file_path.suffix.lower() in video_extensions:
            filename = file_path.name
            print(f"Processing file: {filename}")
            
            # Parse date from the filename
            parsed_date = parse_filename_date(filename)
            
            if parsed_date:
                print(f"  Parsed date: {parsed_date}")
                
                # Apply date to video metadata
                if set_video_metadata_date(file_path, parsed_date):
                    print(f"  ✅ Metadata updated successfully")
                    processed_count += 1
                else:
                    print(f"  ❌ Failed to update metadata")
                    error_count += 1
            else:
                print(f"  ⚠️ Could not parse date from filename")
                error_count += 1
            
            print()
    
    print("-" * 50)
    print("Process completed:")
    print(f"  Successfully processed: {processed_count} files")
    print(f"  Errors encountered: {error_count}")

def main():
    """
    Main entry point for the script.
    """
    if len(sys.argv) != 2:
        print("Usage: python insta360_date_fixer.py <folder_path>")
        print("Example: python insta360_date_fixer.py /Users/username/Videos/Insta360")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    # Check for ExifTool availability
    if not check_exiftool_installed():
        print("❌ ExifTool not found!")
        print("This script requires ExifTool to function.")
        print("\nInstallation instructions:")
        print("  macOS: brew install exiftool")
        print("  Other systems: https://exiftool.org/install.html")
        sys.exit(1)
    
    process_video_files(folder_path)

if __name__ == "__main__":
    main()
