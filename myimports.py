# myimports.py

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
