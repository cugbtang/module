# -*- coding:utf-8 -*-
# vim: set fileencoding=utf-8
import os
from db import MysqlConnect
from scapy.all import sniff,wrpcap,Raw, IP, TCP

db = MysqlConnect(host="localhost", user="root", passwd="111111", db="alarmtoax")

def get_pcap(ifs,ip=None,size=100):
    ''' 获取指定 ifs(网卡), 指定数量size 的数据包;
        如果有指定ip，则这里只接收tcp，80端口，指定ip的包 '''
    filter = ""
    if ip:
        filter += "host 192.168.1.130 and port 443"
        print (filter)
        # dpkt = sniff(iface=ifs,filter=filter,count=size)
        dpkt = sniff(iface=ifs,filter=filter)
        # sql = "inster into test (sip,dip) values(%s,%s)" % dpkt[0][IP].src, dpkt[0][IP].dst
        sql = "insert into test (sip,dip) values(%s,%s)"
        data = [dpkt[0][IP].src, dpkt[0][IP].dst]
        db.exec_data(sql,data)
        return dpkt
    else:
        dpkt = sniff(iface=ifs,count=size)
    # wrpcap("pc1.pcap",dpkt) # 保存数据包到文件

    return dpkt


def get_ip_pcap(ifs,sender,size):
    ''' 获取指定 ifs(网卡), 指定发送方 sender(域名或ip) 的数据包
        size：(一次获取数据包的数量） '''
    if 'www.' in sender:
        v = os.popen('ping %s'%sender).read()
        ip = v.split()[8]
        print(u"准备接收IP为 %s 的数据包..."%ip)
    else:
        ip = sender
        print(u"准备接收IP为 %s 的数据包..."%ip)
    count = 0
    while count<10:
        d = get_pcap(ifs,ip,size)
        for i in d:
            try:
                if i[Raw]: # 发送方的IP为：ip  接收方的IP：i[IP].dst==ip
                    print(i[Raw].load)
            except:
                pass
        count+=1

def main():
    ifs = 'Realtek PCIe GBE Family Controller' # 网卡
    ip = "192.168.1.130"  # ip地址，也可写域名，如：www.baidu.com
    get_ip_pcap(ifs,ip,size=1)  # 一次接收一个包

if __name__ =='__main__':
    main()