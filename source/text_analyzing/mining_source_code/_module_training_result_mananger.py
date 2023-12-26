import os
import time

def write_in_file(association_rule):
    print("\nwriting file...")
    
    path = os.path.join(os.path.dirname(__file__), '..\\results\\module.dat')
    file_to_write = open(path, 'w')
    for rules in association_rule[0].items():
        file_to_write.write(str(rules).strip('[]') + '\n')
    
    print("done, the file located at: \"{}\"".format(path))
