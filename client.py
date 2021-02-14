import socket
import redis

r = redis.StrictRedis(
    host='localhost',
    port=6379,
)

help_text = 'Для того, чтобы создать пару ключ-значение, введите set [key] [val]\n' \
            'Для того, чтобы удалить ключ, введите del [key]\n' \
            'Для того, чтобы увидеть список всех ключей, введите keyall\n'


def Main():
    host = 'localhost'
    port = 9090

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        s.send(str(input(help_text)).encode('utf-8'))

        data = s.recv(1024)

        print('Received from the server :', str(data.decode('utf-8')))

        ans = input('Хотите выйти?')

        if ans == 'y':
            break
        else:
            continue

    s.close()


if __name__ == '__main__':
    Main()
