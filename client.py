#!/usr/bin/env  python
#coding:utf-8
__author__ = 'zhangjun'


import socket
import time
import sys
from getpass import getpass

HOST = 'localhost'    # The remote host
PORT = 8080              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while 1:
    user = raw_input('\033[32mPlease input your account:\033[0m').strip()
    s.sendall(user)
    data = s.recv(4096)
    if data == 'false':
        print '\033[31mNot a valid user!!!\033[0m'
        continue
    if data == 'ok':
        break
n = 1
for i in range(4):
    passwd = getpass('\033[32mPlease input your password:\033[0m').strip()
    s.sendall(passwd)
    data1 = s.recv(4096)
    if data1 == 'false':
        n += 1
        if n == 4:
            print '\033[31mLogin false!\033[0m'
            s.send('bye')
            s.close()
            sys.exit()
    if data1 == 'ok':
        print '\033[32mLogin success!!!\033[0m'
        break
while 1:
    user_input = raw_input("\033[34mftp-->\033[0m").strip()
    if len(user_input) ==0:continue
    if user_input == 'quit':break
    s.sendall(user_input)
    if user_input.split()[0] == 'put':
        with open(user_input.split()[1]) as f:
            s.sendall(f.read())
            time.sleep(0.5)
            s.send("FileSendDone")
        print 'transfer is done...'
    if user_input.split()[0] == 'get':
        f = file('%s' %user_input.split()[1], 'wb')
        while 1:
            data = s.recv(4096)
            if data == 'FileSendDone':
                print 'transfer is done...'
                break
            f.write(data)
        f.close()
    if len(user_input) > 1:
        data = s.recv(4096)
        if not data:continue
        print data
s.close()