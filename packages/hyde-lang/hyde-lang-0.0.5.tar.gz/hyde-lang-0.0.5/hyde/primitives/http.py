from hyde.hyde_callable import HydeCallable
from hyde.hyde_instance import HydeInstance, HydeInstanceError


from http.server import BaseHTTPRequestHandler as PyBaseHttpRequestHandler
from http.server import HTTPServer
import threading
import os


class BasicHttpRequestHandler(HydeInstance):
    name = 'BasicHttpRequestHandler'

    class BasicHttpRequestHandlerFunction(HydeCallable):
        def __init__(self, handler, token):
            self.handler = handler
            self.token   = token

        
    class Serve(BasicHttpRequestHandlerFunction):
        arity = 0

        def call(self, _interpreter, _arguments):
            server = self._generate_singleton_http_server()
            thread = threading.Thread(
                target=server.serve_forever, kwargs={'poll_interval': 0.005}
            )
            thread.start()

        def _generate_singleton_http_server(self):
            request_attrs = self.handler.request_attrs

            class Handler(PyBaseHttpRequestHandler):
                def handle_single_request(self):
                    target_request_attr = None
                    content_type = self.guess_content_type()

                    if content_type == 'text/html':
                        for request_attr in request_attrs:
                            if request_attr['path'] == self.path:
                                target_request_attr = request_attr
                                break

                    if target_request_attr is None and content_type == 'text/html':
                        self.serve_404()
                    elif content_type != 'text/html':
                        self.serve_content(content_type)
                    else:
                        self.serve_html(request_attr['data'])

                def serve_404(self):
                    self.send_response(404)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write('not found'.encode('utf-8'))

                def serve_content(self, content_type):
                    self.send_response(200)
                    self.send_header('content-type', content_type)
                    self.end_headers()

                    if os.path.exists(self.path[1:]):
                        with open(self.path[1:], 'rb') as content:
                            self.wfile.write(content.read())
                    else:
                        self.wfile.write(''.encode('utf-8'))

                def serve_html(self, html):
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(html.encode('utf-8'))

                def guess_content_type(self):
                    try:
                        if self.path[-4:] == '.css':
                            return 'text/css'
                        elif self.path[-4:] == '.png':
                            return 'image/png'
                        elif self.path[-5:] == '.woff':
                            return 'font/woff'
                        elif self.path[-4:] in ['.otf', '.ttf']:
                            return f'font/{self.path[-3:]}'

                        return 'text/html'
                    except Exception:
                        return 'text/html'

                def do_GET(self):
                    self.handle_single_request()

            return HTTPServer(('', 5000), Handler)


    class ToString(BasicHttpRequestHandlerFunction):
        arity = 0

        def call(self, _interpreter, _arguments):
            return str(self.handler)


    def __init__(self, request_attrs):
        self.request_attrs = [element.value_map for element in request_attrs.elements]

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
