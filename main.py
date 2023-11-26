import socket

"""
You must write a server that will accept the DNS request for the IP address of www.google.co.il, and return an IP address
to another server.
Find in the branch that you were asked for the domain name www.google.co.il and you answered it.
* It is recommended to use the Follow UDP/TCP Stream option on the request you found.
In the next step, connect the UDP server that will listen to the DNS requests.
In the following program, you must make the server listen on the UDP port and write your function
dns_handler. In the next chapter, you will learn in depth about the UDP protocol and understand how the code works.
"""

DNS_SERVER_IP = '0.0.0.0'
DNS_SERVER_PORT = 53
DEFAULT_BUFFER_SIZE = 1024


def dns_handler(data,addr,server_socket):
    print("DNS handler")
    print("Data: {}".format(data))
    print("Addr: {}".format(addr))
    if "www.google.co.il" in str(data):
        print("Google found")
        dns_response = "www.roblox.com A"
        print("Sending response: {}".format(dns_response))
        server_socket.sendto(dns_response.encode(),addr)



def dns_udp_server(ip,port):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('starting up on {} port {}'.format(ip, port))
    server_socket.bind((ip, port))

    while True:
        print('waiting to receive message')
        try:
            data,addr = server_socket.recvfrom(DEFAULT_BUFFER_SIZE)
            print('received {} bytes from {}'.format(len(data), addr))
            dns_handler(data,addr,server_socket)
        except Exception as ex:
            print("Client exception {}".format(ex))

def main():
    print("Starting DNS server")
    dns_udp_server(DNS_SERVER_IP,DNS_SERVER_PORT)

if __name__ == '__main__':
    main()