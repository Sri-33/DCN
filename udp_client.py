# udp_client.py
import socket, sys, time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999
TIMEOUT_SEC = 2.0

USAGE = """\
Usage:
  python udp_client.py                 # interactive send (type messages, Ctrl+C to exit)
  python udp_client.py burst [N]       # send N numbered datagrams quickly, collect replies
"""

def interactive(sock, server):
    print("[CLIENT] Interactive mode. Type messages and press Enter. Ctrl+C to exit.")
    sock.settimeout(TIMEOUT_SEC)
    try:
        while True:
            text = input("> ")
            if not text.strip():
                continue
            # Fire-and-forget: sendto() without establishing a connection
            sock.sendto(text.encode(), server)
            # Optional: try to read a reply (echo server). If none, just continue.
            try:
                data, _ = sock.recvfrom(2048)
                print("[REPLY]", data.decode(errors="replace"))
            except socket.timeout:
                print("[NOTE] No reply (UDP gives no delivery guarantee).")
    except KeyboardInterrupt:
        print("\n[CLIENT] Bye.")

def burst(sock, server, n):
    print(f"[CLIENT] Burst mode: sending {n} datagrams rapidly…")
    sock.settimeout(0.5)
    start = time.time()

    # Send N datagrams quickly (no connection, no order guarantee)
    for i in range(n):
        sock.sendto(f"msg-{i}".encode(), server)

    # Collect replies for a short window
    received = []
    while time.time() - start < 3.0:
        try:
            data, _ = sock.recvfrom(2048)
            received.append(data.decode(errors="replace"))
        except socket.timeout:
            pass

    # Show what came back (may be fewer, may be out of order)
    print("[CLIENT] Received replies (order may differ; some may be missing):")
    for r in received:
        print("  ", r)
    print(f"[CLIENT] Stats: sent={n}, received={len(received)}")

def main():
    server = (SERVER_HOST, SERVER_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Interactive (default) or burst mode
    if len(sys.argv) == 1:
        interactive(sock, server)
    elif len(sys.argv) >= 2 and sys.argv[1] == "burst":
        n = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
        burst(sock, server, n)
    else:
        print(USAGE)

    sock.close()

if __name__ == "__main__":
    main()