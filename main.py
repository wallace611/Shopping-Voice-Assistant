from source import analyzing_module


if __name__ == '__main__':
    module = analyzing_module()
    #module.training()
    input_str = "不用花錢"
    print(module.get_relative(input_str, 0))
