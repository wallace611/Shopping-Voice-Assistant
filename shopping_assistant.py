from source import analyzing_module
from source.voice_helper import *
from source.util import *

if __name__ == '__main__':
    # init
    module = analyzing_module()
    voice = voice_processer()
    end_program = False
    cart = shopping_cart()
    # while not close
    while not end_program:
        
        # keep detecting audio input
        say('我在聽')
        input_line = None
        while input_line == None:
            # input_line will be what the user said
            # if there's no audio input then input_line will be None
            input_line = voice.listening()
            if input_line == None:
                print('say something')
        
        input_line = chinese_to_number(input_line)
        print(input_line)
        # analyze the commend corresponding to the input_line
        command = module.get_relative(input_line, 0)
        print(command)
        
        try:
            command = command[0]
        except:
            command = ('%donothing%', 1.0)
            
        if command[1] < 0.5:
            command = ('%donothing%', 1.0)
        
        execute_command(command[0], input_line, cart)
