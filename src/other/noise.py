import os
import errno
import numpy

def create_result_file(type, name):
    name_folder = '%s' % type
    name_log = '%s.txt' % name
    current_log_directory = os.path.join(LOG_DIRECTORY, name_folder)
    log = os.path.join(current_log_directory, name_log)
    if not os.path.exists(current_log_directory):
        make_sure_path_exists(current_log_directory)
    return log

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
LOG_DIRECTORY = os.path.join(os.getcwd(), 'OUT')

n = numpy.random.normal(0, 0.01, 4000)
summ = 0.
for i in n:
    summ += i

print(summ/len(n))

log = create_result_file('generate', 'noise')
fl = open(log, 'w')
for i in range(0, 4000):
    fl.write("%s %s\n" % ((i+1), n[i]))
fl.close()

