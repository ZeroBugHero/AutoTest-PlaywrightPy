import re


def regex_match(string):
    """
    使用正则表达式匹配字符串
    :param string: 要匹配的字符串
    :return: 匹配结果
    """
    # 使用re.escape来处理可能的特殊字符
    escaped_string = re.escape(string)
    match = re.compile(r'{}'.format(escaped_string))
    return match


if __name__ == '__main__':
    print(regex_match('个人信息'))
