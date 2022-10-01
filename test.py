from myimports import *

print('TEST')

for my_zip in glob.glob('*.zip'):
    print("________________________________________")

    data_dir = Path(my_zip).stem
    data_wd = EXTRACT_DIR.joinpath(data_dir)

    print("\n    " + data_dir + " election data\n")


    # Extract zip file
    with zipfile.ZipFile(my_zip) as zip_file:
        zip_file.extractall(data_wd)
        zip_file.close()

#    extract_zip(data_wd, BOD_ZIP)


    get_location(data_wd, None, 1)

    # get_location(extract_zip(data_wd, BOD_ZIP, 1))
