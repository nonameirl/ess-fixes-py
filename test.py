from myimports import *

for my_zip in glob.glob('*.zip'):
    print("________________________________________")

    data_dir = Path(my_zip).stem
    data_wd = EXTRACT_DIR.joinpath(data_dir)

    print("\n    " + data_dir + " election data\n")

    # Extract zip file
    with zipfile.ZipFile(my_zip) as zip_file:
        zip_file.extractall(data_wd)
        zip_file.close()

    get_location(my_zip)

print("________________________________________")

