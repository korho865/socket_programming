#DRP Client with asynchrounouns communivation
import socket as sc
import threading

def recv(s):    #Define function to threading
    while True:
        try:
            msg, addr = s.recvfrom(1024)
            print("\x1b7\x1b[%d;%dH\x1b[31m%s\x1b[0m\x1b8" % (10,40,msg))
        except OSError:
            break

try:
    s = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
except:
    print("Cannot create socket")
    exit()

t = threading.Thread(target=recv, args=[s]).start()
while True:
    try:
        msg = input("To server: ")
        s.sendto(bytearray(msg, encoding="ascii"), ("192.168.73.235",44444))
        if "BYE" in msg: break
    except KeyboardInterrupt: break

s.close()