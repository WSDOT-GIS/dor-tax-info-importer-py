"""Installs pip, the Python Package installer and modules specified in requirements.txt.
"""
import sys, os, urllib2

get_pip_url = "https://bootstrap.pypa.io/get-pip.py"

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

get_pip_path = "get-pip.py"

if not os.path.exists(get_pip_path):
    download_binary_file(get_pip_url, get_pip_path)

# Install pip.
os.system(get_pip_path)

# Get PIP executable

pydir, pyexe = os.path.split(sys.executable)
pip_exe_path = os.path.join(pydir, "Scripts", "pip.exe")
if not os.path.exists(pip_exe_path):
    raise "File not found: %s" % pip_exe_path

os.system("%s install -r requirements.txt" % pip_exe_path)