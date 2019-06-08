import hashlib
import os
import glob
import traceback
import re
import binascii
import time

BYTES = 1024

class ReadWriteOp:

    def __init__(self):
        pass

    def convert_bytes(self, num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        global BYTES
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < BYTES:
                return "%3.1f %s" % (num, x)
            num /= BYTES


    def extract_digits(self, s):
        """
        this function separates digits and strings
        """
        # remove whitespaces if any
        new_string = s.replace(" ", "")
        string = new_string.strip('0123456789')
        digit = int(re.search(r'\d+', s).group(0))
        return digit, string[0]


    def convert_size(self, string):
        """
        this function calculates total bytes
        """
        global BYTES
        units = ['K', 'M', 'G', 'T']
        requested_size, unit = self.extract_digits(string)
        # for conversion of lowercase to uppercase
        if (unit.islower()):
            unit = unit.upper()
        byte = 1
        if unit in units:
            for i in range(units.index(unit) + 1):
                byte *= BYTES
        return requested_size, byte

    def generate_payload(self, file_no, file_size):
        payload=[]
        size, bytes_required = self.convert_size(file_size)
        for data in range(file_no):
            content = os.urandom(size * bytes_required)
            payload.append(content)
        return payload

    def plain_write(self, file_path, payload):
        try:
            with open(file_path, 'wb') as fout:
                fout.write(payload)
        except Exception as err:
            return -1

    def plain_read(self, file_path):
        try:
            with open(file_path, 'rb') as fout:
                random_data = fout.read()
        except Exception as err:
            return -1
        else:
            return random_data




class Checksum:
    def __init__(self):
        self.source_checksum = None
        self.dest_checksum = None

    def calculate_source_hash(self, data):
        hasher = hashlib.sha256()
        hasher.update(data)
        return hasher.hexdigest()

    def calculate_dest_hash(self, file):
        block = 65536
        hasher = hashlib.sha256()
        with open(file, 'rb') as afile:
            buf = afile.read(block)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(block)
        return hasher.hexdigest()



