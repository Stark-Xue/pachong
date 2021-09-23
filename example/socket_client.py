#!/usr/bin/python3
# -*- coding: utf-8 -*-

import asyncore
import sys

# 1. 定义类继承自 asyncore.dispatcher
class SocketClient(asyncore.dispatcher):

    # 2. 实现类中的回调函数

    def __init__(self, host, port):
        # 调用父类的方法
        asyncore.dispatcher.__init__(self)

        # 创建 Socket 服务器
        self.create_socket()

        # 连接服务器
        address = (host, port)
        self.connect(address)


    def handle_connect(self):
        """当 socket 连接成功服务器时回调"""
        print("连接成功")

    def writable(self):
        """
        描述是否有数据需要被发送到服务器
        True：可写；False：不可写
        如果不实现默认返回True
        如果返回True，回调函数handle_write将被触发
        """
        return False

    def handle_write(self):
        """有数据要被发送时触发，通常情况下在该函数中编写send方法发送数据"""
        # 调用send方法发送数据，参数是字节数据
        self.send("hello world".encode('utf-8'))

    def readable(self):
        """
        描述是否有数据从服务器读取
        True：有数据需要读取；False：没有数据需要读取
        如果不实现默认返回True
        如果返回True，回调函数handle_read将被触发
        """
        return True

    def handle_read(self):
        """有数据要被读取时触发，通常情况下在该函数中编写recv方法读取数据"""
        result = self.recv(1024).decode('utf-8')
        print(result)

    def handle_error(self):
        """当程序运行过程中发生错误"""
        t, e, trace = sys.exc_info()
        # print(t,e,trace)
        self.close()

    def handle_close(self):
        """当连接被关闭"""
        print("连接关闭")

        self.close()


# 3. 创建对象并执行 asyncore.loop 进入运行循环
if __name__ == '__main__':
    client = SocketClient('127.0.0.1', 9000)

    asyncore.loop(timeout=5)