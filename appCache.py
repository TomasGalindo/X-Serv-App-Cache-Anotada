#! /usr/bin/python3
import urllib.request
import webapp

class appCache(webapp.webApp):

    cache = {}

    def parse(self, request):

        return (request.split(' ', 1)[0],
                request.split(' ', 2)[1])

    def process(self, parsed):
        method, resourceName = parsed
        if method == "GET":
            print(resourceName.split("/")[1])
            if resourceName.split("/")[1] == "reload":
                url = resourceName.split("/")[2]
                url = "http://" + url
                httpCode = "302"
                htmlBody = ("<meta http-equiv='refresh' content=0;url=" + url + ">")
            else:
                try:
                    if resourceName in self.cache:
                        httpCode = "200 OK"
                        htmlBody = self.cache[resourceName]
                    else:
                        url = "http:/" + resourceName
                        f = urllib.request.urlopen(url)
                        html = f.read().decode("utf-8")  # html de pag
                        # INTRODUCIR EL MENU
                        antes = html.find("<body")
                        despues = html.find(">",antes)
                        menu = ("<p><a href=" + url + "> Página original</a></p>" \
                                        + "<p><a href=/reload" + resourceName +
                                        "> Recargar </p></a>")
                        body = html[:despues + 1] + menu + html[despues + 1:]
                        # peticion
                        httpCode = "200 OK"
                        htmlBody = body
                        self.cache[resourceName] = htmlBody

                except urllib.error.URLError:
                    httpCode = "404 Not Found"
                    htmlBody = "No has introducido ninguna url"
                except UnicodeDecodeError:
                    httpCode = "404 Not Found"
                    htmlBody = "DECODE ERROR"
        else:
            httpCode = "405 Not method Allowed"
            htmlBody = ("<html><body>ERROOOOOOOOOOOR</html>")

        print("CACHE: " + str(self.cache.keys()))

        return (httpCode, htmlBody)


if __name__ == "__main__":  # si esto es el programa principal.
    testWebApp = appCache("localhost", 1234)  # hacer urlaleat
