#!python3
import ctypes
import json
import os
import sys
import win32con
import win32file

def isDirReparsePoint(dir):
    """Determines if directory is a symbolic link."""
    if not os.path.exists(dir):
        raise FileNotFoundError
    attr = win32file.GetFileAttributes(dir)
    if not (attr & win32con.FILE_ATTRIBUTE_DIRECTORY):
        raise TypeError('"{0}" is not a directory'.format(dir))
    return bool(attr & win32con.FILE_ATTRIBUTE_REPARSE_POINT)

try:
    confFile = open('test-config.json')
    conf = json.load(confFile)
except ValueError as err:
    print('Error loading config file:\n{0}'.format(err))
    exit()
except FileNotFoundError:
    print('Config file does not exist.')
    exit()

for item in conf:
    origin = item['directories']['origin']
    symlink = item['directories']['symlink']
    if not os.path.exists(origin):
        print('Origin folder "{0}" does not exist, check config.'.format(origin))
        exit()

    if os.path.exists(symlink):
        if isDirReparsePoint(symlink):
            print('Already a symbolic link, skipping. "{0}"'.format(symlink))
    else:
        try:
            win32file.CreateSymbolicLink(symlink, origin, win32file.SYMBOLIC_LINK_FLAG_DIRECTORY)
            if isDirReparsePoint(symlink):
                print('Symbolic link created successfully, "{0}" -> "{1}"'.format(symlink, origin))
            else:
                print('Symbolic link not created for unknown reason. "{0}" -> "{1}"'.format(symlink, origin))
        except Exception as err:
            print('Unknown error: {0}'.format(err))


confFile.close()
