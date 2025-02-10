# Reliable Data Transfer (RDT) over UDP

This project implements a simple **Reliable Data Transfer (RDT) protocol** using **UDP sockets** in Python. It simulates packet corruption and loss and uses **ACK (Acknowledgment) and NAK (Negative Acknowledgment)** for reliable communication.

## Features
- Implements **Stop-and-Wait ARQ (Automatic Repeat reQuest)** protocol.
- Simulates **packet corruption** with a probability of 20%.
- Simulates **packet loss** with a probability of 20%.
- Uses **checksums** to detect corrupted packets.
- Implements **ACK (Acknowledgment) and NAK (Negative Acknowledgment)** for retransmission.

## Prerequisites
Ensure you have Python installed. This script requires Python 3.

## File Structure
```
|
|-- rdt_udp.py   # Main script containing client and server implementation
|-- README.md    # Documentation
```

## How It Works
### Packet Structure
Each packet consists of:
1. **Data (4 bytes)**
2. **Sequence Number (1 byte)**
3. **Flag (1 byte)**
   - 1: Data Packet
   - 2: ACK (Acknowledgment)
   - 3: NAK (Negative Acknowledgment)
4. **Checksum (2 bytes)**

### Components
#### 1. `calculate_checksum(data)`
Calculates the checksum by summing the data bytes and taking modulo 65536.

#### 2. `introduce_error(packet)`
Randomly corrupts a byte in the packet with a 20% probability.

#### 3. `RDT_send(sock, data, seq_num)`
- Creates a packet with sequence number and checksum.
- Sends the packet via `UDT_send()`.
- Waits for an **ACK**.
- Retransmits if timeout or **NAK** received.

#### 4. `RDT_recv(sock, packet, addr)`
- Validates the checksum.
- Sends **ACK** if the packet is correct.
- Sends **NAK** if the packet is corrupted.

#### 5. `UDT_send(sock, packet)`
- Simulates **packet loss** with 20% probability.
- Calls `introduce_error()` to simulate corruption.
- Sends the packet over UDP.

#### 6. `UDT_recv(sock)`
- Continuously receives and processes packets.

## How to Run
Open two terminals and run the following:

### Start the Server:
```sh
python rdt_udp.py server
```

### Start the Client:
```sh
python rdt_udp.py client
```

## Expected Output
- Client sends packets sequentially.
- Some packets may be dropped or corrupted.
- Server acknowledges received packets.
- Client retransmits packets on timeout or NAK.

## Example Output
```
Sending Packet [Seq: 0, Data: ABCD, Checksum: 170]
ACK received for Seq 0
Sending Packet [Seq: 1, Data: EFGH, Checksum: 198]
Timeout, retransmitting Seq 1
ACK received for Seq 1
...
```

## Enhancements
- Extend to **Go-Back-N or Selective Repeat** for efficiency.
- Add **multi-threading** to handle multiple clients.
- Implement **file transfer** over this protocol.

