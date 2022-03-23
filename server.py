import sys
import socket
import random
import struct
import time
import json
import select
import hashlib

server_addr = sys.argv[1]
server_port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind( (server_addr, server_port) )

sock.listen(10)

packer_length = struct.Struct('i')
inputs = [sock]

try:
    while True:
        readables, _, _ = select.select( inputs, [], [], 1)

        for s in readables:
            
            if s is sock:
                connection, client_info = sock.accept()
                print("Someone has connected: %s:%d" % client_info )
                inputs.append(connection)

            else:
                msg = s.recv(packer_length.size)

                if not msg: #eof karakter
                    s.close()
                    print("The client has closed the connection.")
                    inputs.remove(s)
                    continue

                length = (packer_length.unpack(msg))[0]
                msg = s.recv(length)
                parsed_msg = json.loads(msg.decode("ascii"))

                if parsed_msg["Hash"] == "md5":
                    hashh = hashlib.md5(b"")
                    for w in parsed_msg["Words"]:
                        hashh.update(w.encode())

                elif parsed_msg["Hash"] == "sha":
                    hashh = hashlib.sha256(b"")
                    for w in parsed_msg["Words"]:
                        hashh.update(w.encode())

                msg = {
                    "Hash": format(hashh.digest())
                }
                msg_json = json.dumps(msg)
                msg = packer_length.pack(len(msg_json)) + bytes(msg_json, encoding = 'ascii')
                s.sendall(msg)


except KeyboardInterrupt:
    sock.close()
    print("Server closed.")