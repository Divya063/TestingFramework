import os
import sys

class Corruption:
    def __init__(self):
        self.exit = 0

    def file_exists(self):
        if not (os.path.exists('output.txt')):
           return 1
        return 0


    def corruption_test(self):
        """

        :return: number of corrupted files
        """
        flag = 0
        corrupted_files = 0
        with open('output.txt', 'rb') as text:
            for line in text:
                string = line.decode('utf-8', 'ignore')
                if (flag == 1):
                    list = string.split(" ")
                    if (list[3].strip() == "YES"):
                        # counts number of corrupted files
                        corrupted_files += 1
                flag = 1

        return corrupted_files

    def exit_code(self):
        if(self.file_exists()==1):
            self.exit|=1
        else:
            if(self.corruption_test()>0):
                self.exit|=1
        return self.exit

if __name__ == "__main__":
    test_integrity =  Corruption()
    print(test_integrity.exit_code())


