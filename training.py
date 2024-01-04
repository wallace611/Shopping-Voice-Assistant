from source import analyzing_module

if __name__ == '__main__':
    module = analyzing_module()
    module.training()
    
    test = '我今天做了10下伏地挺身'
    print(module.get_relative(test, rank=0))