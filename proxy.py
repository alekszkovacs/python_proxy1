import sys
import socket
import struct
import select
import json

proxy_addr = sys.argv[1]
proxy_port = int(sys.argv[2])
server_addr = sys.argv[3]
server_port = int(sys.argv[4])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind( (proxy_addr, proxy_port) )

sock.listen(10)

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.connect( (server_addr, server_port))

packer_length = struct.Struct('i')
inputs = [ sock ]

try:
    while True:
        readables, _, _ = select.select( inputs, [], [] )

        for s in readables:

            if s is sock:
                connection, client_info = sock.accept()
                print("Someone has connected: %s:%d" % client_info )
                inputs.append(connection)

            else:
                og_len = s.recv(packer_length.size)

                if not og_len:
                    s.close()
                    print("The client has closed the connection.")
                    inputs.remove(s)
                    continue

                length = (packer_length.unpack(og_len))[0]

                og_msg = s.recv(length)
                parsed_msg = json.loads(og_msg.decode("ascii"))

                wordslen = 0
                for w in parsed_msg["Words"]:
                    wordslen += len(w)

                if wordslen > 20:
                    msg = {
                        "Hash": "TILOS!!!!"
                    }
                    msg_json = json.dumps(msg)
                    msg = packer_length.pack(len(msg_json)) + bytes(msg_json, encoding = 'ascii')
                    s.sendall(msg)

                else:
                    msg = og_len + og_msg
                    server_sock.sendall(msg)
                
                    og_len = server_sock.recv(packer_length.size)
                    length = (packer_length.unpack(og_len))[0]
                    og_msg = server_sock.recv(length)

                    msg = og_len + og_msg
                    s.sendall(msg)
			
finally:
	sock.close()
