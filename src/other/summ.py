import os
import scipy
import errno

file_with_noise = 'ermakov_Ver2.txt'
file_withou_noise = 'noise.txt'

file = scipy.loadtxt(file_with_noise, dtype=float)
x_noise = file[:, 0]
y_noise = file[:, 1]

file = scipy.loadtxt(file_withou_noise, dtype=float)
x_clear = file[:, 0]
y_clear = file[:, 1]

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
print(LOG_DIRECTORY)
log = create_result_file('generate', 'ver2_with_noise')
fl = open(log, 'w')
for i in range(0, len(x_clear)):
    fl.write("%s %s\n" % ((i+1), y_clear[i] + y_noise[i]))
fl.close()
