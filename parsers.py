from allocate import physical_server, virtual_machine

# =============================================================================
# Number of days of every month
# =============================================================================
days_of_month = list({31, 30, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31})

# =============================================================================
# File path
# =============================================================================
input_path = 'input_5flavors_cpu_7days.txt.'
test_path = 'TestData_2015.2.20_2015.2.27.txt'
train_path = 'TrainData_2015.1.1_2015.2.19.txt'
history_path = '2015.12.01_2016.01.31.txt'

# =============================================================================
# Some constants
# =============================================================================
total_flavors = 15

# =============================================================================
# Read data from given txt
# =============================================================================
def read_data():
    # Read input file
    now_block = 0
    flavor_num = 0
    flavor_list = []
    sample_vm = []
    f = open(input_path, 'r+', encoding='utf-8')
    for line in f:
        if line is not '\n':
            if now_block == 0:
                space_1 = line.find(' ')
                space_2 = line.find(' ', space_1 + 1)
                CPU = int(line[0:space_1])
                MEM = int(line[space_1:space_2])
                STO = int(line[space_2:])
                sample_ps = physical_server(CPU, MEM, STO)
                sample_ps.state()
                now_block += 1
            else:
                if now_block == 1:
                    flavor_num = int(line)
                    for i in range(flavor_num):
                        line = f.readline()
                        space_1 = line.find(' ')
                        space_2 = line.find(' ', space_1 + 1)
                        space_3 = line.find('\n', space_2 + 1)
                        NUM = int(line[6:space_1])
                        CPU = int(line[space_1:space_2])
                        MEM = int(line[space_2:space_3])
                        tempVM = virtual_machine(NUM, CPU, MEM)
                        sample_vm.append(tempVM)
                        flavor_list.append(NUM)
                        tempVM.state()
                    now_block += 1
                else:
                    if now_block == 2:
                        dim_to_be_optimized = line.replace('\n', '')
                        print('The dimension to be optimized is: ' + dim_to_be_optimized)
                        now_block += 1
                    else:
                        if now_block == 3:
                            predict_begin = line.replace('\n', '')
                            predict_end = f.readline().replace('\n', '')
                            print('Predict time begin at: ' + predict_begin)
                            print('Predict time end at: ' + predict_end)
                            print('\n')

    # Read the beginning time
    line = open(train_path, encoding='utf-8').readline()
    space_1 = line.find('\t')
    space_2 = line.find('\t', space_1 + 1)
    history_begin = line[space_2 + 1:].replace('\n', '')

    history_data = [[.0] for i in range(total_flavors)]
    for i in range(total_flavors):
        for j in range(time2val(history_begin), time2val(predict_begin) - 1):
            history_data[i].append(0)

    future_data = [[.0] for i in range(total_flavors)]
    for i in range(total_flavors):
        for j in range(time2val(predict_begin), time2val(predict_end) - 1):
            future_data[i].append(0)

    # Read history data
    for line in open(train_path, encoding='utf-8'):
        space_1 = line.find('\t')
        space_2 = line.find('\t', space_1 + 1)
        temp_flavor = int(line[space_1 + 7:space_2])
        temp_time = line[space_2 + 1:].replace('\n', '')
        if temp_time is not None:
            value = time2val(temp_time)
            if temp_flavor <= total_flavors:
                history_data[temp_flavor - 1][value] += 1
            else:
                pass
        #                print('Flavor data error.\n')
        #                print('Now flavor: ' + str(temp_flavor))
        else:
            print('Time data error.\n')

    # Print history data
    print('History data: ')
    print('Total diffs: ' + str(len(history_data[0])))
    for i in range(total_flavors):
        print('Flavor' + str(i + 1) + ': (Total: ' + str(sum(history_data[i])) + ')\n' + str(history_data[i]) + '\n')

    # Read test data
    for line in open(test_path, encoding='utf-8'):
        space_1 = line.find('\t')
        space_2 = line.find('\t', space_1 + 1)
        temp_flavor = int(line[space_1 + 7:space_2])
        temp_time = line[space_2 + 1:].replace('\n', '')
        if temp_time is not None:
            value = time2val(temp_time) - time2val(predict_begin) - 1
            if temp_flavor <= total_flavors:
                future_data[temp_flavor - 1][value] += 1
            else:
                pass
        #                print('Flavor data error.\n')
        #                print('Now flavor: ' + str(temp_flavor))
        else:
            print('Time data error.\n')

    # Print history data
    print('Future data: ')
    print('Total diffs: ' + str(len(future_data[0])))
    for i in range(total_flavors):
        print('Flavor' + str(i + 1) + ': (Total: ' + str(sum(future_data[i])) + ')\n' + str(future_data[i]) + '\n')
    #    plt.plot(history_data[2])

    return history_data, future_data, sample_ps, sample_vm, dim_to_be_optimized, history_begin,  predict_begin, predict_end, flavor_num


# =============================================================================
# Convert time into value
# =============================================================================
def time2val(time):
    year = time[0:4]
    month = time[5:7]
    day = time[8:10]

    # Convertion
    year = 365 * (int(year) - 2015)
    month = int(month)
    day = int(day)

    # To value
    value = 0
    month -= 1
    for i in range(0, month):
        value += days_of_month[i + 1]
    value += (day - 1) + year

    return value
