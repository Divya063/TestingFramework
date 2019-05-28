import hashlib
import os
import glob
import traceback
import re
import binascii
from timer import StopWatch, Measure, Profiling

BLOCKSIZE = 65536


# SHA256 Hash (also handles Large Files)
def calculate_hash(file):
    hasher = hashlib.sha256()
    with open(file, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return (hasher.hexdigest())


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def extract_digits(s):
    """
    this function separates digits and strings
    """
    string = s.strip('0123456789')
    digit = int(re.search(r'\d+', s).group(0))
    return digit, string


def convert_size(string):
    """
    this function calculates total bytes
    """
    units = ['K', 'M', 'G']
    requested_size, unit = extract_digits(string)
    # for conversion of lowercase to uppercase
    if (unit.islower()):
        unit = unit.upper()
    byte = 1
    if unit in units:
        for i in range(units.index(unit) + 1):
            byte *= 1024
    return requested_size, byte


print("Enter the number of files")
number_of_files = int(input())
print("Enter size (in whole number)")

"""
Example : 1M for 1 MB
          5K for 5 KB
          1G for 1 GB
          1024 for 1 KB
"""

input_size = input()
size, bytes_required = convert_size(input_size)
# print(size, bytes_required)
extension = ".txt"
dictionary = {}
timer = Profiling()
for files in range(number_of_files):
    name = files
    file_name = str(name) + extension
    with open(file_name, 'wb') as fout:
        # create files filled with random bytes
        measure=timer.stats.startMeasurement()
        content = os.urandom(size * bytes_required)
        hash_num = hashlib.sha256(content).hexdigest()
        fout.write(content)
        measure.stop()
        print(measure)

timer.stop()
print(timer)

    # store hashed values in dictionary
    #dictionary[file_name] = hash_num
    # !dd if=/dev/urandom of=$file_name bs=$size count=$bytes_required
    # print(hash_num)
