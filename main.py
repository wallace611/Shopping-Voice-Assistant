from source import analyzing_module


if __name__ == '__main__':
    module = analyzing_module()
    #module.training()
    input_str = "去你的"
    print(module.get_relative(input_str, 0))