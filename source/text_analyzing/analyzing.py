from .mining_module import _mining_module as mining
from itertools import combinations
from collections import defaultdict
import threading
import json
import os
import re

class analyzing_module:
    def __init__(self) -> None:
        self.args = {
            "data file": os.path.dirname(__file__) + "\\training_module\\" + "module_data.dat",
            "minimum support": 0.0,
            "minimum confidence": 0.8,
            "limit": 5,
            "write file": True,
            "parallel processing": "never"
        }
        success = self.read_module()
        if not success:
            print("fail to find module, mining module_data.dat to construct rule_list")
            self.rule_list = self.mine(self.args)
    
    def get_relative(self, cmd, rank=1):
        cmd = re.sub(r'\d+', lambda x: f'#number#', cmd)
        cmd = re.findall(r'#+[number]+#|%+[\w\d]+%|[\w]', cmd)
        res = defaultdict(int)
        for k in range(1, len(cmd) + 1):
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
        training_data_path = os.path.dirname(__file__) + "\\training_module\\training_data\\training.dat"
        data_stack = []
        with open(training_data_path, 'r+') as training_file:
            for line in training_file.readlines():
                data_stack.append(line)
            data_stack.reverse()
            training_file.truncate()
        
        module_data_path = os.path.dirname(__file__) + "\\training_module\\module_data.dat"
        with open(module_data_path, 'a') as module_file:
            learned = [0, len(data_stack)]
            counter = 0
            while (len(data_stack) > 0):
                self.rule_list = self.mine(self.args, counter)
                counter += 1
                line = data_stack[len(data_stack) - 1]
                data_stack.pop()
                try:
                    cmd, target = tuple(line.strip('\n').split(' '))
                    res = self.get_relative(cmd)
                except:
                    continue
                
                print("\nAI answer is {} {}, target is {}\n".format(None if len(res) <= 0 else res[0], None if len(res) <= 0 else res[1], target))
                if (len(res) <= 0 or res[0] != target) or res[1] < 0.7:
                    module_file.write(cmd + ' ' + target + '\n')
                    learned[0] += 1
                    
        self.rule_list = self.mine(self.args, "sum up")
        print("learn {} statement from {}\n".format(learned[0], learned[1]))
        
        self.save_module(self.rule_list)


    def mine(self, args, tried=0):
        print("#{} mining start".format(tried))
        freq, rule = mining.fp_growth_from_file(args)
        
        if args["write file"]:
            freq = freq[1]
            rule_d = rule[0]
            rule = rule[1]
        
        print("find association rules: {}".format(rule))

        print("#{} mining end".format(tried))
        print('done :D')
        return rule_d

    def save_module(self, association_rule):
        print("\nwriting file...")
            
        asso_to_json = [[[s for s in rules[0]],[v for v in rules[1]]] for rules in association_rule.items()]
        json_obj = json.dumps(asso_to_json)
        path = os.path.join(os.path.dirname(__file__), '..\\..\\rule_module\\module.json')
        with open(path, 'w') as write_to_json:
            write_to_json.write(json_obj)
            
    def read_module(self):
        path = os.path.join(os.path.dirname(__file__), '..\\..\\rule_module\\module.json')
        with open(path, 'r') as read_json:
            try:
                json_to_asso = json.loads(read_json.read())
                self.rule_list = {tuple(rules[0]):tuple(rules[1]) for rules in json_to_asso}
            except:
                return False
        return True