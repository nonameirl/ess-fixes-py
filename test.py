from myimports import *

for my_zip in glob.glob('*.zip'):
    print("________________________________________")


    # Define working data folder for current election
    data_wd = EXTRACT_DIR.joinpath(Path(my_zip).stem)

    # parse the Readme.txt file to
    get_location(my_zip)

    # Extract zip file
    with zipfile.ZipFile(my_zip) as zip_file:
        zip_file.extractall(data_wd)
        zip_file.close()





print("________________________________________")

