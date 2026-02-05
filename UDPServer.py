#UDP sequential server program
import socket

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Cannot create socket")
    exit()
s.bind(('', 44444))
print("UDP Server is ready")
while True:
    try:
        m, caddr = s.recvfrom(1000)
        print(f"[{caddr}]: {m.decode("ascii")}")
        m = input("Msg back to: ")
        s.sendto(bytearray(m, encoding="ascii"), caddr)
    except socket.error:
        print("recvfrom error")