#!/usr/bin/env  python
__author__ = 'zhangjun'

import MySQLdb
import base64
from prettytable import PrettyTable

m = MySQLdb.connect(host='localhost',user='root',passwd='westos',db='ftp')
f = m.cursor()

def search():
    while 1:
        name = raw_input('\033[32mWho you want to find info:\033[0m').strip()
        if len(name) == 0:continue
        break
    f.execute("select * from ftp_user where user='%s';"%name)
    a = f.fetchall()
    if not a:
        return "\033[31mnot a valid user!!!\033[0m"
    x = PrettyTable(['Name','Password'])
    x.padding_width = 1
    x.add_row([a[0][0],base64.b64decode(a[0][1])])
    return x

def insert():
    while 1:
        name = raw_input('\033[32mplease input new user name:\033[0m').strip()
        if len(name) == 0:continue
        break
    while 1:
        passwd = raw_input('\033[32mplease input the user passwd:\033[0m').strip()
        if len(passwd) == 0:continue
        break
    f.execute("insert into ftp_user values('%s','%s');" %(name,base64.b64encode(passwd)))
    m.commit()
    print '\033[31mSuccess add...\033[0m'


def update():
    while 1:
        name = raw_input('\033[32mplease input the update user name:\033[0m').strip()
        if len(name) == 0:continue
        break
    while 1:
        passwd = raw_input('\033[32mplease input the new passwd:\033[0m').strip()
        if len(passwd) == 0:continue
        break
    f.execute("update ftp_user set password='%s' where user='%s';"%(base64.b64encode(passwd),name))
    m.commit()
    print 'Update success...'

def delete():
    while 1:
        name = raw_input('\033[32mwho you want to delete:\033[0m').strip()
        if len(name) == 0:continue
        break
    while 1:
        choose = raw_input('\033[31mAre you sure delete it?(y/n)\033[0m').strip()
        if len(choose) == 0:continue
        if choose not in ['y','n']:
            print 'only 2 choice,y or n...'
            continue
        break
    if choose == 'y':
        f.execute("delete from ftp_user where user='%s';"%name)
        m.commit()
        print '\033[31mdelete success...\033[0m'

print '''\033[32mMenu:
        1,select info
        2,modify info
        3,delete info
        4,insert info
        5,exit\033[0m'''

while True:
    choose = raw_input('\033[33mPlease input your choose:\033[0m').strip()
    if len(choose) == 0:continue
    if choose not in ['1','2','3','4','5','exit']:
        print 'Only six option...'
        continue
    if choose == '1':
        print search()
    if choose == '2':
        update()
    if choose == '3':
        delete()
    if choose == '4':
        insert()
    if choose == '5':
        f.close()
        m.close()
        break
    if choose == 'exit':
        f.close()
        m.close()
        break