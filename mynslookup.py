import sys
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sr1

TYPE_A = 1
TYPE_PTR = 12
DNS_SERVER = '8.8.8.8'
MAX_LEN = 3
MIN_LEN = 2
ERROR_CODE = 3


def creates_packet(p_type, my_qname):
    """
    creates a dns query
    :param p_type: type of the query
    :param my_qname: the domain/ip
    :return:a dns query
    """
    if p_type == "A":
        num_type = TYPE_A
    else:
        num_type = TYPE_PTR
        my_qname = ".".join(my_qname.split(".")[::-1]) + ".in-addr.arpa"
    return IP(dst=DNS_SERVER)/UDP(sport=24601, dport=53)/DNS(qdcount=1, rd=1)/DNSQR(qname=my_qname, qtype=num_type)


def valid_ptr_or_A(par1, par2):
    """
    check validation of input parameters
    :param par1: type
    :param par2: ip/domain
    :return: validation of input parameters
    """
    if par1 == "-type=A":
        return True, "A"
    vpar1 = par1 == "-type=PTR"
    splited_ip = par2.split(".")
    vpar2 = len(splited_ip) == 4
    for i in splited_ip:
        vpar2 = vpar2 and i.isdigit() and (0 <= int(i) <= 255)
    return vpar1 and vpar2, "PTR"


def input_parsing():
    """
    Extracts the query type, and the ip/domain
    :return: (validation, type, ip/domain)
    """
    parms_len = len(sys.argv)
    if parms_len > MAX_LEN or parms_len < MIN_LEN:
        return False, "ERROR", "ERROR"
    if parms_len == MIN_LEN:
        return True, "A", sys.argv[1]
    else:
        valid, ptype = valid_ptr_or_A(sys.argv[1], sys.argv[2])
        return valid, ptype, sys.argv[2]


def main():
    """
    act like nslookup
    :return: the ip of the received domain or the domain of the received ip
    """
    valid, p_type, dom_or_ip = input_parsing()
    if not valid:
        print("wrong parameters")
        exit()
    dns_packet = creates_packet(p_type, dom_or_ip)
    response_packet = sr1(dns_packet, verbose=0, timeout=2)
    if response_packet == None:
        print("something got wrong")
        exit()
    if response_packet[DNS].rcode == ERROR_CODE:
        print("No such name")
        exit()
    r_num = response_packet[DNS].ancount
    for r in range(r_num):
        response = response_packet[DNS][DNSRR][r].rdata
        if isinstance(response, bytes):
            print(response.decode()[:-1])
        else:
            print(response)


if __name__ == "__main__":
    main()
