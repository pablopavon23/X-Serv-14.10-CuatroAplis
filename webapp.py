#!/usr/bin/python3

"""
webAppMulti class

Root for hierarchy of classes implementing web applications
Each class can dispatch to serveral web applications, depending
on the prefix of the resource name

Copyright Jesus M. Gonzalez-Barahona, Gregorio Robles (2009-15)
jgb @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
October 2009, February 2015
"""

import socket


class app:
    """Application to which webApp dispatches. Does the real work

    Usually real applications inherit from this class, and redefine
    parse and process methods"""

    def parse(self, request, rest):
        """Parse the received request, extracting the relevant information.

        request: HTTP request received from the client
        rest:    rest of the resource name after stripping the prefix
        """

        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>" +
                          "Dumb application just saying 'It works!'" +
                          "</h1><p>App id: " + str(self) + "<p></body></html>")

class webApp:
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def select(self, request):              #a partir de la peticion nos dice que aplicacion queremos ejecutar
        """Selects the application (in the app hierarchy) to run.

        Having into account the prefix of the resource obtained
        in the request, return the class in the app hierarchy to be
        invoked. If prefix is not found, return app class
        """

        resource = request.split(' ')[1]     #request.split(' ',x) dividelo en espacios pero solo x veces
        for prefix in self.apps:                #en self.apps guarde el diccionario pasado a atributo
            if resource.startswith(prefix):     #si mi recurso empieza con el prefijo:
                print("Running app for prefix: " + prefix + \
                    ", rest of resource: " + resource[len(prefix):] + ".")
                return (self.apps[prefix], resource[len(prefix):])  #self.apps[prefix] me devuelve el objeto asociado a la clave con la que coincide (otherApp o anApp)
                                                                    #devolvemos tambien la peticion pasada esto es: en .../other/34 el 34 en adelante
        print("Running default app")
        return (self.myApp, resource)       #si no es ninguna de esas dos sera la otra que hemos creado en la linea 74

    def __init__(self, hostname, port, apps):
        """Initialize the web application."""

        self.apps = apps    #paso apps a atributo, que es una variable del objeto y se puede ver en cualquier lado del objeto, ya no es una variable local solo
                            #si quito la linea anterior debo pasarle a select apps como parametro de entrada porque seria una variable local de init. Esta
                            #es la diferencia entre una variable o diccionario y un atributo
        self.myApp = app()      #tercera aplicacion, igual que anApp y otherApp pero se crea dentro y por tanto de manera distinta

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        while True:
            print('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print('HTTP request received (going to parse and process):')
            request = recvSocket.recv(2048).decode('utf-8')
            print(request)
            (theApp, rest) = self.select(request)       #para saber que aplicacion de las tres debo ejecutar, theApp es la aplicacion y rest la peticion
            print(rest)
            parsedRequest = theApp.parse(request, rest)     #se lo pasamos al parse
            (returnCode, htmlAnswer) = theApp.process(parsedRequest,request)    #lo que sale del parse se lo pasamos al process
            print('Answering back...')
            recvSocket.send(bytes("HTTP/1.1 " + returnCode + " \r\n\r\n"
                            + htmlAnswer + "\r\n", 'utf-8'))
            recvSocket.close()

if __name__ == "__main__":
    anApp = app()
    otherApp = app()
    port = 1234        #la creo global para que en aleatoria no me de fallo
    testWebApp = webApp("localhost", port, {'/app': anApp,
                                            '/other': otherApp})    #diccionario con /app de clave y anApp valor, y /other clave y otherApp valor
#Cuando me pasen localhost:1234/app ejecuto anApp , cuando me pasen localhost:1234/other ejecuto otherApp, luego le he añadido aleat. Con aleat me daria
#luego una excepcion en la linea 78 ya que no meto ni app ni other ni aleat y me pasa a imprimir la pagina que tenia como excepcion
