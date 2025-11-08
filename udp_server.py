# udp_server.py
import socket, random, time

HOST = "0.0.0.0"
PORT = 9999

# Demo toggles to visualize UDP's "no order / no guarantee"
SIMULATE_DELAY = True          # add random delay to reorder replies
SIMULATE_DROP_PROB = 0.10      # drop ~10% of packets (no ACK back)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[UDP SERVER] Listening on {HOST}:{PORT} (ctrl+c to stop)")

    try:
        while True:
            data, addr = sock.recvfrom(2048)  # blocks until a datagram arrives
            msg = data.decode(errors="replace")
            print(f"[RECV] {addr} -> {msg!r}")

            # Optionally simulate network behavior
            if SIMULATE_DELAY:
                time.sleep(random.uniform(0.0, 0.30))
            if random.random() < SIMULATE_DROP_PROB:
                print(f"[DROP] Simulating drop for {addr}")
                continue

            # UDP echo (stateless—no connection)
            sock.sendto(f"echo:{msg}".encode(), addr)
    except KeyboardInterrupt:
        print("\n[UDP SERVER] Shutting down...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
