from source import analyzing_module
from source import voice_processer
from collections import defaultdict
import threading

shopping_cart = defaultdict()
budget = 0


def execute_command(cmd, input_line):
    pass


if __name__ == '__main__':
    # init
    module = analyzing_module()
    voice = voice_processer()
    end_program = False
    
    # while not close
    while not end_program:
        
        # keep detecting audio input
        voice.say('我在聽')
        input_line = None
        while input_line == None:
            # input_line will be what the user said
            # if there's no audio input then input_line will be None
            input_line = voice.listening()
            if input_line == None:
                print('say something')
        
        print(input_line)
        # analyze the commend corresponding to the input_line
        command = module.get_relative(input_line, 0)
        print(command)
        
        command = command[0]
        
        execute_command(command, input_line)
