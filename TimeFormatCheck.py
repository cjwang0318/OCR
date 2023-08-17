# -*- coding:utf-8 -*-
import time
import re
import datefinder  # pip install datefinder
from dateutil import parser


def insert_date(date):
    char_to_replace = {' ': '-01-', '-': '-01-', ':': '-01-', '.': '-01-', '/': '-01-'}
    # Iterate over all key-value pairs in dictionary
    for key, value in char_to_replace.items():
        # Replace key character with value character in string
        date = date.replace(key, value)
    return date


def isVaildDate(date):
    if not re.search(r'((19|20)\d{2}( |-|:|.|\/)(0[1-9]|1[0-2]))', date) == None:  # check %Y%M 2023-08
        flag = True
        match = re.search(r'((19|20)\d{2}( |-|:|.|\/)(0[1-9]|1[0-2]))', date)
        result = match.group(0)
        if len(result) < 8:
            date = date.replace(result, result + "-01")
    elif not re.search(r'((0[1-9]|1[0-2])( |-|:|.|\/)(19|20)\d{2})', date) == None:  # check %M%Y 08/2023
        flag = True
        match = re.search(r'((0[1-9]|1[0-2])( |-|:|.|\/)(19|20)\d{2})', date)
        result = match.group(0)
        if len(result) < 8:
            date = insert_date(date)
    elif not re.search(r'((0[1-9]|1[0-2])(19|20)\d{2})', date) == None:  # check %Y%M 082023
        flag = True
    elif not re.search(r'((0[1-9]|1[0-2])(\/)(2)\d{1})', date) == None:  # check %Y%M 08/23
        flag = True
        date = date.replace("/", "/01/")
    elif not re.search(r'\d{1}年', date) == None:  # check %Y年 2023年
        flag = True
    else:
        flag = False
    return flag, date


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
            match = re.search(r'((19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))', date)  # for this format 20230318
            if match == None:
                # match = re.search(r'(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])(0[1-9]|[123]\d)',date)  # for this format 290722 start from 2001
                match = re.search(r'(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])(2[1-9]|[3]\d)',
                                  date)  # for this format 290722 start from 2020
    except:
        return None
    if not match == None:
        result = match.group(0)
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
    try:
        d = parser.parse(str1)
        str1 = d.strftime("%Y-%m-%d")
        return str1
    except:
        return "0000-00-00"


def get_result(check_list):
    date_list = []
    # first check by datefinder api
    for str in check_list:
        flag, str = isVaildDate(str)
        # print(f"Vaild_Date={flag}, date={str}")
        if flag:
            result = extractDate1(str)
            if len(result) == 0:
                # second check by RE
                result = extractDate2(str)
                if not result == None:
                    date_list.append(result)
            else:
                date_list.extend(result)
        else:
            continue
    for index, value in enumerate(date_list):  # normalization
        normalized_value = normalization(value)
        date_list[index] = normalized_value
    date_list = list(filter(("0000-00-00").__ne__, date_list))  # remove "0000-00-00"
    date_list = list(dict.fromkeys(date_list))  # remove duplicate
    date_list.sort()  # sort by dat
    if len(date_list) > 2:  # Get first and last date
        date_list = date_list[::len(date_list) - 1]
    return date_list


if __name__ == '__main__':
    # test_time_list = ["KFG:2020.06.19",'290722', '生產日期：2020 07 14QQ~我', '生產日期：2020-07-14QQ~我',
    # '生產日期：2020:07:14QQ~我',
    # '生產日期：2021.07.14QQ~我', '20230318', '生產日期：2020年07月14日QQ~我']
    test_time_list = ['PPGXXXXX-13-DEACYLTETRADECE', '202111.12', "12/24", '03-2026']
    print(get_result(test_time_list))
