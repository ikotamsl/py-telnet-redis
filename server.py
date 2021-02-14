import socket
import redis
import sys

from _thread import *
import threading

print_lock = threading.Lock()
r = redis.StrictRedis(
    host='localhost',
    port=6379
)


def threaded(c):
    while True:

        data = c.recv(1024)

        inner_data = data.decode().split()

        if not data:
            print('Всего доброго')

            print_lock.release()
            break

        elif inner_data[0] == 'set':
            key = inner_data[1]
            val = inner_data[2]
            r.set(key, val)
            data = key.encode('utf-8') + b' has a value: ' + r.get(key)

        elif inner_data[0] == 'del':
            key = inner_data[1]
            r.delete(inner_data[1])
            data = key.encode('utf-8') + b' was deleted'

        elif inner_data[0] == 'keyall':
            for i in r.keys('*'):
                data += str(i) + '\n'

        elif inner_data[0] == 'kill':
            print('What have you done...')
            print_lock.release()
            break

        else:
            data = b'Succ'

        # send back reversed string to client
        c.send(data)

        # connection closed
    c.close()
    sys.exit()


def Main():
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 9090
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))


if __name__ == '__main__':
    Main()
