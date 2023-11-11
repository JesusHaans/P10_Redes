import socket
import threading
import ssl

'''
Variables para la coneccion y los comandos
'''
HOST = '127.0.0.1'
PORT = 50001
CLIENTES_CONECTADOS = 0
LIMITE_CLIENTES = 5

creadores= "Creado por: \n Jesus Haans Lopez Hernandez - 311245488 \n Axel Casas Espinosa - 316218849"

bienvenida = "Bienvenido al servidor!!!"

'''
Funciones del Servidor
'''

def end_conection(socket_cliente, dirreccion_cliente):
    print(f'Conexion cerrada con: ', dirreccion_cliente)
    socket_cliente.close()

def show_creators():
    return creadores

def show_help():
    return "Comandos disponibles: \n 1. Creators \n 2. Help \n 3. Close \n 4. Meme \n 5. Cancion \n"



'''
Funcion principal del servidor
'''

def client_thread(socket_cliente, dirreccion_cliente):
    print(f'Conexion establecida con: ', dirreccion_cliente)
    ssl_version = socket_cliente.version()
    print(f"Versión del protocolo SSL/TLS: {ssl_version}")

    #enviar bien venida al cliente
    socket_cliente.send(bienvenida.encode())

    while True:
        try:
            #recibir mensaje del cliente
            data = socket_cliente.recv(1024)
            mensaje = data.decode()


            #si el cliente envia un mensaje vacio cerrar la conexion
            if not data:
                break
            #si el cliente envia el comando creators
            elif mensaje == 'creators':
                socket_cliente.send(show_creators().encode())

            #si el cliente envia el comando help
            elif mensaje == 'help':
                socket_cliente.send(show_help().encode())

            #si el cliente envia el comando close
            elif mensaje == 'close':
                end_conection(socket_cliente, dirreccion_cliente)
                break

            #si el cliente envia el comando meme
            elif mensaje == 'meme':
                socket_cliente.send("https://www.youtube.com/watch?v=CGRCnr4LAPQ".encode())

            #si el cliente envia el comando cancion
            elif mensaje == 'cancion':
                socket_cliente.send("https://www.youtube.com/watch?v=BeUOBoSPWvA".encode())

            #si el cliente envia un comando invalido
            else:
                socket_cliente.send("Comando invalido".encode())

        except Exception as e:
            print(f"Error en la conexión con {client_address}: {str(e)}")
            pass

'''
Creacion de socket
'''
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind((HOST, PORT))
socket_servidor.listen(500)

'''
Cifrado con certificado SSL
'''
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="server_new.crt", keyfile="server_new.key")

print(f"Servidor escuchando en {HOST}:{PORT}")

while CLIENTES_CONECTADOS < LIMITE_CLIENTES:
    socket_cliente, client_address = socket_servidor.accept()
    ssl_socket = context.wrap_socket(socket_cliente, server_side=True)
    CLIENTES_CONECTADOS += 1
    thread = threading.Thread(target=client_thread, args=(ssl_socket, client_address))
    thread.start()
    print(f"Clientes conectados: {CLIENTES_CONECTADOS}")

print("Limite de clientes alcanzado. Cerrando servidor...")
socket_servidor.close()
