import socket


def main() -> None:
    student_id = "e22xxxx"  # Replace xxxx with your actual ID digits.
    target = ("8.8.8.8", 80)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(student_id.encode("utf-8"), target)
        print("Packet successfully transmitted to 8.8.8.8:80")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
