#!/usr/bin/env python
# encoding: utf-8

"""
@author: david
@time: 7/15/17 1:48 PM
"""

import re
import traceback
import MySQLdb

# import urllib2
# import os
# from urllib import urlopen

DATABASE = dict(
    host='localhost',
    user='tokenuser',
    passwd='123456%$',
    db='token'
)


def truncate_data():
    conn = MySQLdb.connect(**DATABASE)
    curs = conn.cursor()
    try:
        curs.execute("USE token");  # 指定数据库

        curs.execute("TRUNCATE TABLE cri");  # 指定数据库中的数据表
        conn.commit()  # 没有提交的话，无法完成插入
    except:
        conn.rollback()
        traceback.print_exc()
        return False
    finally:
        curs.close()
        conn.close()
    return True


def init_data(lstData):
    conn = MySQLdb.connect(**DATABASE)
    curs = conn.cursor()
    try:
        curs.executemany("insert into cri (CRI) values(%s)", lstData)
        conn.commit()  # 没有提交的话，无法完成插入
    except:
        conn.rollback()
        traceback.print_exc()
        return False
    finally:
        curs.close()
        conn.close()
    return True


def query_data():
    conn = MySQLdb.connect(**DATABASE)
    curs = conn.cursor()
    result = None
    try:
        result = curs.execute("SELECT * FROM cri")
    except:
        traceback.print_exc()
    finally:
        curs.close()
        conn.close()
    return result


def test_mysql_operation():
    assert truncate_data()
    fh = open("xx.txt")
    idPattern = r"\d{1,8}\.\d{1,8}"
    pattern = re.compile(idPattern)
    lstData = []
    for line in fh.readlines():
        match = pattern.findall(line)
        [lstData.append((_,)) for _ in match]
    assert init_data(lstData)
    data = query_data()
    return data


if __name__ == "__main__":
    data = test_mysql_operation()
    assert data
