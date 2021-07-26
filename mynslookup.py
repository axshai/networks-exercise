import sys
#from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sr1


def main():
    """
    act like nslookup
    :return: the ip of the recived domain
    """
    domain=sys.argv[1]
    dns_packet =IP(dst='8.8.8.8')/UDP(sport=24601,dport=53)/DNS(qdcount=1 ,rd=1 )/DNSQR(qname=domain)
    response_packet = sr1(dns_packet)
    r_num=response_packet[DNS].ancount
    for r in range(r_num):
        print(response_packet[DNS][DNSRR][r].rdata)






if __name__ == "__main__":
    main()