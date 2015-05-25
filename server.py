#!/usr/bin/env  python
#coding:utf-8
__author__ = 'zhangjun'


import SocketServer,time
import MySQLdb,base64
import commands,os

class verify:
    def search(self,name):
        m = MySQLdb.connect(host='localhost',user='root',passwd='westos',db='ftp')
        f = m.cursor()
        f.execute("select * from ftp_user where user='%s';"%name)
        a = f.fetchall()
        return a

class MyTCPHandler(SocketServer.BaseRequestHandler,verify):
    def handle(self):
        while 1:
            user = self.search(self.request.recv(4096))
            if not user:
                self.request.sendall('false')
                continue
            if user:
                self.request.sendall('ok')
                break
        while 1:
            passwd = self.request.recv(4096)
            if  base64.b64decode(user[0][1]) == passwd:
                self.request.sendall('ok')
                print "Client is connected..", self.client_address[0]
                if not os.path.exists('/ftp/%s' %user[0][0]):
                    os.system('mkdir /ftp/%s' %user[0][0])
                os.chdir('/ftp/%s' %user[0][0])
                break
            elif passwd == 'bye':
                break
            else:
                self.request.sendall('false')
                continue
        while 1:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                print "Client is disconnected..", self.client_address[0]
                break

            if self.data.split()[0] == 'put':
                print "Going to receive file ", self.data.split()[1]
                f = file('/ftp/%s/%s' %(user[0][0],self.data.split()[1]), 'wb')
                while 1:
                    data = self.request.recv(4096)
                    if data == "FileSendDone":
                        print "Transfer is done.."
                        break
                    f.write(data)
                f.close()
                break

            if self.data.split()[0] == 'get':
                print "Going to send file...",self.data.split()[1]
                with open('/ftp/%s/%s' %(user[0][0],self.data.split()[1])) as f:
                    self.request.sendall(f.read())
                    time.sleep(0.5)
                    self.request.send("FileSendDone")

            if len(self.data) > 1:
                if self.data.split()[0] in ['ls','pwd','rm','mv','touch','mkdir','help']:
                    if self.data.split()[0] == 'help':
                        self.request.sendall('\033[31mls...列出文件和目录\npwd...显示当前所在路径\nrm...删除文件\nmv...改名 移动文件\ntouch...创建文件\nmkdir...创建目录\nhelp...帮助\033[0m')
                        continue
                    print 'going to run cmd:',self.data
                    status, result = commands.getstatusoutput(self.data)
                    if len(result) ==0:result = "CMD is has been executed!"
                    self.request.sendall(result)
                else:
                    self.request.sendall('The command is not available')


if __name__ == "__main__":
    HOST, PORT = "",8080
    server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()