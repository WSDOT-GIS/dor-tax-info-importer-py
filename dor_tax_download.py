"""Downloads tax rate data from the WA DOR website
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from datetime import date
import os
import math
from zipfile import ZipFile
import requests


def get_quarter(the_date=None):
    # type: (date) -> (int, int)
    """Returns the year and quarter for the given date.
    If given date is None (default), the current date
    (datetime.date.today()) is assumed.

    :Quarters:
    January-March:      1
    April-June:         2
    July-September:     3
    October-December:   4

    :Returns:

    year (int), quarter (int)
    """
    if not the_date:
        the_date = date.today()
    quarter = int(math.ceil(the_date.month / 3))
    return the_date.year % 100, quarter


def get_sales_tax_shapefile_zip_path(the_date=None):
    # type: (date) -> str
    """Gets the URL for ZIPped shapefile for the given date"""
    return "https://dor.wa.gov/sites/default/files/legacy/downloads/CTbounds/Cities_%02dQ%d.zip" % get_quarter(the_date)


def main():
    """This function is executed when file is run as a script
    """
    zip_path = get_sales_tax_shapefile_zip_path()
    zip_fn = os.path.split(zip_path)[1]
    zip_dir = os.path.join(".", os.path.splitext(zip_fn)[0])
    zip_dir = os.path.abspath(zip_dir)
    is_new_file = download_file(zip_path, zip_fn)
    if is_new_file:
        extract_zip(zip_fn, zip_dir)


def download_file(file_url, out_path):
    # type: (str, str)
    """Copies a file from a URL to local path
    """
    out_path = os.path.abspath(out_path)
    if os.path.exists(out_path):
        print("%s already exists." % out_path)
        return None

    with open(out_path, 'wb') as out_file:
        print("Saving %s to %s..." % (file_url, out_path))
        response = None
        try:
            response = requests.get(file_url, stream=True)
            for chunk in response.iter_content(chunk_size=128):
                out_file.write(chunk)
        finally:
            if response:
                response.close()
    return out_path


def extract_zip(zip_path, out_dir):
    # type: (str, str)
    """Extracts a zip file's contents
    """
    if not os.path.exists(zip_path):
        raise FileNotFoundError(zip_path)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    else:
        raise FileExistsError(out_dir)

    print("Extracting contents from %s into %s..." % (zip_path, out_dir))
    with ZipFile(zip_path) as zip_file:
        zip_file.extractall(out_dir)


if __name__ == "__main__":
    main()
