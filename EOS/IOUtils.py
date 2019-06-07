import hashlib
import os
import glob
import traceback
import re
import binascii

BLOCKSIZE = 65536

class ReadWriteOp:

    def __init__(self):
        pass

    def convert_bytes(self, num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0


    def extract_digits(self, s):
        """
        this function separates digits and strings
        """
        string = s.strip('0123456789')
        digit = int(re.search(r'\d+', s).group(0))
        return digit, string


    def convert_size(self, string):
        """
        this function calculates total bytes
        """
        units = ['K', 'M', 'G']
        requested_size, unit = self.extract_digits(string)
        # for conversion of lowercase to uppercase
        if (unit.islower()):
            unit = unit.upper()
        byte = 1
        if unit in units:
            for i in range(units.index(unit) + 1):
                byte *= 1024
        return requested_size, byte



class Checksum:
    def __init__(self):
        self.source_checksum = None
        self.dest_checksum = None

    def calculate_source_hash(self, data):
        hasher = hashlib.sha256()
        hasher.update(data)
        return hasher.hexdigest()

    def calculate_dest_hash(self, file):
        hasher = hashlib.sha256()
        with open(file, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest()

