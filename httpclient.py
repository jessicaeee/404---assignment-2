#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        # search for equals in data
        equal = re.match(r'^\S+\s+(\d+)', data)
        # if no equal is found
        if not equal:
            return None
        else: 
            # if equal is found
            if equal:
                return int(equal.group(1))
        

    def get_headers(self,data):
        # dictionary to keep track of headers
        dictionary_header = {}
        # create separators and split the data into parts
        sep = '\r\n\r\n'
        sep2 = '\r\n'
        parts = data.split(sep, 1)[0]
        # split the parts into lines
        lines = parts.split(sep2)[1:]
        # check every line and split them into parts
        i = 0
        while i < lines:
            x, y = lines.split(':', 1)
            dictionary_header[x] = y
            i + 1
        return dictionary_header


    def get_body(self, data):
        # separator between header and body and split into parts
        sep = '\r\n\r\n'
        index = data.rfind(sep)
        part = data.split(sep, 1)
        # if separator index is found
        if index == -1:
            return ''
        else: 
            # if list has more than one element
            if len(part) > 1:
                body = part[1]
                return body

    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        # get info from url
        url_analysis = urllib.parse.urlparse(url)
        host = url_analysis.hostname

        # get path from url
        if url_analysis.path:
            path = url_analysis.path
        else: 
            # if there is no path is available from url
            if not url_analysis.path:
                path = '/'

        # get query from url
        if url_analysis.query:
            query = url_analysis.query
        else: 
            # if there is no query is available from url
            if not url_analysis.query:
                query = ''

        # get port number from url
        if url_analysis.port:
            port = url_analysis.port
        else: 
            # if there is no port number is available from url
            if not url_analysis.port:
                port = 80

        # form the questions to send
        question = f"GET {path}?{query} HTTP/1.1\r\n"
        question += f"Host: {host}\r\n\r\n"

        # connect and send question to server
        self.connect(host, port)
        self.sendall(question)

        # get answer from server
        answer = self.recvall(self.socket)
        code, body = (self.get_code(answer), self.get_body(answer))

        # close connection to server
        self.close()
        return HTTPResponse(code, body)
        

    def POST(self, url, args=None):
        # get info from url
        url_analysis = urllib.parse.urlparse(url)
        host = url_analysis.hostname

        # get path from url
        if url_analysis.path:
            path = url_analysis.path
        else: 
            # if there is no path is available from url
            if not url_analysis.path:
                path = '/'
        
        # get query from url
        if url_analysis.query:
            query = url_analysis.query
        else: 
            # if there is no query is available from url
            if not url_analysis.query:
                query = ''
        # get port number from url
        if url_analysis.port:
            port = url_analysis.port
        else: 
            # if there is no port number is available from url
            if not url_analysis.port:
                port = 80
    
        # if there is no argument
        if not args:
            posted = ''
        else:
            # get argument
            if args:
                posted = urllib.parse.urlencode(args)
        # format POST
        posting = "POST {}{} HTTP/1.1\r\n".format(path, query)
        question = posting
        # format host
        hosting = "Host: {}\r\n".format(host)
        # create question to send
        question = question + hosting
        # get content
        content = "Content-Type: application/x-www-form-urlencoded\r\n"
        question = question + content
        # get the length of the content
        content_length = "Content-Length: {}\r\n\r\n".format(len(posted))
        question = question + content_length
        # form completed question to send
        question = question + posted
        
        # connect to server and send question
        self.connect(host, port)
        self.sendall(question)

        # get answer from server
        answer = self.recvall(self.socket)
        code, body = (self.get_code(answer), self.get_body(answer))

        # close connection to server
        self.close()
        return HTTPResponse(code, body)
        

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))

'''
Sources Consulted:
            https://note.nkmk.me/en/python-split-rsplit-splitlines-re/
            https://stackoverflow.com/questions/6479423/does-d-in-regex-mean-a-digit
            https://stackoverflow.com/questions/40557606/how-to-url-encode-in-python-3
            https://www.youtube.com/watch?v=T19SWjvHrGk
'''
