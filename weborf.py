#!/usr/bin/env python
# author: rene@kray.info
# date: 2017-02-28
# purpose: like "python -m SimpleHTTPServer" but esear to configure

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from socket import socket, AF_INET, SOCK_DGRAM, inet_ntoa
from fcntl import ioctl
from struct import pack

from os import listdir

from optparse import OptionParser
#from re import match

class WebOrf:
    def __init__(self):
        # defiune defaults here
        self.conf=dict(
            verbose=True,
            port=8000,
            ip=WebOrf.get_ip_address('eth0') # '192.168.0.110'
        )

    def run(self):
        # configure the SimpleHTTPServer
        HandlerClass = SimpleHTTPRequestHandler
        ServerClass  = HTTPServer
        Protocol     = "HTTP/1.0"

        server_address=(
            self.conf["ip"],
            int(self.conf["port"])
        )

        HandlerClass.protocol_version = Protocol
        httpd = ServerClass(server_address, HandlerClass)

        sa = httpd.socket.getsockname()
        print "Serving HTTP on", self.conf["ip"], "port", self.conf["port"], "..."

        index=listdir(".")
        for i in index:
            print("http://%s:%s/%s" % (self.conf["ip"],self.conf["port"],i))

        # run server
        httpd.serve_forever()

    def get_arguments(self):
        parser = OptionParser()
        parser.add_option(
            "-p", "--port",
            dest="port",default=self.conf["port"],
            help="set listen port number", metavar="PORT")
        parser.add_option(
            "-q", "--quiet",
            action="store_false", dest="verbose", default=True,
            help="don't print status messages to stdout")

        (options, args) = parser.parse_args()
        # join defaults with optons from command line
        self.conf.update(vars(options))
    
    @classmethod
    # find the IP address for eth0
    def get_ip_address(cls,ifname):
        s = socket(AF_INET, SOCK_DGRAM)
        return inet_ntoa(
            ioctl(
                s.fileno(),
                0x8915, # SIOCGIFADDR
                pack('256s', ifname[:15])
            )[20:24]
        )

# END of WebOrf class

# Run this party only if this file is started as script
if __name__=="__main__":
   wo=WebOrf()
   wo.get_arguments()
   wo.run()


