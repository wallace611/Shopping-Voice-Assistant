from .fp_mining import _mining_module as mining
from itertools import combinations
from collections import defaultdict
import json
import os
import re

class analyzing_module:
    def __init__(self, get_from_json=True):
        self.args = {
            "data file": os.path.dirname(__file__) + "\\training\\" + "module_data.dat",
            "minimum support": 0.01,
            "minimum confidence": 0.8,
            "limit": 5,
            "write file": True,
            "parallel processing": "auto"
        }
        self.rule_list = {}
        success = True
        if get_from_json:
            # try to get the module from module.json
            success = self._read_module()
        else:
            print("mining module_data.dat to construct rule_list")
            self.rule_list = self._mine()
            self._save_module()
        if not success:
            # failed, mine the module from module_data.dat
            print("fail to find module, mining module_data.dat to construct rule_list")
            self.rule_list = self._mine()
            self._save_module()
    
    def get_relative(self, cmd, rank=1):
        cmd = re.sub(r'\d+', lambda x: f'#number#', cmd)
        cmd = re.findall(r'#+[number]+#|%+[\w\d]+%|[\w]', cmd)
        res = defaultdict(int)
        max_length = len(cmd) + 1 if len(cmd) <= self.args["limit"] else self.args["limit"]
        for k in range(1, max_length):
            for i in tuple([*combinations(cmd, k)]):
                try:
                    res[str(self.rule_list[i][0]).strip('[]').strip('\'')] += self.rule_list[i][1]
                except:
                    continue
        res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
        sum_val = sum(res.values())
        res = {k: v / sum_val for k, v in res.items()}
        res = [(k, v) for k, v in res.items()]
        if rank == 1 and len(res) > 0:
            return res[0]
        return res

    def training(self):
        print("mining module_data.dat to construct rule_list")
        self.rule_list = self._mine()
        # reading training data to a stack
        training_data_path = os.path.dirname(__file__) + "\\training\\training.dat"
        data_stack = []
        with open(training_data_path, 'r+', encoding='utf-8') as training_file:
            for line in training_file.readlines():
                data_stack.append(line)
            data_stack.reverse()
            training_file.truncate()
        data_stack = list(set(data_stack))
        
        # open module data
        module_data_path = os.path.dirname(__file__) + "\\training\\module_data.dat"
        with open(module_data_path, 'r', encoding='utf-8') as module_file:
            # get the data in module_file
            _module_data = [line.strip('\n') for line in module_file.readlines()]
        learned = [0, 0, len(data_stack)] # the tuple shows that how many training data was learned
        failed_statement = []
        
        # start training
        print("\nstart training...\n")
        counter = 0
        while (len(data_stack) > 0):
            counter += 1
            
            # get a line of training data
            line = data_stack[len(data_stack) - 1].strip('\n')
            data_stack.pop()
            try:
                # target is the expected result of cmd
                cmd, target = tuple(line.split(' '))
                # res is the actual result of cmd
                res = self.get_relative(cmd)
            except:
                continue
            # print result
            print("\n#{} module answer is {} {}, target is {}".format(counter, None if len(res) <= 0 else res[0], None if len(res) <= 0 else res[1], target))
            print("command: {}".format(line))
            
            # compare the expected result and actual result
            if (len(res) <= 0 or res[0] != target) or res[1] < 0.8:
                # module fail to identify the meaning of cmd
                if line in _module_data:
                    print(line + 'failed')
                    learned[1] += 1
                    failed_statement.append(line)
                
                else:
                    _module_data.append(cmd + ' ' + target)
                    learned[0] += 1
                
                    # training
                    print("failed, I thought it is {}".format(res))
                    print("start training...")
                    self.rule_list = self._mine(counter, data=_module_data)
                    data_stack.insert(0, line + '\n')
            else:
                # same, it remember
                print("I've learned this")
        
        print("\nlearn {} statement, fail {} statement from {}\n".format(learned[0], learned[1], learned[2]))
        if (len(failed_statement) > 0):
            print("failed statement: {}\nmaybe try others statement".format(failed_statement))
        
        self._save_module()
        
        with open(module_data_path, 'w', encoding='utf-8') as module_file:
            for line in _module_data:
                module_file.write(line + '\n')


    def _mine(self, tried='', data=None):
        print("#{} mining start".format(tried))
        freq, rule = mining.fp_growth_from_file(self.args, data=data)
        
        if self.args["write file"]:
            freq = freq[1]
            rule_d = rule[0]
            rule = rule[1]
        
        print("find association rules: {}".format(rule))

        print("#{} mining end".format(tried))
        print('done :D')
        return rule_d

    def _save_module(self):
        print("\nwriting file...")
            
        asso_to_json = [[[s for s in rules[0]],[v for v in rules[1]]] for rules in self.rule_list.items()]
        json_obj = json.dumps(asso_to_json)
        path = os.path.join(os.path.dirname(__file__), 'module_temp\\association_rule_module.json')
        with open(path, 'w', encoding='utf-8') as write_to_json:
            write_to_json.write(json_obj)
            
        print("done!")
            
    def _read_module(self):
        path = os.path.join(os.path.dirname(__file__), 'module_temp\\association_rule_module.json')
        try:
            with open(path, 'r', encoding='utf-8') as read_json:
                try:
                    json_to_asso = json.loads(read_json.read())
                    self.rule_list = {tuple(rules[0]):tuple(rules[1]) for rules in json_to_asso}
                except:
                    return False
            return True
        except:
            return False