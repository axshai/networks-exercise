from scapy.all import *
from scapy.layers.inet import TCP
from scapy.layers.inet import IP


SUSPECT_NUM = 7  # 7 or more syn packets is suspicious
SNIFF_FILE_PATH = r"C:\Users\User\Desktop\forpy\SynFloodSample.pcap"
OUTPUT_FILE__PATH = r"C:\Users\User\Desktop\forpy\suspectips.txt"

ipdict = {}
pcapFile = rdpcap(SNIFF_FILE_PATH)


def main():
    with open(OUTPUT_FILE__PATH, 'w') as output_file:
        for pack in pcapFile:  # for each packet in the file
            if TCP in pack:
                if pack[TCP].flags == 'S':  # if it is a tcp syn packet
                    for pack2 in pcapFile:  # if the sender responded to the "syn ack" packet - he isn't suspect
                        if TCP in pack2 and pack2[IP].src == pack[IP].src \
                                and pack2[TCP].flags == 'A' and pack2[TCP].seq - 1 == pack[TCP].seq:
                            continue
                    if pack[IP].src in ipdict:
                        ipdict[pack[IP].src] += 1  # Increase in the dictionary the number of
                        # times we received a syn packet from this ip address
                    else:
                        ipdict[pack[IP].src] = 1  # Enter the ip address in the dictionary if it is not there
                    if ipdict[pack[IP].src] == SUSPECT_NUM:  # If we have reached the suspicious number - write the ip
                        output_file.write(str(pack[IP].src) + '\n')


if __name__ == "__main__":
    main()
