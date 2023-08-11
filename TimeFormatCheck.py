import time
import re
import datefinder  # pip install datefinder
from dateutil import parser

def isVaildDate(date):
    try:
        if " " in date:
            time.strptime(date, "%Y %m %d")
        elif "-" in date:
            time.strptime(date, "%Y-%m-%d")
        elif ":" in date:
            time.strptime(date, "%Y:%m:%d")
        elif "." in date:
            time.strptime(date, "%Y.%m.%d")
        elif "/" in date:
            time.strptime(date, "%Y/%m/%d")
        elif "年" in date:
            time.strptime(date, "%Y年%m月%d日")
        else:
            time.strptime(date, "%Y%m%d")
        return True
    except:
        return False


def extractDate2(date):
    try:
        if " " in date:
            match = re.search(r'(\d+ \d+ \d+)', date)
        elif "-" in date:
            match = re.search(r'(\d+-\d+-\d+)', date)
        elif ":" in date:
            match = re.search(r'(\d+:\d+:\d+)', date)
        elif "." in date:
            match = re.search(r'(\d+.\d+.\d+)', date)
        elif "/" in date:
            match = re.search(r'(\d+/\d+/\d+)', date)
        elif "年" in date:
            match = re.search(r'(\d+年\d+月\d+日)', date)
        else:
            match = re.search(r'((19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))', date)
    except:
        return None
    if not match == None:
        result = match.group(1)
        # print(result)
        return result
    else:
        # print("No date string match")
        return None


def extractDate1(date):
    match_list = []
    matches = datefinder.find_dates(date)
    for match in matches:
        # print(str(match)[:10])
        match_list.append(str(match)[:10])
    return match_list


def normalization(str1):
    char_to_replace = {':': '-', '年': '-', '月': '-', '日': ''}
    # Iterate over all key-value pairs in dictionary
    for key, value in char_to_replace.items():
        # Replace key character with value character in string
        str1 = str1.replace(key, value)
    d = parser.parse(str1)
    str1=d.strftime("%Y-%m-%d")
    return str1


def get_result(check_list):
    date_list = []
    # first check by datefinder api
    for str in check_list:
        result = extractDate1(str)
        if len(result) == 0:
            # second check by RE
            result = extractDate2(str)
            if not result == None:
                date_list.append(result)
        else:
            date_list.extend(result)
    for index, value in enumerate(date_list): #normalization
        date_list[index] = normalization(value)
    date_list = list(dict.fromkeys(date_list))  # remove duplicate
    date_list.sort()  # sort by dat
    return date_list


if __name__ == '__main__':
    test_time_list = ['290722', '生產日期：2020 07 14QQ~我', '生產日期：2020-07-14QQ~我',
                      '生產日期：2020:07:14QQ~我',
                      '生產日期：2020.07.14QQ~我', '20230318', '生產日期：2020年07月14日QQ~我']
    print(get_result(test_time_list))
