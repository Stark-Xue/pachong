#!/usr/bin/python3
# -*- coding: utf-8 -*-

import asyncore
import sys
import socket
from queue import Queue

DATA_PACKET_TYPE_SEND = 689
DATA_PACKET_TYPE_RECV = 690

# 数据包进行对象化封装，方便以后实现对象和二进制数据之间的转换
class DataPacket():
    def __init__(self, type=DATA_PACKET_TYPE_SEND, content=''):
        # 数据包的类型
        self.type = type
        # 数据部分内容
        self.content = content
        # 加密字段
        self.encrypt_flag = 0
        #保留字段
        self.preserve_flag = 0

    def get_length(self):
        """
        获取当前数据包的长度
        :return:
        """
        return 4+2+1+1+len(self.content.encode('utf-8'))+1


    def get_bytes(self):
        """
        获取二进制数据
        :return:
        """
        data = bytes()
        # 构建4个字节的消息长度数据
        data_packet_length = self.get_length()
        '''
        to_bytes 把一个整形数据转换成二进制数据
        第一个参数 表示需要转换的二进制数据占几个字节
        第二个参数 byteorder 描述字节序
        第三个参数 signed 描述是否有符号
        '''
        # 处理消息长度
        data += data_packet_length.to_bytes(4, byteorder='little', signed=False)
        # 处理消息类型
        data += self.type.to_bytes(2, byteorder='little', signed=False)
        # 处理加密字段
        data += self.encrypt_flag.to_bytes(1, byteorder='little', signed=False)
        # 处理保留字段
        data += self.preserve_flag.to_bytes(1, byteorder='little', signed=False)

        # 处理数据部分
        data += self.content.encode('utf-8')

        # 添加结尾 '\0'
        data += b'\0'

        return  data



class DouyuClient(asyncore.dispatcher):

    def __init__(self, host, port):

        # 构建发送数据包的容器
        # 存放数据包对象
        self.send_queue = Queue()


        asyncore.dispatcher.__init__(self)
        self.create_socket()

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
        return self.send_queue.qsize() > 0

    def handle_write(self):
        """有数据要被发送时触发，通常情况下在该函数中编写send方法发送数据"""
        # 调用send方法发送数据，参数是字节数据
        print('准备发送：')

        # 从数据包队列中获取数据包对象
        dp = self.send_queue.get()

        # 获取数据包的长度并发送给服务器
        dp_length = dp.get_length()
        dp_length_bytes = dp_length.to_bytes(4, byteorder='little', signed=False)
        self.send(dp_length_bytes)

        # 发送二进制数据包
        self.send(dp.get_bytes())
        self.send_queue.task_done()


        pass

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
        print(t,e,trace)
        self.close()

    def handle_close(self):
        """当连接被关闭"""
        print("连接关闭")

        self.close()

    def login_room_id(self, room_id):
        # 构建登录数据包
        content = "type@=loginreq/roomid@={}/".format(room_id)
        login_dp = DataPacket(DATA_PACKET_TYPE_SEND, content)

        # 把数据包添加到发送数据包队列容器中
        self.send_queue.put(login_dp)





if __name__ == '__main__':
    douyu_client = DouyuClient("wss://danmuproxy.douyu.com", 8504)
    douyu_client.login_room_id(5574575)

    asyncore.loop(timeout=15)