# Local file updater
> A package that allows to backup local files to a specific directory and update already backuped files if they were modified

## Install

`pip install file-updater`

## Console script

`lofup.py [Source path] [Destination path] (optional: Path to .fupignore or .fupinclude file)`

Example:

![sample_1](https://user-images.githubusercontent.com/48239596/127472933-66bf1f94-bbce-47dd-b112-18442645ce3d.PNG)

## How to use in code

```python
from fup.updater import FileUpdater

file_updater = FileUpdater(output_console=True)

file_updater.update_files(
    path_source=r'C:\Users\riffe\schule\5.klasse\pos\docs', 
    path_dest=r'C:\Users\riffe\spare\programming\file-update-testfolder')
```

## Ignore or include files

You can also ignore or include files by providing a full or relative path to a .fupignore or .fupinclude file. If you specify
a .fupignore file, all files will be included by default except files that are affected by the .fupignore file. However, if you specify a .fupinclude file, all files will be ignored by default.

```python
from fup.updater import FileUpdater

file_updater = FileUpdater(output_console=True, fup_file_path=r'C:\Temp\.fupignore.txt')
```

Example for such a file:

```

# full paths
c:\Temp\From\text4.docx
c:\Temp\From\sub

# relative paths (need to have exclamation mark at the start of the line)
!sub\text3.docx

# ignore or include certain file extensions
*.txt
```
