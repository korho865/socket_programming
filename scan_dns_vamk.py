import socket as soc
import struct

s = input("Enter the subnet (x.y.z.t): ").split("/")
subnetID = soc.inet_aton(s[0])
mask_len =32 - int(s[1])
subnetSize = 2**mask_len
first = int.from_bytes(subnetID)

outfile = open("active_vamk_addresses.txt", "w")

for i in range(1, subnetSize):
    try:
        addr = struct.pack("!I", first + i)
        ip = soc.inet_ntoa(addr)
        result = soc.gethostbyaddr(ip)
        print(soc.gethostbyaddr(soc.inet_ntoa(addr)))

        line = f"{ip} -> {result}\n"
        print(line.strip())
        outfile.write(line)

    except soc.error:
        line = f"{soc.inet_ntoa(struct.pack('!I', first + i))} -> Address is not active\n"
        print(line.strip())
        outfile.write(line)

outfile.close()