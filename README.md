# File Organizer Script

Unique Python script to keep your directories clean by organizing files into subfolders based on their extensions.

## Features
- **Smart Categorization**: Groups files into `Images`, `Videos`, `Documents`, `Audio`, `Archives`, etc.
- **Interactive Input**: If you just run the script, it will ask you for the folder path.
- **Collision Handling**: Renames files if a file with the same name exists in the destination.
- **Dry Run Mode**: Preview changes without actually moving files.

## Usage

### 1. Interactive Mode (Easiest)
Just run the script:
```powershell
python organize_files.py
```
It will prompt:
```text
Enter the full path of the folder to organize:
```
Paste your path and hit Enter.

### 2. Command Line
Run the script passing the folder you want to organize:
```powershell
python organize_files.py "
```

### Dry Run (Preview)
To see what would happen without moving files:
```powershell
python organize_files.py --dry-run
```
(It will then ask for the path if you didn't provide it).

## Scheduling with Windows Task Scheduler
To run this automatically every day:
1.  Open **Task Scheduler**.
2.  Create a **Basic Task**.
3.  Set trigger to **Daily**.
4.  Action: **Start a program**.
5.  Program: `python` (or full path to python.exe).
6.  Arguments

Enjoy your organized files!
