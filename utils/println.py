def println(color, *args, **kwargs):
    try:
        color = color.lower()
    except AttributeError:
        print(*args, **kwargs)
        return
    if type(color) != str:
        raise TypeError('颜色值必须为字符串')
    # 自定义颜色,传入颜色值
    if color == 'green':
        print('\033[1;32m')
        print(*args, **kwargs)
        print('\033[0m')
    elif color == 'red':
        print('\033[1;31m')
        print(*args, **kwargs)
        print('\033[0m')
    elif color == 'yellow':
        print('\033[1;33m')
        print(*args, **kwargs)
        print('\033[0m')
    elif color == 'blue':
        print('\033[1;34m')
        print(*args, **kwargs)
        print('\033[0m')
    elif color == 'purple':
        print('\033[1;35m')
        print(*args, **kwargs)
        print('\033[0m')
    elif color == 'skyblue':
        print('\033[1;36m')
        print(*args, **kwargs)
        print('\033[0m')
    elif color == 'white':
        print('\033[1;37m')
        print(*args, **kwargs)
        print('\033[0m')
    else:
        print(*args, **kwargs)
