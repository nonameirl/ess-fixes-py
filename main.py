from myimports import *

x_pdf = "r'*'"

if (filecount('*.zip') == 1 and filecount('*.pdf') <= 1) or \
        (filecount('*.zip') > 1 and filecount('*2D*.pdf') is False):

    # print("________________________________________")

    for my_zip in glob.glob('*.zip'):
        print("________________________________________")

        # print(my_zip)
        # print(Path(my_zip))

        data_dir = Path(my_zip).stem
        data_wd = EXTRACT_DIR.joinpath(data_dir)

        print("\n    " + data_dir + " election data\n")
        # print(data_wd)

        # Create folder for extraction, replace if exists
        try:
            data_wd.mkdir(parents=True, exist_ok=True)
        except IOError:
            shutil.rmtree(EXTRACT_DIR, data_dir)
            data_wd.mkdir(parents=True, exist_ok=False)

        # Extract zip file
        with zipfile.ZipFile(my_zip) as zip_file:
            zip_file.extractall(data_wd)
            zip_file.close()

        zipn = data_wd.joinpath(BOD_ZIP)
        # print(zipn)
        zip_obj = zipfile.ZipFile(zipn, "r")

        restart = True
        x = 0
        while restart:
            restart = False
            try:
                zip_obj.extractall(Path(data_wd, BOD_DIR))
                zip_obj.close()
            except (IOError, PermissionError):
                print("Unable to extract files. Perhaps you have a file opened from there. Creating a separate folder")
                try:
                    tmp_dir = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
                    bod_zdir = Path(tmp_dir)
                    data_wd.joinpath(''.join(random.choice(string.ascii_lowercase) for i in range(5))).mkdir(
                        parents=True, exist_ok=True)
                    time.sleep(3)
                    zip_obj.extractall(Path(data_wd, bod_zdir))
                    restart = False
                finally:
                    print("Temp file created")
                    restart = False
            time.sleep(3)

        zip_obj.close()


            def mn_data_fix():

                # DATA CRUNCHING AND COMPARISON SECTION #

                # Read Candidates.txt file and assign only the 'Import Office ID' column for comparison
                candidate_data = pd.read_csv(data_wd.joinpath(CANDIDATE_FILE), encoding='UTF-16', on_bad_lines='skip', skiprows=1,
                                  sep='|',
                                  usecols=['Import Office ID'], keep_default_na=False, dtype=object)

                # Read Offices.txt file with '|' delimiter and a header define on line 1
                office_data = pd.read_csv(Path(import_dir, OFFICE_FILE), encoding='UTF-16', on_bad_lines='skip', sep='|', header=1,
                                  keep_default_na=False, dtype=object)

                # If values in column 'Import Office ID' in df1 does not exist in column 'Import Office ID' in df2 then delete the row in df1.
                new_df = df1[df1['Import Office ID'].isin(df2['Import Office ID'])]

                # Overwrite Offices.txt with updated version
                new_df.to_csv(Path(import_dir, OFFICE_FILE), sep='|', index=False)

                first_line = "$$Offices$$\n"

                with open(Path(import_dir, OFFICE_FILE), 'r+') as fp:
                    lines = fp.readlines()  # lines is list of line, each element '...\n'
                    lines.insert(0, first_line)  # you can use any index if you know the line index
                    fp.seek(0)  # file pointer locates at the beginning to write the whole file again
                    fp.writelines(lines)  # write whole lists again to the same file

                # ZIP IT ALL UP SECTION #

                # File list for ZIP function

                file_list1 = ['ROTATION.xlsx', 'BallotOnDemand_Export.ezip']

                file_list2 = ['Languages.txt', 'Offices.txt', 'Parties.txt', 'Poll Places.txt', 'Poll Relations.txt',
                              'Precincts.txt', 'Questions.txt', 'Registered Voters.txt', 'Candidate Level Text.txt',
                              'Candidates.txt',
                              'Contest Level Text.txt', 'District Relations.txt', 'District Types.txt', 'Districts.txt',
                              'Headings.txt', 'Language Candidate Level Text.txt', 'Language Candidates.txt',
                              'Language Contest Level Text.txt', 'Language Districts.txt', 'Language Groups.txt',
                              'Language Headings.txt', 'Language Offices.txt', 'Language Parties.txt',
                              'Language Poll Places.txt', 'Language Precincts.txt', 'Language Questions.txt']

            print(Path(COMPLETE_DIR, data_dir + '_fixed.zip'))
            Path(COMPLETE_DIR).mkdir(parents=True, exist_ok=True)
            zip_output = Path(COMPLETE_DIR, data_dir + '_fixed.zip')
            if zip_output.exists():
                zip_output.unlink()

            with zipfile.ZipFile(zip_output, 'w') as zipF:

                for file in file_list1:
                    zipF.write(Path(data_wd, file), Path(file), compress_type=zipfile.ZIP_DEFLATED)
                for file in file_list2:
                    zipF.write(Path(import_dir, file), Path(import_dir.name, file), compress_type=zipfile.ZIP_DEFLATED)
'''
            if Path(z_dir + '_fixed.zip'):
                print('\n    Files have been compressed')
                try:
                    shutil.rmtree(data_wd)
                except:
                    print("Unable to remove election folder. Perhaps you have a file open")
#
#Path('zips').mkdir(parents=True, exist_ok=True)
'''
'''                   if d2d_exists:
                    two_d_dump = '../../2d/'
                    if os.path.exists('../../2d'):
                        #print(zip_dir)
                        shutil.move(crop_path + d2d, two_d_dump + d2d)
                    else:
                        os.mkdir('../../2d')
                        shutil.move(crop_path + d2d, two_d_dump + d2d)                   
'''

'''
                    source = (my_zip)
                    destination = ("./zips")

                    filename = os.path.basename(source)
                    dest = os.path.join(destination,filename)
                    shutil.move(source, dest)
                    print('\n    The files has been compressed\n')
                    print("    Pausing for suspense")
                    print("________________________________________")
                    time.sleep(2)


'''
