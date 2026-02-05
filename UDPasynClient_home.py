# UDPasynClient_home.py
# Home-safe version for the ICMP raw socket assignment:
# - Sends exactly 3 echo requests (seq 1,2,3)
# - Identifier = 0x(last4 of STUDENT_ID interpreted as hex)
# - Payload = 8 ASCII bytes of STUDENT_ID
# - Default target = 127.0.0.1 (loopback, safest)

import socket as sc
import time

# === CHANGE THIS ===
STUDENT_ID = "e2202928"  # must be EXACTLY 8 characters (8 bytes ASCII)

def checksum(packet_bytes: bytes) -> int:
    data = bytearray(packet_bytes)  # copy so we don't mutate caller
    if len(data) % 2 == 1:
        data.append(0)

    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i + 1]
        # fold carries as we go
        s = (s & 0xFFFF) + (s >> 16)

    # final fold (just in case)
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)

    return (~s) & 0xFFFF

def build_packet(ident: int, seq: int, payload: bytes) -> bytearray:
    # ICMP Echo Request header is 8 bytes:
    # type(8), code(0), checksum(2), identifier(2), sequence(2)
    pkt = bytearray(8 + len(payload))
    pkt[0] = 8   # type echo request
    pkt[1] = 0   # code

    # checksum initially 0
    pkt[2] = 0
    pkt[3] = 0

    # identifier (big-endian)
    pkt[4] = (ident >> 8) & 0xFF
    pkt[5] = ident & 0xFF

    # sequence (big-endian)
    pkt[6] = (seq >> 8) & 0xFF
    pkt[7] = seq & 0xFF

    # payload
    pkt[8:] = payload

    # compute checksum over entire ICMP message
    csum = checksum(pkt)
    pkt[2] = (csum >> 8) & 0xFF
    pkt[3] = csum & 0xFF

    return pkt

def main():
    if len(STUDENT_ID) != 8:
        raise ValueError("STUDENT_ID must be exactly 8 characters (8 bytes).")

    # Identifier = hex value of last 4 characters
    last4 = STUDENT_ID[-4:]
    try:
        ident = int(last4, 16)
    except ValueError:
        raise ValueError(
            f"Last 4 chars of STUDENT_ID must be hex digits (0-9, a-f). Got: {last4}"
        )

    # safest target for home VM
    target_ip = input("Target IP (Enter for 127.0.0.1): ").strip() or "127.0.0.1"
    payload = STUDENT_ID.encode("ascii")

    s = sc.socket(sc.AF_INET, sc.SOCK_RAW, sc.IPPROTO_ICMP)

    for seq in (1, 2, 3):
        pkt = build_packet(ident, seq, payload)
        print(f"Sent -> {target_ip}  id=0x{ident:04x}  seq=0x{seq:04x}  data={STUDENT_ID}")
        s.sendto(pkt, (target_ip, 0))
        time.sleep(1)

    s.close()
    print("Done. In Wireshark: capture 'lo' (if 127.0.0.1) and filter 'icmp'.")

if __name__ == "__main__":
    main()
