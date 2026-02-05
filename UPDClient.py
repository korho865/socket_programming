import socket as sk

try:
    s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM, sk.IPPROTO_UDP)
except sk.error: 
    print("Cannot open socket, quit")
    exit()

while True:
    try:
        m = input("Message to server: ")
        s.sendto(bytearray(m, encoding="ascii"), ("192.168.73.126", 44444))
        try:
            m, addr = s.recvfrom(1000)
            print(m.decode("ascii\n"))
        except sk.error: 
            print("something is wrong")
            break 
    except KeyboardInterrupt: break 

s.close()