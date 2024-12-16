import socket
import threading
import time
import random
from collections import deque

N = 8
WINDOW_SIZE = 7
T1, T2 = 1, 3
T3, T4 = 0.5, 1.5
DROP_PROBABILITY = 0.1
TOTAL_PACKETS = 10000
outgoing_queue = deque()
incoming_queue = deque()

ENTITY_IP = 'localhost'
PEER_IP = 'localhost'
ENTITY_PORT = 8080
PEER_PORT = 9090  

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

retransmissions = 0
total_delay = 0
sent_frames = 0

def packet_generator(entity_name):
    global TOTAL_PACKETS
    seq_num = 0
    for packet_num in range(1, TOTAL_PACKETS + 1):
        time_gap = random.uniform(T1, T2)
        time.sleep(time_gap)
        packet = f"{seq_num} {packet_num}"
        print(f"[{entity_name}] Generated Packet: {packet_num} with Seq {seq_num}")
        outgoing_queue.append(packet)
        seq_num = (seq_num + 1) % N

def send_frame(seq_num, packet_num, entity_name):
    global retransmissions, total_delay, sent_frames
    frame = f"DATA {seq_num} {packet_num}".encode()

    if random.random() < DROP_PROBABILITY:
        print(f"[{entity_name}] Dropped frame with Seq {seq_num}")
        return

    start_time = time.time()
    send_socket.sendto(frame, (PEER_IP, PEER_PORT))
    delay = time.time() - start_time
    total_delay += delay
    sent_frames += 1
    print(f"[{entity_name}] Sent packet: {packet_num} with Seq {seq_num}")

def sender_dl_entity(entity_name):
    global retransmissions
    base = 0
    while True:
        next_seq_num = -1
        if outgoing_queue:
            next_seq_num, packet_num = outgoing_queue.popleft().split()
            next_seq_num = int(next_seq_num)
            if next_seq_num < base + WINDOW_SIZE:
                send_frame(next_seq_num, packet_num, entity_name)

            delay = random.uniform(T3, T4)
            time.sleep(delay)

        try:
            recv_socket.settimeout(1)
            data, _ = recv_socket.recvfrom(1024)
            data = data.decode().split()
            frame_type = data[0]

            if frame_type == 'ACK':
                ack_no = int(data[1])
                if (base <= ack_no < base + WINDOW_SIZE) or (ack_no < base and ack_no + N >= base):
                    base = (ack_no + 1) % N
                    print(f"[{entity_name}] ACK received for Seq {ack_no}, base updated to {base}")
        
        except socket.timeout:
            pass
        
        if base != next_seq_num and next_seq_num != -1:
            print(f"[{entity_name}] Timeout! Retransmitting frames.")
            for i in range(base, next_seq_num):
                retransmissions += 1
                send_frame(i % N, packet_num, entity_name)

def send_ack(ack_no, entity_name):
    frame = f"ACK {ack_no}".encode()

    if random.random() < DROP_PROBABILITY:
        print(f"[{entity_name}] Dropped ACK for Seq {ack_no}")
        return

    send_socket.sendto(frame, (PEER_IP, PEER_PORT))
    print(f"[{entity_name}] Sent ACK for Seq {ack_no}")

def receiver_dl_entity(entity_name):
    expected_seq_num = 0

    while True:
        delay = random.uniform(T3, T4)
        time.sleep(delay)
        try:
            recv_socket.settimeout(1)
            data, _ = recv_socket.recvfrom(1024)
            data = data.decode().split()
            frame_type = data[0]

            if frame_type == 'DATA':
                seq_num = data[1]
                packet_num = data[2]
                seq_num = int(seq_num)
                if seq_num == expected_seq_num:
                    print(f"[{entity_name}] Received: {packet_num} with Seq {seq_num}")
                    incoming_queue.append(packet_num)
                    send_ack(seq_num, entity_name)
                    expected_seq_num = (expected_seq_num + 1) % N
                else:
                    print(f"[{entity_name}] Out-of-order frame Seq {seq_num}, expected Seq {expected_seq_num}")
                    send_ack((expected_seq_num - 1) % N, entity_name)           

        except socket.timeout:
            pass


def start_two_way_protocol(entity_name, entity_port, peer_port):
    global ENTITY_PORT, PEER_PORT, TOTAL_PACKETS
    ENTITY_PORT = entity_port
    PEER_PORT = peer_port

    recv_socket.bind((ENTITY_IP, ENTITY_PORT))

    threading.Thread(target=packet_generator, args=(entity_name,), daemon=True).start()
    threading.Thread(target=sender_dl_entity, args=(entity_name,), daemon=True).start()
    threading.Thread(target=receiver_dl_entity, args=(entity_name,), daemon=True).start()

    time.sleep(TOTAL_PACKETS+10)

    print(f"\n[INFO] Time limit reached. Ending protocol.")
    print(f"Total frames sent: {sent_frames}")
    print(f"Total retransmissions: {retransmissions}")
    print(f"Average delay per frame: {total_delay / sent_frames if sent_frames > 0 else 0:.3f} seconds")
    send_socket.close()
    recv_socket.close()

if __name__ == "__main__":
    entity_name = input("Enter entity name (Client/Server): ").strip()

    if entity_name.lower() == 'client':
        start_two_way_protocol(entity_name, 8080, 9090)
    else:
        start_two_way_protocol(entity_name, 9090, 8080)
