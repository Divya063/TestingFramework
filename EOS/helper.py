"""
Helper file automate running of tests
"""
import os
import glob
def cleanup():
    """
    delete the created files
    """
    filelist = glob.glob(os.path.join("", "*.txt"))
    for f in filelist:
        os.remove(f)

def run_eos(tests, tasks):
    if(len(tests)==1):
        print(tests)
    test_storage = tasks['tests']['storage']
    number_of_files = test_storage['throughput']['fileNumber']
    size = test_storage['throughput']['fileSize']
    # test = Benchmark(number_of_files, size)
    logger.info(test.print_result())
