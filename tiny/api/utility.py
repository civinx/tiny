import re

char_set = [chr(num+ord('0')) for num in range(0, 10)]
low_case_set = [chr(num+ord('a')) for num in range(0, 26)]
upper_case_set = [chr(num+ord('A')) for num in range(0, 26)]
char_set.extend(low_case_set)
char_set.extend(upper_case_set)


def gen(record_id):
    n = char_set.__len__()
    result = ''
    for i in range(5):
        result = result + char_set[record_id % n]
        record_id = record_id // n
    result = result[::-1]
    return result


def star_with_http(url):
    if re.match(r'https?:/{2}\w.+$', url):
        return True
    else:
        return False


def delete_http(url):
    if not star_with_http(url):
        return url
    if url.startswith("http://"):
        url = url[7:]
    else:
        url = url[8:]
    return url
