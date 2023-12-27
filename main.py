from source import analyzing_module


if __name__ == '__main__':
    module = analyzing_module()
    module.training()
    input_str = "老哥幫個忙"
    print(module.get_relative(input_str, 0))