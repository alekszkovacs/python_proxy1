import sys
import socket
import random
import struct
import time
import json
import zlib

server_addr = sys.argv[1]
server_port = int(sys.argv[2])
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.connect( (server_addr, server_port) )

file_name = sys.argv[3]

packer_length = struct.Struct('i')

with open(file_name, "rb") as file:
    data = json.load(file)

data["Hash"] = "sha"

msg_json = json.dumps(data)
msg = packer_length.pack(len(msg_json)) + bytes(msg_json, encoding = 'ascii')

server_sock.sendall(msg)

msg = server_sock.recv(packer_length.size)
length = (packer_length.unpack(msg))[0]
msg = server_sock.recv(length)
parsed_msg = json.loads(msg.decode("ascii"))

print(parsed_msg["Hash"])

# The file will be closed because of the "with", so we don't have to close it here.
server_sock.close()