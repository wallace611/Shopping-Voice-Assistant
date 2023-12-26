from . import _association_rule
from . import _freq_item_set
import time
import os

FIS_time = 0.0
aso_time = 0.0
overall_time = 0.0

def fp_growth_from_file(args):
    name, minimum_support, minimum_confidence, limits, detailed_result, parallel = args.values()
    if parallel != 'always' and parallel != 'never':
        parallel = 'auto'
        
    print('\nSettings:\n')
    for item in args.items():
        print('\t' + str(item).strip('()').replace("'", '').replace(',', ':'))
    print('\nTimes:\n')
    

    global FIS_time
    global aso_time
    global overall_time
    
    # start FIS_time and overall_time
    FIS_time = overall_time = time.time()
    
    data = get_from_file(file_name=name)
    minimum_freq = int(minimum_support * len(data) + 1)

    freq_item = []
    freq_gen = _freq_item_set.find_frequent_itemsets(data, minimum_freq, limit=limits)
    for itemSet, support in freq_gen:
        freq_item.append((itemSet, support))
    
    # end FIS_time
    FIS_time = time.time() - FIS_time

    print('\tfrequency item set: ', FIS_time, 'seconds')

    #start aso_time
    aso_time = time.time()
    
    # calculating association rule
    if (len(freq_item) < 400000 and parallel == 'auto') or parallel == 'never':
        rules = _association_rule.caluculate_association_rule(freq_item, minimum_confidence, detailed_result)
    else:
        rules = _association_rule.caluculate_association_rule_parallel(freq_item, minimum_confidence, detailed_result)
    
    # end all the others timers
    end_time = time.time()
    aso_time = end_time - aso_time
    overall_time = end_time - overall_time
    
    print('\tassciation rules: ', aso_time, 'seconds')
    print('\toverall time: ', overall_time, 'seconds')
    
    return (freq_item, get_each_number(freq_item)) if detailed_result else get_each_number(freq_item), rules

def get_from_file(file_name):
    data_path = os.path.join(os.path.dirname(__file__), '..\\training_data\\' + file_name)
    data = []
    for line in open(data_path).readlines():
        temp = line.strip('\n').split(' ')
        data.append([*temp[0], temp[1]])

    return data

def get_each_number(freq_item_list):
    freq_item_set = {}
    for item_set, sup in freq_item_list:
        if len(item_set) in freq_item_set:
            freq_item_set[len(item_set)] += 1
        else:
            freq_item_set[len(item_set)] = 1
    return freq_item_set

def get_time():
    yield "frequency item set:", FIS_time
    yield "association rule:", aso_time
    yield "overall time:", overall_time