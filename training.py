from source import analyzing_module

if __name__ == '__main__':
    module = analyzing_module()
    #module.training()
    
    test = ''
    print(module.get_relative(test, rank=0))