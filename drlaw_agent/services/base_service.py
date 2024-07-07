def convert_to_str(f):
    if f > 1e8:
        f = f / 1e8
        return f"{round(f, 2):.2f}" + "亿"
    if f > 1e4:
        f = f / 1e4
        return f"{round(f, 2):.2f}" + "万"
    return f"{round(f, 2):.2f}"


def convert_to_float(s):
    if s is None:
        return 0

    # 使用正则表达式将字符串中的数字和中文符号替换为英文符号
    s = s.replace("亿", "e8").replace("万", "e4")

    try:
        # 使用float函数将字符串转换为浮点数
        result = float(s)
    except Exception as e:
        result = 0

    return result
