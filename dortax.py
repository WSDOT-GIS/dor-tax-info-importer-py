from datetime import date
import os, io, urllib2, zipfile, csv, json, math

class DateEncoder(json.JSONEncoder):
    """This class allows datetime.date objects to be serialized as JSON.
    Dates will be output as ISO strings.
    """
    def default(self, o):
        if type(o) == date:
            return o.isoformat()
        else:
            return json.JSONEncoder.default(self, o)

def get_quarter(the_date=None):
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
    return the_date.year, quarter

def get_rates_zip_path(the_date=None):
    """Gets the path to the current rates ZIP file.
    """
    return "http://dor.wa.gov/downloads/Add_Data/Rates%sQ%s.zip" % get_quarter(the_date)

def get_location_code_boundaries_zip_path(the_date=None):
    """Gets the path to the ZIP archive containing 
    """
    # http://dor.wa.gov/downloads/LocBounds/LOCCODE_PUBLIC_14Q4.zip
    year, quarter = get_quarter(the_date)
    return "http://dor.wa.gov/downloads/LocBounds/LOCCODE_PUBLIC_%sQ%s.zip" %  (str(year)[-2:], quarter)

def set_dict_types(d):
    """When CSVs are parsed all fields are interpreted as strings.
    This function sets the values to the correct types.
    """
    for k in ["State", "Local", "RTA", "Rate"]:
        d[k] = float(d[k])
    for k in ["Effective Date", "Expiration Date"]:
        s = d[k]
        d[k] = date(*map(int,  (s[0:4],s[4:-2],s[6:])))
    # Delete the blank entry
    if d.has_key(''):
        del d['']

def download_binary_file(url, out_path):
    """Downloads a ZIP file from the internet
    """
     # Download the zip file and save a local version
    zip = urllib2.urlopen(url)
    with open(out_path, "wb") as f:
        while 1:
            packet = zip.read()
            if not packet:
                break
            f.write(packet)
        f.close()

def iterate_rate_csv(csvfile):
    """Generator function that iterates over a CSV file using a csv.DictReader.
    Additionally converts the types from string when necessary.
    """
    reader = csv.DictReader(csvfile)
    for d in reader:
        set_dict_types(d)
        yield d


if __name__ == "__main__":
    zip_path = get_rates_zip_path()


    zip_fn = os.path.split(zip_path)[1]

    csv_fn = os.path.splitext(zip_fn)[0] + ".csv"

    # Download ZIP and extract the CSV file.
    if not os.path.exists(zip_fn):
        download_binary_file(zip_path, zip_fn)

    if not os.path.exists(csv_fn):
        with zipfile.ZipFile(zip_fn) as zf:
            zf.extractall(".")

    out_list = {}


    with open(csv_fn, 'rb') as csvfile:
        for d in iterate_rate_csv(csvfile):
            out_list[d["Code"]] = d

    with open("rates.json", "w") as jsonfile:
        json.dump(out_list, jsonfile, cls=DateEncoder)

