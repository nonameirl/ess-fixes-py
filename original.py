import pandas as pd
import pathlib
import shutil
import glob
import zipfile
import os
import re
import time
import sys
import re
import pikepdf
from halo import Halo
# from pikepdf import _cpphelpers
from pikepdf import Pdf
from pdfCropMargins import crop

path = "."
extension = ".zip"


def directory(path, extension):
    list_dir = []
    list_dir = os.listdir(path)
    count = 0
    for file in list_dir:
        if file.endswith(extension):  # eg: '.txt'
            count += 1
    return count


multizip = directory(path, extension)
multipdf = directory('.', '.pdf')

# print(multizip)

d2d = 0
d2d_exists = 0
for file in glob.glob(r'*2D*.pdf'):
    if file:
        # print(file, 'exists')
        d2d = file
        d2d_exists = 1
    else:
        # print('file not exists')
        continue

if (multizip == 1 and multipdf <= 1) or (multizip > 1 and d2d_exists == False):
    print("________________________________________")
    for my_zip in glob.glob(r".\\*.zip"):
        print("\n    " + my_zip[2:-4] + " election data")
        if re.search('GEN.zip', my_zip):
            zip_dir = os.path.splitext(my_zip)[0]

            # print(os.getcwd())
            zip_dir = os.path.splitext(my_zip)[0]
            # print(my_zip)
            if os.path.exists('extracted/' + zip_dir):
                shutil.rmtree('extracted/' + zip_dir)
                os.makedirs('extracted/' + zip_dir)
            else:
                os.mkdir('extracted/' + os.path.splitext(my_zip)[0])

            with zipfile.ZipFile(my_zip) as zip_file:
                zip_file.extractall('extracted/' + os.path.splitext(my_zip)[0])
                zip_file.close()

                os.chdir('.\extracted' + zip_dir)

                # Create Import folder in current directory
                pathlib.Path('Import').mkdir(parents=True, exist_ok=True)

                # Define files and folder path for copy
                dir_path = (r".")
                txt_path = glob.glob("*.txt")
                dest_txt_dir_path = (r"Import")

                # Copy files in current folder with *.txt to Import folder
                for txt_path in txt_path:
                    txt_name = txt_path.split("""\\""")[-1]
                    txt_dest_full_path = dest_txt_dir_path + """\\""" + txt_name
                    shutil.copy(txt_path, txt_dest_full_path)  ## copy the file

                # DATA CRUNCHING AND COMPARISON SECTION #

                # Read Candidates.txt file and assign only the 'Import Office ID' column for comparison
                df2 = pd.read_csv(r'Candidates.txt', encoding='UTF-16', on_bad_lines='skip', skiprows=1, sep='|',
                                  usecols=['Import Office ID'])

                # Read Offices.txt file with '|' delimiter and a header define on line 1
                df1 = pd.read_csv(r'Offices.txt', encoding='UTF-16', on_bad_lines='skip', sep='|', header=1,
                                  keep_default_na=False)

                # If values in column 'Import Office ID' in df1 does not exist in column 'Import Office ID' in df2 then delete the row in df1.
                new_df = df1[df1['Import Office ID'].isin(df2['Import Office ID'])]

                # Overwrite Offices.txt with updated version
                new_df.to_csv('Import/Offices.txt', sep='|', index=False)

                one_line = "$$Offices$$\n"

                with open("Import/Offices.txt", 'r+') as fp:
                    lines = fp.readlines()  # lines is list of line, each element '...\n'
                    lines.insert(0, one_line)  # you can use any index if you know the line index
                    fp.seek(0)  # file pointer locates at the beginning to write the whole file again
                    fp.writelines(lines)  # write whole lists again to the same file

                # creating a variable and storing the text
                search_text = "False"

                # creating a variable and storing the text
                replace_text = "false"

                # Opening our text file in read only
                # mode using the open() function
                with open(r'Import/Offices.txt', 'r') as file:

                    # Reading the content of the file
                    # using the read() function and storing
                    # them in a new variable
                    data = file.read()

                    # Searching and replacing the text
                    # using the replace() function
                    data = data.replace(search_text, replace_text)

                # Opening our text file in write only
                # mode to write the replaced content
                with open(r'Import/Offices.txt', 'w') as file:

                    # Writing the replaced data in the text file
                    file.write(data)

                # ZIP IT ALL UP SECTION #

                # File list for ZIP function
                list_files = ['ROTATION.xlsx', 'BallotOnDemand_Export.ezip', 'Import\Languages.txt',
                              'Import\Offices.txt', 'Import\Parties.txt', 'Import\Poll Places.txt',
                              'Import\Poll Relations.txt', 'Import\Precincts.txt', 'Import\Questions.txt',
                              'Import\Registered Voters.txt', 'Import\Candidate Level Text.txt',
                              'Import\Candidates.txt', 'Import\Contest Level Text.txt', 'Import\District Relations.txt',
                              'Import\District Types.txt', 'Import\Districts.txt', 'Import\Headings.txt',
                              'Import\Language Candidate Level Text.txt', 'Import\Language Candidates.txt',
                              'Import\Language Contest Level Text.txt', 'Import\Language Districts.txt',
                              'Import\Language Groups.txt', 'Import\Language Headings.txt',
                              'Import\Language Offices.txt', 'Import\Language Parties.txt',
                              'Import\Language Poll Places.txt', 'Import\Language Precincts.txt',
                              'Import\Language Questions.txt']
                #                print(os.getcwd())

                #                print(zip_dir)
                with zipfile.ZipFile("../../completed" + zip_dir + '_fixed.zip', 'w') as zipF:
                    for file in list_files:
                        zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)

                os.chdir("../../")

                if zip_dir + '_fixed.zip':
                    print('\n    Files have been compressed')
                    if d2d_exists:
                        two_d_dump = '../../2d/'
                        if os.path.exists('../../2d'):
                            # print(zip_dir)
                            shutil.move(crop_path + d2d, two_d_dump + d2d)
                        else:
                            os.mkdir('../../2d')
                            shutil.move(crop_path + d2d, two_d_dump + d2d)
                pathlib.Path('zips').mkdir(parents=True, exist_ok=True)

                source = (my_zip)
                destination = ("./zips")

                filename = os.path.basename(source)
                dest = os.path.join(destination, filename)
                shutil.move(source, dest)
                print('\n    The files has been compressed\n')
                print("    Pausing for suspense")
                print("________________________________________")
                time.sleep(2)
        else:
            d2d = 0
            d2d_exists = 0
            if not os.path.exists('extracted'):
                os.mkdir('extracted')

            # print(os.getcwd())
            zip_dir = os.path.splitext(my_zip)[0]
            #           print(my_zip)
            if os.path.exists('extracted/' + zip_dir):
                shutil.rmtree('extracted/' + zip_dir)
                os.makedirs('extracted/' + zip_dir)
            else:
                os.mkdir('extracted' + os.path.splitext(my_zip)[0])

            with zipfile.ZipFile(my_zip) as zip_file:
                zip_file.extractall('extracted' + os.path.splitext(my_zip)[0])
                zip_file.close()

                os.chdir('./extracted/' + zip_dir)

                shutil.copyfile('..\..\Mapping Templates.xlsx', 'Mapping Templates.xlsx')

                multi_in_pdf = directory('.', '.pdf')

                for file in glob.glob(r'*2D*.pdf'):
                    if file and multi_in_pdf == 1:
                        # print(file, 'exists')
                        d2d = file
                        d2d_exists = 2
                    elif multi_in_pdf >= 2:
                        print("\n    Multiple 2D PDF files detected in " + my_zip)
                        print("\n    Please correct or remove before running again\n")
                        input("\n    Press Enter to exit...\n")
                        sys.exit(1)

#                print(os.getcwd())

                for fname in glob.glob('*.xlsx'):
                    if re.match('Mapping Templates.xlsx', fname):
                        continue
                    else:
                        os.replace(fname, 'Rotations.xlsx', )

                # DATA CRUNCHING AND COMPARISON SECTION #

                path = 'Export Files'
                if os.path.exists(path):
                    precinct_folder = 'Export Files'
                else:
                    precinct_folder = 'Import Files'
                # print(os.getcwd())
                # Read Precincts.txt file

                print("\n    Adding Split IDs to data\n")
                # data = pd.read_csv (precinct_folder + "/Precincts.txt",encoding='UTF-16', on_bad_lines='skip', header=1,sep='|',keep_default_na=False)
                data = pd.read_csv(precinct_folder + "/Precincts.txt", encoding='UTF-16', on_bad_lines='skip', header=1,
                                   sep='|', dtype=object)

                # Read Offices.txt file with '|' delimiter and a header define on line 1
                data['Split ID'] = data['Split Name'].str.split(' ', n=1).str.get(-1).str.rjust(4, '0').replace('0000',
                                                                                                                '')
                if data['Split Name'].str.contains("/", na=False).sum() > 0:
                    print("    The data in " + zip_dir[2:] + " contains a slash in the sname eg. 'ISD 13\ISD 16' ")
                    input("\n    Press Enter to continue...")
                    print("\033[A                             \033[A")

                # Overwrite Offices.txt with updated version
                data.to_csv(precinct_folder + "/Precincts.txt", sep='|', index=False)

                one_line = "$$Precincts$$\n"

                with open(precinct_folder + "//Precincts.txt", 'r+') as fp:
                    lines = fp.readlines()  # lines is list of line, each element '...\n'
                    lines.insert(0, one_line)  # you can use any index if you know the line index
                    fp.seek(0)  # file pointer locates at the beginning to write the whole file again
                    fp.writelines(lines)  # write whole lists again to the same file

                if d2d_exists != 0:
                    spinner = Halo(text='.   Cropping and splitting 2D PDFs', spinner='dots', interval='700',
                                   placement='right')
                    spinner.start()
                    # print("wemadeit")
                    file2pages = {
                        0: [0, 2],
                        1: [2, 4],
                        2: [4, 6],
                        3: [6, 8],
                        4: [8, 10],
                        5: [10, 12],
                        6: [12, 14],
                        7: [14, 16],
                        8: [16, 18],
                        9: [18, 20],
                        10: [20, 22],
                        11: [22, 24],
                        12: [24, 26],
                        13: [26, 28],
                        14: [28, 30],
                        15: [30, 32],
                        16: [32, 34],
                        17: [34, 36],
                        18: [36, 38],
                        19: [38, 40],
                        20: [40, 42],
                        21: [42, 44],
                        22: [44, 46],
                        23: [46, 48],
                        24: [48, 50],
                        25: [50, 52],
                        26: [52, 54],
                        27: [54, 56],
                        28: [56, 58],
                        29: [58, 60],
                        30: [60, 62],
                        31: [62, 64],
                        32: [64, 66],
                        33: [66, 68],
                        34: [68, 70],
                        35: [70, 72],
                        36: [72, 74],
                        37: [74, 76],
                        38: [76, 78],
                        39: [78, 80],
                        40: [80, 82],
                        41: [82, 84],
                        42: [84, 86],
                        43: [86, 88],
                        44: [88, 90],
                        45: [90, 92],
                        46: [92, 94],
                        47: [94, 96],
                        48: [96, 98],
                        49: [98, 100],
                        50: [100, 102],
                        51: [102, 104],
                        52: [104, 106],
                        53: [106, 108],
                        54: [108, 110],
                        55: [110, 112],
                        56: [112, 114],
                        57: [114, 116],
                        58: [116, 118],
                        59: [118, 120],
                        60: [120, 122],
                        61: [122, 124],
                        62: [124, 126],
                        63: [126, 128],
                        64: [128, 130],
                        65: [130, 132],
                        66: [132, 134],
                        67: [134, 136],
                        68: [136, 138],
                        69: [138, 140],
                        70: [140, 142],
                        71: [142, 144],
                        72: [144, 146],
                        73: [146, 148],
                        74: [148, 150],
                        75: [150, 152],
                        76: [152, 154],
                        77: [154, 156],
                        78: [156, 158],
                        79: [158, 160],
                        80: [160, 162],
                        81: [162, 164],
                        82: [164, 166],
                        83: [166, 168],
                        84: [168, 170],
                        85: [170, 172],
                        86: [172, 174],
                        87: [174, 176],
                        88: [176, 178],
                        89: [178, 180],
                        90: [180, 182],
                        91: [182, 184],
                        92: [184, 186],
                        93: [186, 188],
                        94: [188, 190],
                        95: [190, 192],
                        96: [192, 194],
                        97: [194, 196],
                        98: [196, 198],
                        99: [198, 200],
                        100: [200, 202],
                        101: [202, 204],
                        102: [204, 206],
                        103: [206, 208],
                        104: [208, 210],
                        105: [210, 212],
                        106: [212, 214],
                        107: [214, 216],
                        108: [216, 218],
                        109: [218, 220],
                        110: [220, 222],
                        111: [222, 224],
                        112: [224, 226],
                        113: [226, 228],
                        114: [228, 230],
                        115: [230, 232],
                        116: [232, 234],
                        117: [234, 236],
                        118: [236, 238],
                        119: [238, 240],
                        120: [240, 242],
                        121: [242, 244],
                        122: [244, 246],
                        123: [246, 248],
                        124: [248, 250],
                        125: [250, 252],
                        126: [252, 254],
                        127: [254, 256],
                        128: [256, 258],
                        129: [258, 260],
                        130: [260, 262],
                        131: [262, 264],
                        132: [264, 266],
                        133: [266, 268],
                        134: [268, 270],
                        135: [270, 272],
                        136: [272, 274],
                        137: [274, 276],
                        138: [276, 278],
                        139: [278, 280],
                        140: [280, 282],
                        141: [282, 284],
                        142: [284, 286],
                        143: [286, 288],
                        144: [288, 290],
                        145: [290, 292],
                        146: [292, 294],
                        147: [294, 296],
                        148: [296, 298],
                        149: [298, 300],
                        150: [300, 302],
                        151: [302, 304],
                        152: [304, 306],
                        153: [306, 308],
                        154: [308, 310],
                        155: [310, 312],
                        156: [312, 314],
                        157: [314, 316],
                        158: [316, 318],
                        159: [318, 320],
                        160: [320, 322],
                        161: [322, 324],
                        162: [324, 326],
                        163: [326, 328],
                        164: [328, 330],
                        165: [330, 332],
                        166: [332, 334],
                        167: [334, 336],
                        168: [336, 338],
                        169: [338, 340],
                        170: [340, 342],
                        171: [342, 344],
                        172: [344, 346],
                        173: [346, 348],
                        174: [348, 350],
                        175: [350, 352],
                        176: [352, 354],
                        177: [354, 356],
                        178: [356, 358],
                        179: [358, 360],
                        180: [360, 362],
                        181: [362, 364],
                        182: [364, 366],
                        183: [366, 368],
                        184: [368, 370],
                        185: [370, 372],
                        186: [372, 374],
                        187: [374, 376],
                        188: [376, 378],
                        189: [378, 380],
                        190: [380, 382],
                        191: [382, 384],
                        192: [384, 386],
                        193: [386, 388],
                        194: [388, 390],
                        195: [390, 392],
                        196: [392, 394],
                        197: [394, 396],
                        198: [396, 398],
                    }

                    zipn = "BallotOnDemand_Export.ezip"
                    zip_obj = zipfile.ZipFile(zipn, "r")
                    zip_obj.extractall("BallotOnDemand_Export")
                    zip_obj.close()

                    bodnum = directory(os.getcwd() + '/BallotOnDemand_Export', 'NON.pdf')
                    # print(os.getcwd() + '/BallotOnDemand_Export')
                    # print(bodnum)

                    if d2d_exists == 1:
                        crop_path = "../../"
                    else:
                        crop_path = "./"

                    # print(crop_path + d2d)
                    # print(os.getcwd())
                    crop(["-p", "0", "-ap", "18", crop_path + d2d, "-o2D_cropped.pdf"])

                    d2d_split = d2d.split('\\')[-1].split('.')[0]

                    # print(d2d_split)
                    # pdf = Pdf.open(d2d_split + "_cropped.pdf")
                    # filename = d2d_split + "_cropped.pdf"
                    filename = "2D_cropped.pdf"
                    pdf = Pdf.open(filename)

                    # make the new splitted PDF files
                    new_pdf_files = [Pdf.new() for i in file2pages]
                    # the current pdf file index
                    new_pdf_index = 0

                    mtt = 0
                    # iterate over all PDF pages
                    for n, page in enumerate(pdf.pages):
                        if n in list(range(*file2pages[new_pdf_index])):
                            # add the `n` page to the `new_pdf_index` file
                            new_pdf_files[new_pdf_index].pages.append(page)
                            # print(f"[*] Assigning Page {n} to the file {new_pdf_index}")
                        elif new_pdf_index < 9:
                            mtt = 1
                            # make a unique filename based on original file name plus the index
                            output_filename = f"01-0000{new_pdf_index + 1}-01-NON.pdf"
                            # save the PDF file
                            new_pdf_files[new_pdf_index].save(output_filename)
                            # print(f"[+] File: {output_filename} saved.")
                            # go to the next file
                            new_pdf_index += 1
                            # add the `n` page to the `new_pdf_index` file
                            new_pdf_files[new_pdf_index].pages.append(page)
                            # print(f"[*] Assigning Page {n} to the file {new_pdf_index}")
                        elif new_pdf_index < 99:
                            mtt = 2
                            # make a unique filename based on original file name plus the index
                            output_filename = f"01-000{new_pdf_index + 1}-01-NON.pdf"
                            # save the PDF file
                            new_pdf_files[new_pdf_index].save(output_filename)
                            # print(f"[+] File: {output_filename} saved.")
                            # go to the next file
                            new_pdf_index += 1
                            # add the `n` page to the `new_pdf_index` file
                            new_pdf_files[new_pdf_index].pages.append(page)
                            # print(f"[*] Assigning Page {n} to the file {new_pdf_index}")
                        else:
                            mtt = 3
                            # make a unique filename based on original file name plus the index
                            output_filename = f"01-00{new_pdf_index + 1}-01-NON.pdf"
                            # save the PDF file
                            new_pdf_files[new_pdf_index].save(output_filename)
                            # print(f"[+] File: {output_filename} saved.")
                            # go to the next file
                            new_pdf_index += 1
                            # add the `n` page to the `new_pdf_index` file
                            new_pdf_files[new_pdf_index].pages.append(page)
                            # print(f"[*] Assigning Page {n} to the file {new_pdf_index}")

                    # save the last PDF file

                    if mtt == 1:
                        name, ext = os.path.splitext(filename)
                        output_filename = f"01-0000{new_pdf_index + 1}-01-NON.pdf"
                        new_pdf_files[new_pdf_index].save(output_filename)
                        # print(f"[+] File: {output_filename} saved.")
                    elif mtt == 2:
                        aname, ext = os.path.splitext(filename)
                        output_filename = f"01-000{new_pdf_index + 1}-01-NON.pdf"
                        new_pdf_files[new_pdf_index].save(output_filename)
                        # print(f"[+] File: {output_filename} saved.")
                    elif mtt == 3:
                        aname, ext = os.path.splitext(filename)
                        output_filename = f"01-00{new_pdf_index + 1}-01-NON.pdf"
                        new_pdf_files[new_pdf_index].save(output_filename)
                        # print(f"[+] File: {output_filename} saved.")

                    pdf.close()
                    spinner.stop()
                    path = "."
                    extension = "NON.pdf"
                    pdfcronum = directory(path, extension)

                    if ((pdfcronum) != bodnum):
                        print("    2D and ESS ballot # do not match in " + zip_dir)
                        print("\n    Please correct or remove before running again\n")
                        input("\n    Press Enter to exit...\n")
                        sys.exit(1)

                    print("    Cropped and split 2D PDFs")

                    # Define files and folder path for copy
                    dir_path = (r".")
                    txt_path = glob.glob("*NON.pdf")
                    dest_txt_dir_path = (r"BallotOnDemand_Export")

                    # Copy files in current folder with *.txt to Import folder
                    for txt_path in txt_path:
                        txt_name = txt_path.split("""\\""")[-1]
                        txt_dest_full_path = dest_txt_dir_path + """\\""" + txt_name
                        shutil.move(txt_path, txt_dest_full_path)  ## copy the file

                    bodpath = pathlib.Path("BallotOnDemand_Export/")
                    with zipfile.ZipFile("BallotOnDemand_Export.ezip", mode="w") as archive:
                        for file_path in bodpath.iterdir():
                            archive.write(file_path, arcname=file_path.name)
                else:

                    spinner = Halo(text='.   Cropping PDFs', spinner='dots', interval='700', placement='right')
                    spinner.start()
                    zipn = "BallotOnDemand_Export.ezip"
                    zip_obj = zipfile.ZipFile(zipn, "r")
                    zip_obj.extractall("BallotOnDemand_Export")
                    zip_obj.close()

                    globz = glob.glob("BallotOnDemand_Export/*NON.pdf")
                    for globz in globz:
                        crop(["-p", "57", "-ap", "18", globz])

                    for filename in os.listdir('.'):
                        os.rename(filename, filename.replace('_cropped.pdf', '.pdf'))

                    fileList = glob.glob('BallotOnDemand_Export/*NON.pdf')

                    # Iterate over the list of filepaths & remove each file.
                    for filePath in fileList:
                        try:
                            os.remove(filePath)
                        except:
                            print("Error while deleting file : ", filePath)

                    source = '.'
                    destination = './BallotOnDemand_Export'
                    #
                    # gather all files
                    allfiles = glob.glob(os.path.join(source, '*NON.pdf*'), recursive=True)
                    # print("Files to move", allfiles)

                    # iterate on all files to move them to destination folder
                    for file_path in allfiles:
                        dst_path = os.path.join(destination, os.path.basename(file_path))
                        shutil.move(file_path, dst_path)

                    bodpath = pathlib.Path("BallotOnDemand_Export/")
                    with zipfile.ZipFile("BallotOnDemand_Export.ezip", mode="w") as archive:
                        for file_path in bodpath.iterdir():
                            archive.write(file_path, arcname=file_path.name)

                    spinner.stop()
                    print("    Cropped PDFs")
                # ZIP IT ALL UP SECTION #

                # File list for ZIP function
                list_files = ['Mapping Templates.xlsx', 'Rotations.xlsx', 'BallotOnDemand_Export.ezip',
                              precinct_folder + '\Languages.txt', precinct_folder + '\Offices.txt',
                              precinct_folder + '\Parties.txt', precinct_folder + '\Poll Places.txt',
                              precinct_folder + '\Poll Relations.txt', precinct_folder + '\Precincts.txt',
                              precinct_folder + '\Questions.txt', precinct_folder + '\Registered Voters.txt',
                              precinct_folder + '\Candidate Level Text.txt', precinct_folder + '\Candidates.txt',
                              precinct_folder + '\Contest Level Text.txt', precinct_folder + '\District Relations.txt',
                              precinct_folder + '\District Types.txt', precinct_folder + '\Districts.txt',
                              precinct_folder + '\Headings.txt', precinct_folder + '\Language Candidate Level Text.txt',
                              precinct_folder + '\Language Candidates.txt',
                              precinct_folder + '\Language Contest Level Text.txt',
                              precinct_folder + '\Language Districts.txt', precinct_folder + '\Language Groups.txt',
                              precinct_folder + '\Language Headings.txt', precinct_folder + '\Language Offices.txt',
                              precinct_folder + '\Language Parties.txt', precinct_folder + '\Language Poll Places.txt',
                              precinct_folder + '\Language Precincts.txt', precinct_folder + '\Language Questions.txt']

                #                print(zip_dir)
                pathlib.Path('../../completed').mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile("../../completed" + zip_dir + '_fixed.zip', 'w') as zipF:
                    for file in list_files:
                        zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)

                if (zip_dir + '_fixed.zip'):
                    print('\n    Files have been compressed')
                    if d2d_exists:
                        two_d_dump = '../../2d/'
                        if os.path.exists('../../2d'):
                            # print(zip_dir)
                            shutil.move(crop_path + d2d, two_d_dump + d2d)
                        else:
                            os.mkdir('../../2d')
                            shutil.move(crop_path + d2d, two_d_dump + d2d)
                    os.chdir("../../")
                    pathlib.Path('zips').mkdir(parents=True, exist_ok=True)
                    source = (my_zip)
                    destination = ("./zips")

                    filename = os.path.basename(source)
                    dest = os.path.join(destination, filename)
                    shutil.move(source, dest)
            print("\n    Pausing for suspense")
            time.sleep(2)
            print("________________________________________")
    print("\n    Program complete\n\n    Pausing for super suspense")
    print("________________________________________")
    time.sleep(3)

elif multizip == 0:
    print("\n    Hey " + os.getlogin() + "!!! There's no ZIP file in folder to extract!")
    print("\n    Pausing for suspense\n")
    time.sleep(3)
else:
    print("\n    If there is a 2D.pdf present there can only be one ZIP in the folder")
    print("\n    Pausing for suspense\n")
    time.sleep(3)
