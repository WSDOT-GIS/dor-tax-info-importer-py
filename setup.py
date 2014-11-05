"""Installs pip, the Python Package installer and modules specified in requirements.txt.
"""
import sys, os, urllib2

get_pip_url = "https://bootstrap.pypa.io/get-pip.py"

def download_binary_file(url, out_path=None):
    """Downloads a ZIP file from the internet if it does not already exist.
    """
    if not out_path:
        url_root, out_path = os.path.split(url)
        del url_root
    if not os.path.exists(out_path):
         # Download the zip file and save a local version
        zip = urllib2.urlopen(url)
        with open(out_path, "wb") as f:
            while 1:
                packet = zip.read()
                if not packet:
                    break
                f.write(packet)
            f.close()
    return out_path

get_pip_path = download_binary_file(get_pip_url)

# Install pip.
os.system(get_pip_path)

# Get PIP executable
pydir, pyexe = os.path.split(sys.executable)
pip_exe_path = os.path.join(pydir, "Scripts", "pip.exe")
if not os.path.exists(pip_exe_path):
    raise "File not found: %s" % pip_exe_path

# Install requirements.
os.system("%s install -r requirements.txt" % pip_exe_path)

print "Get Geopackage library for SQLite..."
libgpkg_path = download_binary_file("https://bitbucket.org/luciad/libgpkg/downloads/libgpkg-0.9.18-win64.zip")