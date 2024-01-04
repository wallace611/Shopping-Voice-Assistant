from source import analyzing_module

if __name__ == '__main__':
    module = analyzing_module()
    #module.training()
    
    test = '馬的貢丸'
    print(module.get_relative(test))