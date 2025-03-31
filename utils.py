import zipfile
import os

def create_zip(filenames, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, ) as zipf:
        for filename in filenames:
            zipf.write(filename, arcname=os.path.basename(filename))
    return zip_filename

