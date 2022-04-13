from os import system

from scapy.all import *
from scapy.layers.inet import TCP
from scapy.layers.inet import IP
from scapy.layers.l2 import ARP


def scan_ips():
    p = ARP()
    for i in range(255):
        p[ARP].pdst = "10.0.0." + str(i)
        x = sr1(p, verbose=False, timeout=0.1)
        if x is not None:
            ips = x[ARP].psrc
            print("ip: " + str(ips))
    print("finish")


scan_ips()
