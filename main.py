import socket
import netifaces

DNS_SERVER_IP = '0.0.0.0'
DNS_SERVER_PORT = 53
DEFAULT_BUFFER_SIZE = 1024

WEBSITES = {
    'www.google.co.il': '80.179.226.44',
    'nana10.co.il': '172.217.22.67',
    'www.example.com': '127.0.0.1'}

DEFAULT_GATEWAY = netifaces.gateways()['default'][netifaces.AF_INET][0]

READ_DATA_LENGTH = b'\x00\x04'
TIME_TO_LIVE = b'\x00\x00\x03\x3C'
DNS_NAME = b'\xC0\x0C'

FLAGS = b'\x81\x80'
QUESTION_COUNT = b'\x00\x01'
AUTHORITY_COUNT = b'\x00\x00'
ADDITIONAL_COUNT = b'\x00\x00'
QUERY_TYPE = b'\x00\x01'
QUERY_CLASS = b'\x00\x01'


def parse_dns_query(data):
    print("Parse DNS query")
    domain_name = ''
    index = 12
    length = data[index]
    while length != 0:
        domain_name += data[index + 1:index + length + 1].decode('utf-8') + '.'
        index += length + 1
        length = data[index]
    return domain_name[:-1]


def create_dns_response(transaction_id, ip):
    print("Create DNS response")
    response = (transaction_id
                + FLAGS
                + QUESTION_COUNT
                + AUTHORITY_COUNT
                + ADDITIONAL_COUNT
                + DNS_NAME
                + QUERY_TYPE
                + QUERY_CLASS
                + TIME_TO_LIVE
                + READ_DATA_LENGTH
                + ip)
    return response


def dns_handler(data, addr, server_socket):
    print("DNS handler")
    print("Data: {}".format(data))
    print("Addr: {}".format(addr))

    domain_name = parse_dns_query(data)
    print("Domain name: {}".format(domain_name))

    if domain_name not in WEBSITES:
        isp_tuple = (DEFAULT_GATEWAY, DNS_SERVER_PORT)
        server_socket.sendto(data, isp_tuple)
        data, new_addr = server_socket.recvfrom(DEFAULT_BUFFER_SIZE)
        print("Data from isp: {}".format(data))
        server_socket.sendto(data, addr)
        return

    ip = WEBSITES[domain_name]
    print("IP: {}".format(ip))
    response = create_dns_response(data[:2], socket.inet_aton(ip))
    print("Response: {}".format(response))
    server_socket.sendto(response, addr)


def dns_udp_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Starting up on {} port {}'.format(ip, port))
    server_socket.bind((ip, port))

    while True:
        print('Waiting to receive message')
        try:
            data, addr = server_socket.recvfrom(DEFAULT_BUFFER_SIZE)
            print('Received {} bytes from {}'.format(len(data), addr))
            dns_handler(data, addr, server_socket)
        except Exception as ex:
            print("Client exception {}".format(ex))


def main():
    print("Starting DNS server")
    dns_udp_server(DNS_SERVER_IP, DNS_SERVER_PORT)


if __name__ == '__main__':
    main()
