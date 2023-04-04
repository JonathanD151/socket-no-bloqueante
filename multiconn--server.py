#ANDRADE JIMENEZ JONATHAN DEMIAN

#!/usr/bin/env python3
import sys
import socket
import selectors
import types
import logging
sel = selectors.DefaultSelector()

def accept(sock_a, mask):
    sock_conn, addr = sock_a.accept()  # Listo
    print('aceptado', sock_conn, ' de', addr)
    sock_conn.setblocking(False)
    sel.register(sock_conn, selectors.EVENT_READ | selectors.EVENT_WRITE, read_write)

def read_write(sock_c, mask):
    if mask & selectors.EVENT_READ:
        try:
            data = sock_c.recv(1024)  # listo
            if data:
                print('recibido', repr(data), 'a', sock_c)
                print('respondiendo', repr(data), 'a', sock_c)
                sock_c.sendall(data)  # esperando que no se bloquee
            else:
                print('cerrando', sock_c)
                sel.unregister(sock_c)
                sock_c.close()
        except BlockingIOError:
            pass
    if mask & selectors.EVENT_WRITE:
        print ("enviando datos")

        # Enviando informacion
        message = b"Hola cliente"
        try:
            sock_c.sendall(message)
        except BlockingIOError:
            pass

with socket.socket() as sock_accept:
    sock_accept.bind(('localhost', 12345))
    sock_accept.listen(100)
    sock_accept.setblocking(False)
    sel.register(sock_accept, selectors.EVENT_READ, accept)

    while True:
        print("Esperando evento...")
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)