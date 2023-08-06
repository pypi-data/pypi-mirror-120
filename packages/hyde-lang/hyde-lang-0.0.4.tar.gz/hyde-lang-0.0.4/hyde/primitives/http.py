from hyde.hyde_callable import HydeCallable
from hyde.hyde_instance import HydeInstance, HydeInstanceError


from http.server import BaseHTTPRequestHandler as PyBaseHttpRequestHandler
from http.server import HTTPServer
import threading


class BasicHttpRequestHandler(HydeInstance):
    name = "BasicHttpRequestHandler"

    class BasicHttpRequestHandlerFunction(HydeCallable):
        def __init__(self, handler, token):
            self.handler = handler
            self.token   = token

        
    class Serve(BasicHttpRequestHandlerFunction):
        arity = 0

        def call(self, _interpreter, _arguments):
            self._generate_singleton_http_server()

        def _generate_singleton_http_server(self):
            request_attrs = self.handler.request_attrs

            class Handler(PyBaseHttpRequestHandler):
                def do_GET(self):
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(request_attrs['data'].encode('utf-8'))

            server = HTTPServer(("", 5000), Handler)
            thread = threading.Thread(
                target=server.serve_forever, kwargs={"poll_interval": 0.005}
            )
            thread.start()

            return server


    class ToString(BasicHttpRequestHandlerFunction):
        arity = 0

        def call(self, _interpreter, _arguments):
            return str(self.handler)


    def __init__(self, request_attrs):
        self.request_attrs = request_attrs.value_map
    
    def get(self, name):
        if name.lexeme == 'serve':
            return BasicHttpRequestHandler.Serve(self, name)
        elif name.lexeme == 'toString':
            return BasicHttpRequestHandler.ToString(self, name)

        raise HydeInstanceError(name, f'Undefined property {name.lexeme} for {self.name} instance.')

    def set(self, name, _value):
        raise HydeInstanceError(name, "Can't add properties to BasicHttpRequestHandlers.")

    def __str__(self):
        return f'<BasicHttpRequestHandler route: {self.request_attrs}>'
