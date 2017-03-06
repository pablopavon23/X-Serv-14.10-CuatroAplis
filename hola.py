#!/usr/bin/python3

import webapp
import socket


class holaApp(webapp.app):

    def process(self, parsedRequest,request):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>" +
                          "Hola!!!" +
                          "</h1></body></html>")

class adiosApp(webapp.app):
    def process(self, parsedRequest,request):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>" +
                              "Adios!!!" +
                              "</h1></body></html>")

if __name__ == "__main__":
    hola = holaApp()
    adios = adiosApp()
    port = 1234       #la creo global para que en aleatoria no me de fallo
    testWebApp = webapp.webApp("localhost", port, {'/hola': hola,
                                            '/adios': adios})
