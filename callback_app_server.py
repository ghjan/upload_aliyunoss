import socket
import httplib
import base64
import md5
import urllib2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from M2Crypto import RSA
from M2Crypto import BIO
import json
from settings import *
import os
import logging

logging.basicConfig(filename=os.path.join(os.getcwd(), 'callback_server_log.txt'), level=logging.DEBUG)

LIST_VALID_CALLBACK_URL = [_.get('callback_url') for _ in oss_data.values() if
                           _.get('callback_url')]


def get_local_ip():
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return ""


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # get public key
        pub_key_url = ''
        try:
            pub_key_url_base64 = self.headers['x-oss-pub-key-url']
            pub_key_url = pub_key_url_base64.decode('base64')
            url_reader = urllib2.urlopen(pub_key_url)
            pub_key = url_reader.read()
        except Exception as e:
            logging.error('exception catched, pub_key_url : ' + pub_key_url)
            logging.error('Get pub key failed!')
            logging.error(e)
            self.send_response(400)
            self.end_headers()
            return

        # get authorization
        authorization_base64 = self.headers['authorization']
        authorization = authorization_base64.decode('base64')
        # get callback body
        content_length = self.headers['content-length']
        callback_body = self.rfile.read(int(content_length))

        # compose authorization string
        auth_str = ''
        pos = self.path.find('?')
        if -1 == pos:
            auth_str = self.path + '\n' + callback_body
        else:
            auth_str = urllib2.unquote(self.path[0:pos]) + self.path[pos:] + '\n' + callback_body

        # verify authorization
        auth_md5 = md5.new(auth_str).digest()
        bio = BIO.MemoryBuffer(pub_key)
        rsa_pub = RSA.load_pub_key_bio(bio)
        try:
            result = rsa_pub.verify(auth_md5, authorization, 'md5')
        except Exception as e:
            logging.error('exception catched when rsa_pub.verify')
            logging.error(e)
            result = False

        if not result:
            logging.error('Authorization verify failed!')
            logging.error('Public key : %s' % (pub_key))
            logging.error('Auth string : %s' % (auth_str))
            self.send_response(400)
            self.end_headers()
            return

        # do something accoding to callback_body
        if callback_body:
            if type(callback_body) == str:
                list_data = callback_body.split('&')
                dict_data = {}
                for _ in list_data:
                    kv = _.split('=')
                    dict_data[kv[0]] = kv[1]
            else:
                dict_callback_body = json.loads(callback_body.decode('base64'))
                callbackUrl = dict_callback_body.get('callbackUrl')
                valid = callbackUrl and callbackUrl in LIST_VALID_CALLBACK_URL
                callbackBody = dict_callback_body.get('callbackBody')
                list_data = callbackBody.split('&')
                dict_data = {}
                for _ in list_data:
                    kv = _.split('=')
                    dict_data[kv[0]] = kv[1]
            logging.debug("dict_data:{}".format(dict_data))
        # response to OSS
        resp_body = '{"Status":"OK"}'
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(resp_body)))
        self.end_headers()
        self.wfile.write(resp_body)


class MyHTTPServer(HTTPServer):
    def __init__(self, host, port):
        HTTPServer.__init__(self, (host, port), MyHTTPRequestHandler)


if '__main__' == __name__:
    # server_ip = get_local_ip()
    server_ip = '0.0.0.0'
    server_port = 23450

    server = MyHTTPServer(server_ip, server_port)
    logging.debug('start to run callback server')
    server.serve_forever()
