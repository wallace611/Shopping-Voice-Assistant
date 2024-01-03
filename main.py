from source import analyzing_module
from source import voice_processer
import threading


if __name__ == '__main__':
    training = False
    module = analyzing_module()
    voice = voice_processer()
    
    if training:
        train_thread = threading.Thread(target=module.training)
        train_thread.start()
    
    input_str = "早上好中國"
    voice.say(input_str)
    print(module.get_relative(input_str, 0))
    
    try:
        train_thread.join()
    
    except:
        pass
