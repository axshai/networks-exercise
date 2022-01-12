from scapy.all import *
from scapy.layers.inet import TCP
from scapy.layers.inet import IP

SNIFF_FILE_PATH = r"C:\Users\User\Desktop\forpy\SynFloodSample.pcap"
OUTPUT_FILE__PATH = r"C:\Users\User\Desktop\forpy\suspectips.txt"
SYN_ACK = 0X012
IP_DICT = {}
IP_DICT2 = {}
SUSPECT_DICT = {}
DELTA = 0.0001
pcapFile = rdpcap(SNIFF_FILE_PATH)


def main():
    with open(OUTPUT_FILE__PATH, 'w') as output_file:
        for pack in pcapFile:  # for each packet in the file
            if TCP in pack:
                if pack[TCP].flags == SYN_ACK:
                    if pack[IP].dst in IP_DICT:
                        IP_DICT[pack[IP].dst] += [pack[TCP].seq]
                    else:
                        IP_DICT[pack[IP].dst] = [pack[IP].seq]
                if pack[IP].src in IP_DICT and pack[TCP].flags == "A" and pack[TCP].ack - 1 in IP_DICT[pack[IP].src]:
                    IP_DICT[pack[TCP].src].remove(pack[TCP].ack - 1)

        for pack in pcapFile:  # for each packet in the file
            if TCP in pack:
                if pack[TCP].flags == "S":
                    if pack[IP].src in IP_DICT2:
                        flag = True
                        for t in IP_DICT2[pack[IP].src]:
                            if abs(pack.time - t) < DELTA:
                                SUSPECT_DICT[pack[IP].src] = 1
                                flag = False
                        if flag:
                            IP_DICT2[pack[IP].src] += [pack.time]
                    else:
                        IP_DICT2[pack[IP].src] = [pack.time]

        for i in IP_DICT.keys():
            if IP_DICT[i] != [] and i not in SUSPECT_DICT:
                output_file.write(str(i) +"\n")
        for i in SUSPECT_DICT:
            output_file.write(str(i) + "\n")
            print(IP_DICT2[i])


if __name__ == "__main__":
    main()
