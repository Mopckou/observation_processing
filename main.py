import os
import math
import scipy
import errno
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from src.approximater import SVD_APPROXIMATE
from src.function import FUNCTION
from configparser import ConfigParser

GSHV_1_1 = 0.
GSHV_1_1_sys = 0.
GSHN_1_1 = 0.
GSHN_1_1_sys = 0.
GSHV_2_1 = 0.
GSHV_2_1_sys = 0.
GSHN_2_1 = 0.
GSHN_2_1_sys = 0.
A_sys_aver = 0.
A_sys_percent = 0.
A_sour = 0.
A_sour_sys = 0.


LOG_DIRECTORY = os.path.join(os.getcwd(), 'OUT')

conf = ConfigParser()
conf.read('Configuration.ini')

FILE = conf.get('FILE', 'file')

error_min = float(conf.get('GENERAL', 'error_min'))

do_gshv = int(conf.get('GSHV', 'calc'))
gshv_width_begin = float(conf.get('GSHV', 'width_begin'))
gshv_width_end = float(conf.get('GSHV', 'width_end'))
gshv_step = float(conf.get('GSHV', 'step'))
gshv_windows = int(conf.get('GSHV', 'windows'))
error_limit_gshv = float(conf.get('GSHV', 'error'))

do_gauss = int(conf.get('GAUSS', 'calc'))
gauss_width_begin = float(conf.get('GAUSS', 'a0_begin'))
gauss_width_end = float(conf.get('GAUSS', 'a0_end'))
gauss_step = float(conf.get('GAUSS', 'step'))
gauss_windows = int(conf.get('GAUSS', 'windows'))
error_limit_gauss = float(conf.get('GAUSS', 'error'))



def clear_data():
    data = {
        'coeff': None,
        'important_section': None,
        'error': None,
        't_nul': None,
        'width': None,
        'x_segment': None,
        'y_segment': None,
        'y_new_segment': None
    }
    return data

flag_continue = True
FILE = os.path.join('IN', FILE)
file = scipy.loadtxt(FILE, dtype=float)
x = file[:, 0]
y = file[:, 1]

x_begin = x[30: 40]
y_begin = y[30: 40]

x_end = x[-10:]
y_end = y[-10:]


def get_average(list):
    summ = 0.
    for elem in list:
        summ += elem
    return summ/len(list)

def get_error(max_elem, average):
    return max_elem - average

def get_percent(error, average):
    return error * 100 / average

aver_begin = get_average(y_begin)
aver_end = get_average(y_end)

def get_sigma(value_list):
    sigma = 0.
    N = len(value_list)
    average = get_average(value_list)
    for value in value_list:
        sigma += (value - average) * (value - average)
    sigma = sigma / (N - 1)
    sigma = scipy.sqrt(sigma)
    return sigma

def get_aver_and_percent(aver_list):
    aver_list.sort()
    aver_list.reverse()
    _aver = get_average(aver_list)
    print('aver - %s' % _aver)
    sigma = get_sigma(aver_list)
    print('sigma %s' % sigma)
    percent = get_percent(sigma, _aver)
    if percent < error_min:
        percent = error_min
    return _aver, percent

A_sys_aver, A_sys_percent = get_aver_and_percent([aver_begin, aver_end])
print(A_sys_aver)
print(A_sys_percent)

def approximate(apx, x, y, windows, width):
    work_array = []
    coeff = apx.fit(x, y, windows, width)

    for num in range(0, len(coeff)):
        data = clear_data()
        x_segment = x[num: num + windows]
        y_segment = y[num: num + windows]
        if coeff[num][6] == 'T':
            important_section = True
        else:
            important_section = False
        data['t_nul'] = coeff[num][5]
        data['important_section'] = important_section
        data['x_segment'] = x_segment
        data['width'] = width
        data['coeff'] = coeff[num][:4]
        data['error'] = coeff[num][4]
        data['y_segment'] = y_segment
        work_array.append(data)
    return work_array

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

def logging(log, x, y):
    fl = open(log, 'w')
    for i in range(len(x)):
        fl.write("%s %s\n" % (x[i], y[i]))
    fl.close()

def get_amplitude_gauss(obs):
    #print('________________________________________')
    begin_points = obs['y_new_segment'][:10]
    end_points = obs['y_new_segment'][-10:]
    #print(begin_points)
    #print(end_points)

    aver_begin = get_average(begin_points)
    aver_end = get_average(end_points)
    #print(aver_begin)
    #print(aver_end)
    aver = get_average([aver_begin, aver_end])
    #print(aver)
    f = FUNCTION('gauss')
    maximum = f.calc_dot(obs['coeff'], obs['t_nul'], obs['t_nul'], obs['width'])
    #print(maximum)
    return maximum - aver



def get_summ_coeff(coeff):
    sum = 0.
    for c in coeff:
        sum += c
    return sum

def filter_gauss(gauss_list):
    flag = 0
    group = [gauss_list[0]]
    gauss_group = []
    final_list = []
    for num in range(1, len(gauss_list)):
        #print(num)

        if gauss_list[num]['t_nul'] - gauss_list[num - 1]['t_nul'] == 1:
            group.append(gauss_list[num])
        else:
            gauss_group.append(group)
            group = [gauss_list[num]]
    if group != []:
        gauss_group.append(group)

    for gr in gauss_group:
        best = gr[0]
        for i in gr:
            if i['coeff'][3] > best['coeff'][3]:
                best = i
        final_list.append(best)
    return final_list

def find_best(all_fits, windows):
    new_fits = []

    for num, fits in enumerate(all_fits):
        for fit in fits:
            #print(fit['coeff'])
            if is_best(fit, new_fits, all_fits[num + 1:], windows/2):
                new_fits.append(fit)

    return new_fits

def is_best(fit, new_fits, all_fits, windows):
    t_nul = fit['t_nul']
    error = fit['error']
    for f in new_fits:
        if f['t_nul'] == t_nul or abs(f['t_nul'] - t_nul) < windows:
            return False

    for fits in all_fits:
        for f in fits:
            if (f['t_nul'] == t_nul or abs(f['t_nul'] - t_nul) < windows) and f['error'] < error:
                return False
    return True

print('-----------')
plt.scatter(x, y, s=5)
plt.xlabel(r'$x$')
plt.ylabel(r'$f(y)$')
plt.title(r'$y=$')
plt.grid(True)
plt.show()
plt.scatter(x, y, s=5)

max_gshv = []


if do_gshv:
    apx = SVD_APPROXIMATE()
    apx.set_function('right_angled')
    all_gsha = []
    best_fit = []
    for width in np.arange(gshv_width_begin, gshv_width_end, gshv_step):
        work_array = approximate(apx, x, y, gshv_windows, width)
        best_fit = []

        for fit in work_array:
            #print('x0 - %s, error - %s, coeff - %s, important_section - %s' % (
            #fit['t_nul'], fit['error'], fit['coeff'], fit['important_section']))
            error_percent_with_sys = abs(get_percent(float(fit['coeff'][0]), A_sys_aver) - 100)
            if abs(float(fit['coeff'][3])) > 0.24 and float(fit['coeff'][0]) > 0.1 and error_percent_with_sys < 20. and fit['error'] is not None and fit['error'] < error_limit_gshv:# and fit['important_section']:
                best_fit.append(fit)
        if best_fit:
            best_fit = filter_gauss(best_fit)
        for i in best_fit:
            print(i['coeff'], i['t_nul'], i['error'], i['width'])
        all_gsha.append(best_fit)
        print('____________')
    best_fit = find_best(all_gsha, gshv_windows)
    for i in best_fit:
        error_percent_with_sys = abs(get_percent(float(i['coeff'][0]), A_sys_aver) - 100)
        print(error_percent_with_sys)
        print(i['coeff'], i['t_nul'], i['error'], i['width'])
    for i in best_fit:
        Y_new = apx.get_new_segment(i['coeff'], i['x_segment'], i['t_nul'], i['width'])
        i['y_new_segment'] = Y_new
        #i['sig'] = get_sig_segment()
        plt.plot(i['x_segment'], i['y_new_segment'])
        log = create_result_file('gshv', 'gshv_%s' % (best_fit.index(i) + 1))
        logging(log, i['x_segment'], i['y_new_segment'])
        max_gshv.append(
            i['coeff'][3]
        )

max_gauss = []
if do_gauss:
    apx = SVD_APPROXIMATE()
    apx.set_function('gauss')
    all_gauss = []
    best_fit = []
    for width in np.arange(gauss_width_begin, gauss_width_end, gauss_step):
        work_array = approximate(apx, x, y, gauss_windows, width)
        best_fit = []

        for fit in work_array:
            #print('x0 - %s, error - %s, coeff - %s, important_section - %s' % (
            #fit['t_nul'], fit['error'], fit['coeff'], fit['important_section']))
            error_percent_with_sys = abs(get_percent(float(fit['coeff'][0]), A_sys_aver) - 100)
            if error_percent_with_sys < 16. and float(fit['coeff'][3]) > 0.8 and fit['error'] is not None and fit['error'] < error_limit_gauss:# and fit['important_section']:
                best_fit.append(fit)
        #print(len(best_fit))
        if best_fit:
            best_fit = filter_gauss(best_fit)
        for i in best_fit:
            print(i['coeff'], i['t_nul'], i['error'], i['width'])
        all_gauss.append(best_fit)
        print('____________')
    best_fit = find_best(all_gauss, gauss_windows)
    for i in best_fit:
        print(i['coeff'], i['t_nul'], i['error'], i['width'])
    for i in best_fit:
        Y_new = apx.get_new_segment(i['coeff'][:4], i['x_segment'], i['t_nul'], i['width'])
        i['y_new_segment'] = Y_new
        plt.plot(i['x_segment'], i['y_new_segment'])
        log = create_result_file('gauss', 'gauss_%s' % (best_fit.index(i) + 1))
        logging(log, i['x_segment'], i['y_new_segment'])
        max_gauss.append(
            get_amplitude_gauss(i)
        )

def eq(elem, elem2):
    percent = abs((elem * 100 / elem2) - 100)
    return percent < 1.5

def find_eq(elem, index, list):
    if index > len(list):
        return None
    for i in list[index:]:
        if eq(elem, i):
            return i

def find_equal(elem, elem_list):
    eq = abs(elem - elem_list[0])
    save = elem_list[0]
    for e in elem_list[1:]:
        diff = abs(elem-e)
        if diff < eq:
            eq = diff
            save = e
    return save


def get_gsha_pairs(pairs):
    summ1 = 0
    summ1 += mg[0] / mg[9]
    summ1 += mg[1] / mg[5]
    summ1 += mg[2] / mg[6]
    summ1 += mg[3] / mg[7]
    summ1 += mg[4] / mg[8]

    summ2 = 0
    summ2 += mg[0] / mg[9]
    summ2 += mg[1] / mg[7]
    summ2 += mg[2] / mg[8]
    summ2 += mg[3] / mg[5]
    summ2 += mg[4] / mg[6]

    pairs = []
    print(summ1)
    print(summ2)
    print(4 - summ1)
    print(4 - summ2)
    if abs(4 - summ1) < abs(4 - summ2):
        print('normal pair')
        pairs.append([mg[0], mg[9]])
        pairs.append([mg[1], mg[5]])
        pairs.append([mg[2], mg[6]])
        pairs.append([mg[3], mg[7]])
        pairs.append([mg[4], mg[8]])
        return pairs
    else:
        print('mirror pair')
        pairs.append([mg[0], mg[9]])
        pairs.append([mg[1], mg[7]])
        pairs.append([mg[2], mg[8]])
        pairs.append([mg[3], mg[5]])
        pairs.append([mg[4], mg[6]])
        return pairs



if max_gshv != []:
    try:
        print('максимумы всех ГШВ - %s' % max_gshv)
        pairs = []
        index = 0
        # for gshv_elem in max_gshv:
        #     index += 1
        #     eq_gshv_elem = find_eq(gshv_elem, index, max_gshv)
        #     if eq_gshv_elem is not None:
        #         pairs.append(
        #             [gshv_elem, eq_gshv_elem]
        #         )
        # pair_sys = []
        new_pair = []
        print('dasdas')
        pair_part_one = max_gshv[:int(len(max_gshv)/2)]
        pair_part_two = max_gshv[int(len(max_gshv)/2):]

        print(pair_part_one, pair_part_two)
        for elem in pair_part_one:
            equal = find_equal(elem, pair_part_two)
            new_pair.append([elem, equal])
        print('new_pair - %s' % new_pair)
        mg = [0 for i in range(1, 11)]
        print(mg)
        for num, val in enumerate(mg): # 10 элемент специально не учитываю, т.к. это пара для определения нуля
            try:
                mg[num] = max_gshv[num]
            except IndexError:
                print(123)
                pass
        pairs = get_gsha_pairs(mg)

        print('pairs - %s' % pairs)
        #print(pairs)
        GSHV_1_1, GSHV_1_1_sys = get_aver_and_percent(pairs[1])
        GSHN_1_1, GSHN_1_1_sys = get_aver_and_percent(pairs[2])
        GSHV_2_1, GSHV_2_1_sys = get_aver_and_percent(pairs[3])
        GSHN_2_1, GSHN_2_1_sys = get_aver_and_percent(pairs[4])
        print('GSHV_1_1 - %s, GSHV_1_1_sys - %s' % (GSHV_1_1, GSHV_1_1_sys))
        print('GSHN_1_1 - %s, GSHN_1_1_sys - %s' % (GSHN_1_1, GSHN_1_1_sys))
        print('GSHV_2_1 - %s, GSHV_2_1_sys - %s' % (GSHV_2_1, GSHV_2_1_sys))
        print('GSHN_2_1 - %s, GSHN_2_1_sys - %s' % (GSHN_2_1, GSHN_2_1_sys))
    except Exception as exe:
        print(exe)

if max_gauss != []:
    try:
        best_gauss = None
        print('максимумы гауссиан - %s' % max_gauss)
        # for elem, value in enumerate(max_gauss):
        #     v = value * (1 / (gauss_width_begin * math.sqrt(2 * math.pi)))
        #     max_gauss[elem] = v
        print('максимумы гауссиан 2 - %s' % max_gauss)
        first_half_sour, first_half_sour_sys = get_aver_and_percent([max_gauss[0], max_gauss[1]])
        second_half_sour, second_half_sys = get_aver_and_percent([max_gauss[2], max_gauss[3]])
        if first_half_sour > second_half_sour:
            print('first half')
            best_gauss = [max_gauss[0], max_gauss[1]]
        else:
            print('second half')
            best_gauss = [max_gauss[2], max_gauss[3]]
        A_sour, A_sour_sys = get_aver_and_percent(best_gauss)
        print('___')
        print(A_sour)
        print(A_sour_sys)
    except Exception as e:
        print(e)

def write_result_file(GSHV_1_1, GSHN_1_1, GSHV_2_1, GSHN_2_1, A_sys, A_sour):
    tem = '\n'
    #tem += "#234567810123456782012345678301234567840123456785012345678601234567870123456788012345678901234567100123456711012345671201234567130123456714012345671501234567160\n"
    #tem += "# Title, ch1     Year MM DD Year.XXX  NSH1_1   sig     NSL1_1   sig     NSH2_1   sig     NSL2_1   sig     A_sys    sig     A_sour   sig  F_sou   g       T_cal=\n"
    #tem += "#        ch2                          NSH1_2           NSL1_2           NSH2_2           NSL2_2                                          Jy              =T/g,K\n"
    #tem += "# ==============================================================================================================================================================\n"
    #tem += "#\n"
    G1, S1 = round(GSHV_1_1[0], 3), round(GSHV_1_1[1], 4)
    G2, S2 = round(GSHN_1_1[0], 3), round(GSHN_1_1[1], 4)
    G3, S3 = round(GSHV_2_1[0], 3), round(GSHV_2_1[1], 4)
    G4, S4 = round(GSHN_2_1[0], 3), round(GSHN_2_1[1], 4)
    A1, S5 = round(A_sys[0], 3), round(A_sys[1], 4)
    A2, S6 = round(A_sour[0], 3), round(A_sour[1], 4)
    tem += 'CasA_K1_Volt_obs 2018 08 09  0.0       %s     %s     %s      %s     %s      %s     %s      %s     %s       %s     %s     %s    0.0     0.0     0.0' % (G1, S1, G2, S2, G3, S3, G4, S4, A1, S5, A2, S6)
    log = create_result_file('result', 'result_file')
    fl = open(log, 'a')
    fl.write("%s\n" % (tem))
    fl.close()

write_result_file([GSHV_1_1, GSHV_1_1_sys], [GSHN_1_1, GSHN_1_1_sys], [GSHV_2_1, GSHV_2_1_sys], [GSHN_2_1, GSHN_2_1_sys], [A_sys_aver, A_sys_percent], [A_sour, A_sour_sys] )

plt.xlabel(r'$x$')
plt.ylabel(r'$f(y)$')
plt.title(r'$y=$')
plt.grid(True)
plt.show()