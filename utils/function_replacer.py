import re

import utils.global1 as global1


def replace_functions(value):
    if isinstance(value, dict):
        for key, val in value.items():
            value[key] = replace_functions(val)
    elif isinstance(value, list):
        for i in range(len(value)):
            value[i] = replace_functions(value[i])
    elif isinstance(value, str):
        match = re.match(r"\$(.+)", value)
        if match:
            function_name = match.group(1)
            if hasattr(global1, function_name):
                func = getattr(global1, function_name)
                new_value = func()
                print(f"函数 {function_name} 执行结果：{new_value}")  # 打印函数执行结果
                return new_value
    return value


# 测试用例
test_dict = {
    'key1': '$get_count',
    'key2': {
        'sub_key1': '$get_count',
        'sub_key2': 'normal_string'
    },
    'key3': ['$get_count', 'normal_string']
}

print("替换前的字典：", test_dict)
replaced_dict = replace_functions(test_dict)
print("替换后的字典：", replaced_dict)
