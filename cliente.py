import socket
import ssl

'''
Variables para la coneccion
'''
HOST = '127.0.0.1'
PORT = 50001

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations('server_new.crt') # certificado del servidor

socket_cliente = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=HOST)
socket_cliente.connect((HOST, PORT))

'''
Recibimos Bienvenida
'''

bienvenida = socket_cliente.recv(1024).decode()
print(f"Servidor dice: {bienvenida}")

while True:
    mensaje = input("Ingrese su comando: ")
    socket_cliente.send(mensaje.encode())

    if mensaje == 'close':
        break

    respuesta = socket_cliente.recv(1024).decode()
    print(f"Servidor dice: {respuesta}")

socket_cliente.close()