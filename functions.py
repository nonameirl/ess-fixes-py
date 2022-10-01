# functions.py
import shutil
import zipfile
from glob import glob

import constants

from myimports import *


# Function to check how many files with defined extension exist in the directory


def filecount(y_pdf, path='.'):
    return len(fnmatch.filter(os.listdir(path), y_pdf))


def get_location(data_wd, folder=None, overwrite=False):
    try:
        if folder is None:
            ext_folder = extract_zip(data_wd, BOD_ZIP, overwrite)
        else:
            ext_folder = data_wd.joinpath(folder)
        f = open(data_wd.joinpath(ext_folder, README_FILE))
        spl = str(f.readlines()[8])
        f.close()
        da = re.split("[/|:|\n]", spl)
        location = Location(rmdigit(da[2]), da[3])
        assert location.county is not None and 'ElectionWare' not in location.county
    except IOError:
        print("Unable to open Readme.txt")
    except AssertionError:
        print("Location missing from ESS data")
    else:
        print("Found location data")
        print("County: ", location.county)
        print("State: ", location.state)


def create_dir(data_wd, dir_name, overwrite=bool):
    try:
        data_wd.joinpath(dir_name).mkdir(parents=True, exist_ok=(not overwrite))
        return dir_name
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


def mv_import(data_wd):
    try:
        # Create Import folder in current directory
        if filecount('*.txt', str(data_wd)):
            import_folder = create_dir(data_wd, IMPORT_DIR)
            # Copy files in current folder with *.txt to Import folder
            for src_file in data_wd.joinpath(glob('*.txt')):
                shutil.copy(src_file, import_folder)
            return import_folder
        else:
            return print("No .txt files to move")
    except IOError:
        print("Unable to copy import files to folder.")
    else:
        print("Import files copied to ", import_folder)
        return import_folder


def extract_zip(wd_folder, a_zip, overwrite=False):
    zip_path = wd_folder.joinpath(a_zip)
    zip_folder = zip_path.stem

    i = 0
    for i in range(2):
        i = +1
        try:
            zi = zipfile.ZipFile(zip_path)
            zip_folder = create_dir(wd_folder, zip_folder, overwrite)
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


def print_loc(dal):
    print(dal[2][0])
    print(f"{dal[0]}:\t{dal[2]}")
    print(f"{dal[1]}:\t{dal[3]}")


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
            input * ()
            # sys.exit(1)
        x += 1
    return 0
