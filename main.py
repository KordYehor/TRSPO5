import socket
import struct
import threading
import time

def server():
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print('Server start working...')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                # Отримуємо довжину повідомлення
                data_length = conn.recv(4)
                if not data_length:
                    break
                length = struct.unpack('!I', data_length)[0]

                # Отримуємо повідомлення
                data = conn.recv(length)
                print(f"Received message from CLIENT: {data.decode('utf-8')}")

                # Відсилаємо відповідь
                if (data.decode('utf-8') == f"Ladno, davay, dobre pogovorulu, poka"):
                    response = "Answer for CLIENT: Tak tak, duje dobre pobalakaly, garnogo dnia, poka"
                    conn.sendall(struct.pack('!I', len(response)) + response.encode('utf-8'))
                else:
                    response = "Answer for CLIENT: Ta normalno vse. A tu scho tam?"
                    conn.sendall(struct.pack('!I', len(response)) + response.encode('utf-8'))




    print("Server has closed the connection.")



def client():
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        message = f"Scho tu tam?"
        print(f"Sending to SERVER: {message}")
        s.sendall(struct.pack('!I', len(message)) + message.encode('utf-8'))
        data_length = s.recv(4)
        length = struct.unpack('!I', data_length)[0]
        data = s.recv(length)
        print(f"Received message from SERVER: {data.decode('utf-8')}")

        for i in range(98):
            message = f"Ta normalno vse. A tu scho tam?"
            print(f"Sending to SERVER: {message}")

            s.sendall(struct.pack('!I', len(message)) + message.encode('utf-8'))

            data_length = s.recv(4)
            length = struct.unpack('!I', data_length)[0]
            data = s.recv(length)
            print(f"Received message from SERVER: {data.decode('utf-8')}")

        message = f"Ladno, davay, dobre pogovorulu, poka"
        print(f"Sending to SERVER: {message}")
        s.sendall(struct.pack('!I', len(message)) + message.encode('utf-8'))
        data_length = s.recv(4)
        length = struct.unpack('!I', data_length)[0]
        data = s.recv(length)
        print(f"Received message from SERVER: {data.decode('utf-8')}")

    print("Client has finished sending messages.")


if __name__ == '__main__':
    server_process = threading.Thread(target=server)
    client_process = threading.Thread(target=client)

    server_process.start()
    time.sleep(2)
    client_process.start()

    client_process.join()
    server_process.join()
