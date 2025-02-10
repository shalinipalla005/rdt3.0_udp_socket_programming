import socket
import struct
import random
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
CLIENT_PORT = 5001
TIMEOUT = 2
PACKET_SIZE = 8

def calculate_checksum(data):
    return sum(data) % 65536  

def introduce_error(packet):
    if random.random() < 0.2:  
        corrupted = bytearray(packet)
        index = random.randint(0, 3) 
        corrupted[index] ^= 0xFF  
        print(f"Corrupting packet at index {index}: {packet[index]} -> {corrupted[index]}")
        return bytes(corrupted)
    return packet


def RDT_send(sock, data, seq_num):
    checksum = calculate_checksum(data)
    packet = struct.pack('4sBBH', data, seq_num, 1, checksum)
    while True:
        UDT_send(sock, packet)
        try:
            sock.settimeout(TIMEOUT)
            ack_packet, _ = sock.recvfrom(PACKET_SIZE)
            ack_seq, flag = struct.unpack('BB', ack_packet[:2])
            if flag == 2 and ack_seq == seq_num:  
                print(f'ACK received for Seq {seq_num}')
                sock.settimeout(None)
                break
            elif flag == 3:  
                print(f'NAK received, retransmitting Seq {seq_num}, Checksum: {calculate_checksum(data)}')
        except socket.timeout:
            # print(socket.timeout)
            print(f'Timeout, retransmitting Seq {seq_num}')

def UDT_send(sock, packet):
    if random.random() < 0.2: 
        print("Dropping packet")  # Simulating packet loss
        return  
    original_packet = packet
    packet = introduce_error(packet)
    if packet != original_packet:
        print(f"Corrupted Packet: {original_packet} -> {packet}")
    sock.sendto(packet, (SERVER_IP, SERVER_PORT))


def UDT_recv(sock):
    while True:
        packet, addr = sock.recvfrom(PACKET_SIZE)
        RDT_recv(sock, packet, addr)

def RDT_recv(sock, packet, addr):
    data, seq_num, flag, checksum = struct.unpack('4sBBH', packet)
    if flag == 1 and calculate_checksum(data) == checksum:  # Valid data packet
        print(f'Received Packet [Seq: {seq_num}, Data: {data.decode()}, Checksum: {calculate_checksum(data)}] - ACK Sent')
        ack_packet = struct.pack('BB', seq_num, 2)  
    else:
        print(f"Received Data: {data}, Seq: {seq_num}, Flag: {flag}, Checksum: {checksum}, Computed Checksum: {calculate_checksum(data)}")
        print(f'Received Packet [Seq: {seq_num}] - Corrupted (Sending NAK)')
        ack_packet = struct.pack('BB', seq_num, 3)  
    sock.sendto(ack_packet, addr)

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('0.0.0.0', CLIENT_PORT))
    data_blocks = [bytes(random.choices(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4)) for _ in range(10)]
    seq_num = 0
    for data in data_blocks:
        print(f'Sending Packet [Seq: {seq_num}, Data: {data.decode()}, checksum: {calculate_checksum(data)}]')
        RDT_send(client_socket, data, seq_num)
        seq_num = 1 - seq_num 
    client_socket.close()

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print('Server running...')
    UDT_recv(server_socket)
    server_socket.close()

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'server':
        server()
    elif sys.argv[1] == 'client' :
        client()
    else:
        print('Invalid argument')
        pass
        
