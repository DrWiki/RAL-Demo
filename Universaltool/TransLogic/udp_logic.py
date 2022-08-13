import Signal
import stopThreading
import socket
import threading
import struct
class UdpLogic(Signal.Signals):
    def __init__(self):
        super(UdpLogic, self).__init__()
        self.udp_socket = None
        self.udp_sever_th = None
        self.udp_port1 = 8080
        self.udp_ip1 = "0.0.0.0"
        self.udp_port2 = 8080
        self.udp_ip2 = "0.0.0.0"
        self.link = False

    def udp_server_start(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            address = ('', self.udp_port1)
            self.udp_socket.bind(address)
            self.link = True
        except Exception as ret:
            self.signal_write_msg.emit('请检查端口号\n')
        else:
            self.udp_sever_th = threading.Thread(target=self.udp_server_concurrency)
            self.udp_sever_th.start()
            self.signal_write_msg.emit('UDP服务端正在监听端口:{}\n'.format(self.udp_port1))

    def udp_server_concurrency(self):
        numnum = 0
        while True:
            recv_msg, recv_addr = self.udp_socket.recvfrom(500)
            # print(recv_msg, type(recv_msg),len(recv_msg))
            # a, b, c, d, e, f,_,_ = struct.unpack('<ffffffcc', recv_msg)
            # print(a,b,c,d,e,f)
            # msg = recv_msg.decode('utf-8')
            # print(len(recv_msg))
            if len(recv_msg)==22:
                self.signal_PackedDataComing.emit(recv_msg[0:20])
                numnum += 1
                if numnum == 5:
                    numnum = 0
                    self.udp_socket.sendto(recv_msg, ("192.168.43.167", 9999))
            else:
                msg = recv_msg.decode('utf-8')
                print("recv_msg", recv_msg)
                msg = 'from IP :{} port :{}: {}\n'.format(recv_addr[0], recv_addr[1], msg)
                self.signal_write_msg.emit(msg)

    def udp_send(self, sendstr):
        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                send_msg = sendstr.encode('utf-8')
                self.udp_socket.sendto(send_msg, (self.udp_ip2, self.udp_port2))
                msg = 'UDP客户端已发送\n'
                self.signal_write_msg.emit(msg)
            except Exception as ret:
                msg = '发送失败\n'
                self.signal_write_msg.emit(msg)

    def udp_send_2(self, sendstr):
        if self.link is False:
            msg = '请选择服务，并点击连接网络\n'
            self.signal_write_msg.emit(msg)
        else:
            try:
                self.udp_socket.sendto(25, ("192.168.43.167", 9999))
                msg = 'UDP客户端已发送\n'
                self.signal_write_msg.emit(msg)
            except Exception as ret:
                msg = '发送失败\n'
                self.signal_write_msg.emit(msg)

    def udp_close(self):
        try:
            stopThreading.stop_thread(self.udp_sever_th)
        except Exception:
            pass

        try:
            self.udp_socket.close()
            if self.link is True:
                msg = '已断开网络\n'
                self.signal_write_msg.emit(msg)
        except Exception as ret:
            pass
        self.link = False
