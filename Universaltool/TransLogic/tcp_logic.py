import Signal
import socket
import threading
import stopThreading
import time


class TcpLogic(Signal.Signals):

    def __init__(self):
        super(TcpLogic, self).__init__()
        self.tcp_socket = None
        self.tcp_sever_th = None
        self.tcp_client_th = None
        self.tcp_client_socket_list = list()
        self.tcp_ip1 = "0.0.0.0"
        self.tcp_port1 = 8080
        self.tcp_link = False  # 用于标记是否开启了连接

    def tcp_server_start(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.tcp_socket.setblocking(False)
        try:
            self.tcp_socket.bind((self.tcp_ip1, self.tcp_port1))
        except Exception as ret:
            msg = '请检查端口号\n'
            self.signal_write_msg.emit(msg)
        else:
            self.tcp_socket.listen()
            self.tcp_sever_th = threading.Thread(target=self.tcp_server_concurrency)
            self.tcp_sever_th.start()
            msg = 'TCP服务端正在监听端口:%s\n' % str(self.tcp_port1)
            self.signal_write_msg.emit(msg)

    def tcp_server_concurrency(self):
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as ret:
                time.sleep(0.001)
            else:
                client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表,client_address为ip和端口的元组
                self.tcp_client_socket_list.append((client_socket, client_address))
                self.signal_NewClientAdded.emit(client_address)
                msg = 'TCP服务端已连接IP:%s端口:%s\n' % client_address
                self.signal_write_msg.emit(msg)
                self.tcp_link = True
            # 轮询客户端套接字列表，接收数据
            for client, address in self.tcp_client_socket_list:
                try:
                    recv_msg = client.recv(1024)
                    # print(recv_msg)
                    # print(len(recv_msg))
                    if len(recv_msg)==100:
                        self.signal_PackedDataComing.emit(recv_msg)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        pass
                        # msg = recv_msg.decode('utf-8')
                        # self.signal_NewDataComing.emit(msg)
                        # msg = 'TCP from IP :{} port:{}:\n{}\n'.format(address[0], address[1], msg)
                        # self.signal_write_msg.emit(msg)
                    else:
                        client.close()
                        self.tcp_client_socket_list.remove((client, address))

    def tcp_send(self, sendstr):
        """
        功能函数，用于TCP服务端和TCP客户端发送消息
        :return: None
        """
        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                send_msg = sendstr.encode('utf-8')
                if self.comboBox_tcp.currentIndex() == 0:
                    # 向所有连接的客户端发送消息
                    for client, address in self.tcp_client_socket_list:
                        client.send(send_msg)
                    msg = 'TCP服务端已发送\n'
                    self.signal_write_msg.emit(msg)
                if self.comboBox_tcp.currentIndex() == 1:
                    self.tcp_socket.send(send_msg)
                    msg = 'TCP客户端已发送\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                msg = '发送失败\n'
                self.signal_write_msg.emit(msg)

    def tcp_close(self):

        try:
            stopThreading.stop_thread(self.tcp_sever_th)
        except Exception:
            pass

        try:
            for client, address in self.tcp_client_socket_list:
                client.close()
            self.tcp_socket.close()
            if self.tcp_link is True:
                msg = 'Clients已断开网络\n'
                self.signal_write_msg.emit(msg)
        except Exception as ret:
            pass

        try:
            self.tcp_socket.close()
            if self.tcp_link is True:
                msg = 'Server已断开网络\n'
                self.signal_write_msg.emit(msg)
        except Exception as ret:
            pass
        self.tcp_link = False


