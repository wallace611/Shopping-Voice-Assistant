from .mining_source_code import _mining_module
from .mining_source_code import _module_training_result_mananger as trm
import threading
from itertools import combinations

def read(cmd, rank=3):
    res = []
    for k in range(1, len(cmd) + 1):
        for i in tuple([*combinations(cmd, k)]):
            try:
                res.append(rules[i])
            except:
                continue
    return res


def training(args):
    freq, rule = _mining_module.fp_growth_from_file(args)
    
    if args["write file"]:
        thread_write_file = threading.Thread(target=trm.write_in_file, args=(rule,))
        thread_write_file.start()
        freq = freq[1]
        rule_d = rule[0]
        rule = rule[1]
    
    print("\n\tfind association rules: {}".format(rule))

    try:
        thread_write_file.join()
        print('done :D')
    except:
        print('done!')
    
    return rule_d

args = {
    "data file": "test.dat",
    "minimum support": 0.0,
    "minimum confidence": 0.8,
    "limit": 5,
    "write file": True,
    "parallel processing": "auto" # "always", "never", others = "auto"
}

rules = training(args)