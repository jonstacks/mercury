TCP_FLAGS = {
    'FIN': 0x01,
    'SYN': 0x02,
    'RST': 0x04,
    'PSH': 0x08,
    'ACK': 0x10,
    'URG': 0x20,
    'ECE': 0x40,
    'CWR': 0x80,
}

def is_tcp_handshake_start(x):
    return True if x == TCP_FLAGS['SYN'] else False

def is_tcp_handshake_reply(x):
    return True if x == (TCP_FLAGS['SYN'] | TCP_FLAGS['ACK']) else False
