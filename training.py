from source import analyzing_module

if __name__ == '__main__':
    module = analyzing_module()
    module.training()
    
    test = '你可以滾了'
    print(module.get_relative(test, rank=0))