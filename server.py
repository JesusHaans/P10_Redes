import socket
import threading
import sys
import pickle


class Servidor:

    mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexiones = []

    def __init__(self, IP, puerto):
        """
        Metodo que crea un instancia de la clase donde iniciliza un 
        socket, la direccion del cliente y la lista de conexiones
        """
        self.obtener_conexiones()
        self.obtener_socket()
        self.direccion = (str(IP), int(puerto))

    def obtener_socket(self):
        """
        Metodo para obtener el socket definido.
        """
        return self.mi_socket

    def asignar_socket(self, socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        """
        Metodo para asignar al cliente una nuevo socket
        """
        self.mi_socket = socket

    def obtener_num_conexiones(self):
        """
        Metodo para obtener el numero de conexiones del chat.
        """
        return len(self.conexiones)

    def obtener_conexiones(self):
        """
        Metodo para obtener las conexiones
        """
        return self.conexiones

    def obtener_direccion(self):
        """
        Metodo para obtener la direccion con la cual se ejecutara 
        el servidor.
        """
        return self.direccion

    def asignar_direccion(self, IP, puerto):
        """
        Metodo para asignar al servidor una direccion con la cual se va a 
        ejecutar el servidor.
        """
        self.IP = str(IP)
        self.puerto = int(puerto)
        self.direccion = (self.IP, self.puerto)
       
    def manejar_conexiones(self):
        """
        Metodo que se encarga de asignar a hilos de ejecucion las tareas del
        manejo y envio de los mensajes.
        """
        manejo = threading.Thread(target = self.manejo)
        manejo.setDaemon(True)
        manejo.start()

    def establecer_conexion(self):
        """
        Se encarga de establecer la conexion y esperar a que los clientes se
        conecten para interactuar entre ellos
        """
        try:
            while True:
                print("Esperando conexion ...")
                mensaje = input("")
                if mensaje == "DISCONNECT":
                    break
            self.obtener_socket().close()
            sys.exit()
        except:
            pass

    def mensajes(self, mensaje, cliente):
        """
        Metodo que se encarga de enviar los mensajes a todos los clientes
        conectados.
        """
        for conexion in self.conexiones:
            try:
                if conexion != cliente:
                    conexion.send(mensaje)
            except:
                self.conexiones.remove(conexion)

                            
    def manejo(self):
        """
        Metodo que se encarga del manejo de los clientes y los mensajes 
        dentro del chat.
        """
        while True:
            try:
                connection, addr = self.obtener_socket().accept()
                connection.setblocking(False)
                self.obtener_conexiones().append(connection)
                print(str(addr[0])+ ": " + str(addr[1]) + " connected")
            except:
                pass

            if self.obtener_num_conexiones() > 0:
                for clt in self.obtener_conexiones():
                    try:
                        datos = clt.recv(1024)
                        try:
                            self.mensajes(datos, clt)
                        except:
                            pass
                        if not datos:
                           print(str(addr[0])+ ": " + str(addr[1]) + " disconnected")
                           self.obtener_conexiones().remove(clt)
                           clt.close()
                           break
                    except:
                        pass

    def ejecutar_servidor(self):
        """
        Metodo que se encarga de ejecutar al servidor.
        """
        self.obtener_socket().bind(self.direccion)
        self.obtener_socket().listen(500)
        self.obtener_socket().setblocking(False)
        self.manejar_conexiones()
        self.establecer_conexion()
        
if __name__=="__main__":
	servidor = Servidor("0.0.0.0",5000)
	servidor.ejecutar_servidor()