# __author__ = "Amos"
# Email: 379833553@qq.com
# Company: 佛山科瑞森科技有限公司


def convert_to_int(value,default=0):

    try:
        result = int(value)
    except Exception as e:
        result = default

    return result

def convert_mb_to_gb(value,default=0):

    try:
        value = value.strip('MB')
        result = int(value)
    except Exception as e:
        result = default

    return result