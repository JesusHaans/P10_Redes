import socket
import threading
import sys
import pickle

class Cliente:

    mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    estado = ""
    
    def __init__(self, IP, puerto): 
        """
        Metodo que crea un instancia de la clase donde iniciliza un socket
        y la direccion del cliente
        """
        self.obtener_socket()
        self.direccion_cliente = (str(IP), int(puerto))

    def obtener_socket(self):
        """
        Metodo para obtener el socket definido
        """
        return self.mi_socket

    def asignar_socket(self, socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        """
        Metodo para asignar al cliente una nuevo socket
        """
        self.mi_socket = socket

    def obtener_direccion(self):
        """
        Metodo para obtener la direccion del cliente que se va a conectar con
        el servidor.
        """
        return self.direccion_cliente

    def asignar_direccion(self, IP, puerto):
        """
        Metodo para asignar al cliente una direccion con la cual se va a 
        conectar con el servidor.
        """
        self.IP = str(IP)
        self.puerto = int(puerto)
        self.direccion_cliente = (self.IP, self.puerto)

    def asignar_estado(self, status):
        """
        Metodo que se encarga de asignarle un estado al cliente mientras
        esta conectado
        """
        self.estado = status

    def obtener_estado(self):
        """
        Metodo para obtner el eestado del cliente
        """
        return self.estado

    def manejar_mensajes(self):
        """
        Metodo que se encarga de asignar a un hilo de ejecucion la tarea de 
        recibir los mensajes.
        """
        mensaje_recibido = threading.Thread(target = self.recibir_mensaje)
        mensaje_recibido.setDaemon(True)
        mensaje_recibido.start()

    def enviar_mensajes(self):
        """
        Metodo que se encarga de enviar el mensaje a todos los clientes 
        conectados.
        """
        print("Dame tu nombre de usuario: ")
        nombre_cliente = str(input())
        self.obtener_socket().send(pickle.dumps(nombre_cliente + " connected"))
        print("Escribe tus mensajes")
        while True:
            entrada = str(input())
            if entrada != "DISCONNECT":
                self.enviar_mensaje(nombre_cliente, entrada)
            else:
                self.obtener_socket().send(pickle.dumps(nombre_cliente + " disconnected"))
                self.obtener_socket().close()
                sys.exit()
                
    def recibir_mensaje(self):
        """
        Metodo que se encarga de aceptar los mensajes de otros clientes
        conectados
        """
        while True:
            try:
                respuesta = self.mi_socket.recv(1024)
                if respuesta:
                    print(pickle.loads(respuesta))
            except:
                pass

    def enviar_mensaje(self, nombre_cliente, mensaje):
        """
        Se encarga de enviar los mensajes.
        """
        try:
            self.obtener_socket().send(pickle.dumps("["+ nombre_cliente +"]: " + mensaje))
        except:
            print("Ocurrio un error al enviar el mensaje")

    def ejecutar_cliente(self):
        """
        Metodo que se encarga de conectar al cliente con el servidor
        """
        self.obtener_socket().connect(self.obtener_direccion())
        self.manejar_mensajes()
        self.enviar_mensajes()

if __name__=="__main__":
	cliente = Cliente(sys.argv[1], 5000)
	cliente.ejecutar_cliente()