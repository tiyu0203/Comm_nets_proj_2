import sys
import socket
import argparse
import errno

data = []
errno.errorcode[errno.EHOSTUNREACH] = "Host Unreachable"
errno.errorcode[errno.ECONNREFUSED] = "No Response"
errno.errorcode[errno.EAGAIN] = "Closed"
errno.errorcode[0] = "Open"

def scan_port(hostname, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        sock.settimeout(.5)
        result = sock.connect_ex((hostname, port))
        # Connect the socket to a remote address; the address is usually a (host address, port #) tuple. This will return an error code instead of raising an exception. A value of 0 means success.

        try:
            server = ' '.join((socket.getservbyport(port)).split())

        except socket.error:
            server = ""

        if result == 0:
            ttl = sock.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
            tcp = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF) -1
            os = OS(ttl, tcp)
            data.append(['Status: '+ errno.errorcode[result], 'hostname: ' + hostname, 'port: ' + str(port), 'server: ' + str(server), 'TTL:' + str(ttl),'TCP: ' + str(tcp), 'OS: ' + str(os)])

        sock.close()

    except KeyboardInterrupt:
        print ("You pressed Ctrl+C. Exiting")
        sys.exit()

    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print ("Could not connect to server. Exiting")
        sys.exit()

def OS(ttl, tcp):
    if ttl == 64:
        if tcp == 5820:
            return "Linux (Kernel 2.4 and 2.6)"
        elif tcp == 5720:
            return "Google's Customized Linux"
        elif tcp == 65535:
            return "FreeBSD"
    elif ttl == 128:
        if tcp == 65535:
            return "Windows XP"
        elif tcp == 8192:
            return "Windows 7, Vista, and Server 2008"
    elif ttl == 255:
        if tcp == 4128:
            return "Cisco Router (IOS 12.4)"
    return "Undetermined OS"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hostname', metavar='hostname', type=str, help='Which hostname you want to look through')
    parser.add_argument('-p', dest='ports', type=str, help='Specify ports [-p 15:25]')
    args = vars(parser.parse_args())
    hostname = args['hostname']
    if args['ports']:
        interval = args['ports'].split(":")
        first = int(interval[0])
        last = int(interval[1])
    else:
        first = 0
        last = 1024

    for port in range(first,last +1):
        scan_port(hostname, port)

    for i in data:
        print(i)
