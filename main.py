from myimports import *
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
from constants import *
from functions import *
import codecs
import html
from bs4 import BeautifulSoup
from io import BytesIO, TextIOWrapper, BufferedReader


def main():
    for my_zip in glob.glob('*.zip'):
        print("________________________________________")

        # Define working data folder for current election
        data_wd = EXTRACT_DIR.joinpath(Path(my_zip).stem)

        # Retrieve election location from Readme.txt file
        current_state = get_location(my_zip)

        # Extract election zip file to data_wd
        with zipfile.ZipFile(my_zip) as zip_file:
            zip_file.extractall(data_wd)
            zip_file.close()

        if current_state == 'Alabama':
            # if *.txt are in root move to folder
            import_folder = mv_import(data_wd, False)



    print("________________________________________")


main()
