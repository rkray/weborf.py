#!/usr/bin/env python
# author: rene@kray.info
# date: 2017-02-28
# purpose: like "python -m SimpleHTTPServer" but esear to configure

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

from socket import socket, AF_INET, SOCK_DGRAM, inet_ntoa
from fcntl import ioctl
from struct import pack

import re
import signal

from os import listdir,popen
from sys import platform

from optparse import OptionParser
#from re import match

class WebOrf:
    def __init__(self):
        # defiune defaults here
    
        self.conf=dict(
            verbose=True,
            port=8000,
            interface=WebOrf.get_interface(),
            ip=None
        )

        signal.signal(signal.SIGINT, WebOrf.cleanup)

    def run(self):
        # configure the SimpleHTTPServer
        HandlerClass = SimpleHTTPRequestHandler
        ServerClass  = HTTPServer
        Protocol     = "HTTP/1.0"

        # if the is no ip address specified, I will try to detect the right one
        if self.conf["ip"]==None:
            self.conf["ip"]=WebOrf.get_ip_address(self.conf["interface"])

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
            "-i", "--interface",
            dest="interface",default=self.conf["interface"],
            help="set the network interface", metavar="INTERVACE")
        parser.add_option(
            "-a", "--address",
            dest="ip",default=self.conf["ip"],
            help="set the network ip address", metavar="ADDRESS")
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
        ## I was not able to implement this function on Mac OS
        # s = socket(AF_INET, SOCK_DGRAM)
        # return inet_ntoa(
        #     ioctl(
        #         s.fileno(),
        #         0x8915, # SIOCGIFADDR
        #         pack('256s', ifname[:15])
        #     )[20:24]
        # )

        my_ip_address=""

        # Linux and MacOSX detection
        if platform in ["linux2","lunux3","darwin"]:
            infile=popen("/sbin/ifconfig "+ifname).read()
            inarray=infile.split("\n")
            for line in inarray:
                print(">"+line+"<")
                match=re.match(r'\s*(inet addr:|inet )(\d+\.\d+\.\d+\.\d+)',line)
                if match:
                    print("IP MATCH:")
                    return match.group(2)
            raise Exception("There is no ip for the interface {iface} configured".format(iface=ifname))

        else:
            raise Exception("unsuportet platform!")

    @classmethod
    # get default interface
    def get_interface(cls):
        if platform in ["linux2","lunux3"]:
            infile=popen("netstat -rn").read()
            inarray=infile.split("\n")
            for line in inarray:
                match=re.match(r"^0\.0\.0\.0 .* (.*)$",line)
                if match:
                    return match.group(1)
            raise Exception("No default gateway found!")

        # MacOSX detection
        elif platform in ["darwin"]:
            infile=popen("netstat -rn").read()
            inarray=infile.split("\n")
            for line in inarray:
                match=re.match(r"^default .* (.*)$",line)
                if match:
                    return match.group(1)
            raise Exception("No default gateway found!")

        else:
            raise Exception("unsuportet platform!")

    @classmethod
    def cleanup(cls, signal, frame):
        print '\nInteruppted by pressing CTRL-C:\nThanks for using me!'
        exit(0)

# END of WebOrf class

# Run this party only if this file is started as script
if __name__=="__main__":
   wo=WebOrf()
   wo.get_arguments()
   wo.run()


