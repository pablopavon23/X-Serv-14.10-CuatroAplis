#!/usr/bin/python3

import webapp
import socket


class sumaApp(webapp.app):
    def process(self, parsedRequest,request):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """
        try:
            #tengo en mi peticion: GET /suma/3+4 HTTP/1.1
            recurso = request.split()[1][1:]       #esto me lo deja en ['GET','/suma/3+4','HTTP/1.1'] y cojo la posicion 1
                                                    #que es /suma/3+4, el 1: me lo deja en suma/3+4
            sumandos = recurso.split('/')[1]        #ahora me queda ['suma','3+4'] y cojo la posicion 1 que es 3+4
            sumando1, sumando2 = sumandos.split('+')    #esto me deja sumando1 como 3 y sumando2 como 4
            suma = int(sumando1) + int(sumando2)
            return ("200 OK", "<html><body><h1>" +
                              "Me estas pidiendo:  " + sumandos +
                              ". Y la suma es:    " + str(suma) +
                              "</h1></body></html>")
        except ValueError:
            return("404 Not found", "<html><body><h1>" +
                              "Debes introducir dos numeros!!!" +
                              "</h1></body></html>")

if __name__ == "__main__":
    suma = sumaApp()
    port = 1234       #la creo global para que en aleatoria no me de fallo
    testWebApp = webapp.webApp("localhost", port, {'/suma': suma})
