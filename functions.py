# functions.py
import builtins
import os
import sys
import re
from pathlib import Path
import glob
import pandas as pd
import shutil
import zipfile
import time
import pikepdf
from halo import Halo
from pikepdf import Pdf
from pdfCropMargins import crop
import fnmatch
import random
import string
import glob
import pathlib
import constants
from constants import *
from functions import *
import codecs
import html
from bs4 import BeautifulSoup
from io import BytesIO, TextIOWrapper, BufferedReader

# Function to check how many files with defined extension exist in the directory


def filecount(y_pdf, path='.'):
    return len(fnmatch.filter(os.listdir(path), y_pdf))


def get_location(zipf):
    try:
        filename = 'Readme.txt'

        with zipfile.ZipFile(zipf, 'r') as zfile:
            for name in zfile.namelist():
                if re.search(r'\.ezip$', name) is not None:
                    zfiledata = BytesIO(zfile.read(name))
                    with zipfile.ZipFile(zfiledata) as zfile2:
                        for name2 in zfile2.namelist():
                            if name2 == filename:
                                readme = zfile2.read(filename)
        location_data = BeautifulSoup(readme, "html.parser").prettify().splitlines()[8]
        da = re.split("[/|:|\n]", location_data)
        location = constants.Location(rmdigit(da[2]), da[3])
        assert location.county is not None and 'ElectionWare' not in location.county
    except IOError:
        print(" Unable to open Readme.txt")
    except AssertionError:
        print(" Location missing from ESS data")
    else:
        print(" Found election data for:")
        print(" County: ", location.county.title())
        print(" State:  ", location.state.title())
        return location.state.title()


def create_dir(data_wd, dir_name, overwrite=bool):
    try:
        data_wd.joinpath(dir_name).mkdir(parents=True, exist_ok=(not overwrite))
        return Path(dir_name)
    except IOError:
        # print("Unable to create folder. Creating a new folder with random name.")
        random_folder = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        data_wd.joinpath(random_folder).mkdir(parents=True, exist_ok=True)
        return random_folder


def mk_dir(data_wd, new_folder, overwrite=bool):
    try:
        data_wd.joinpath(new_folder).mkdir(parents=True, exist_ok=(not overwrite))
    except IOError:
        shutil.rmtree(data_wd, new_folder)
        data_wd.mkdir(parents=True, exist_ok=False)


def numb():
    while True:
        try:
            return int(input('Please enter a number: '))
        except ValueError:
            pass


def mv_import(data_wd, overwrite=True):
    try:
        # Create Import folder in current directory
        if filecount('*.txt', str(data_wd)):
            import_folder = create_dir(data_wd, IMPORT_DIR, overwrite)
            # Copy files in current folder with *.txt to Import folder
            for src_file in data_wd.glob('*.txt'):
                shutil.copy(src_file, data_wd.joinpath(import_folder))
            print(" Copied *.txt to", import_folder)
            return import_folder
        else:
            return print(" No .txt files to move")
    except shutil.SameFileError:
        return print(" Unable to copy import files to folder.")



def extract_zip(wd_folder, a_zip, overwrite=bool(False)):
    zip_path = wd_folder.joinpath(a_zip)
    zip_folder = zip_path.stem
    print(wd_folder, a_zip)

    i = 0
    for i in range(2):
        i = +1
        try:
            zi = zipfile.ZipFile(zip_path)
            zip_folder = create_dir(wd_folder, zip_folder, type(overwrite))
            zi.extractall(wd_folder.joinpath(zip_folder))
            zi.close()
            return zip_folder
        except KeyboardInterrupt:
            # print(wd_folder.joinpath(zip_folder), " ", zip_path)
            print("Unable to create zip folder. Creating a new folder with random name.")


'''          except KeyboardInterrupt:
                print('ah')
         except BaseException:
                print("idk bro")
        except AttributeError:
            print("Path is fucked")
            break
        except FileNotFoundError:
            print("File not found")
            print(" ", zip_path)
            break

    if a_zip.stem != zip_folder:
        return Path(zip_folder)
'''


def rmdigit(value):
    if value[1].isdigit():
        return " ".join(value.split()[1:])
    elif value[0] == ' ':
        return value[1:]
    else:
        return value


def getpath(x_path):
    return os.path.join(os.path.dirname(os.path.realpath(x_path)), x_path)


def getmultipath(x):
    for files in glob.glob(x):
        print(getpath(files))
    else:
        pass


def custompdf(l_pdf, path='.'):
    x = 0
    for files in glob.glob(l_pdf):
        if files and filecount(l_pdf, path) <= 11:
            # print(file)
            # print(os.path.dirname(os.path.realpath(file)))
            print(os.path.join(os.path.dirname(os.path.realpath(files)), files))
        else:
            print("    There can only be 1 .pdf for every .zip")
            input("\n    Press Enter to exit...\n")
            input() * ()
            # sys.exit(1)
        x += 1
    return 0
