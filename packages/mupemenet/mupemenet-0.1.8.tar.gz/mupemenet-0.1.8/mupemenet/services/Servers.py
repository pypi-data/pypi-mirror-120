import asyncio
from queue import Queue
from mvc.eventbus.requests.BasicRequests import FrPipelineRequest
import socket
from pyeventbus3.pyeventbus3 import PyBus
import websockets
import threading
import asyncio
import ssl
from config.Config import HOME_PATH, RESOURCES_PATH
from logging import debug, warning

PORT_NUMBER = 38301
S_PORT_NUMBER = 49412
    

class FaceRecognitionServer:

    async def service(self, websocket, path):
        messsage = await websocket.recv()
        queue = Queue()
        debug("Sending FrPipelineRequest event")
        PyBus.Instance().post(FrPipelineRequest(lambda user, queue: queue.put(user), queue))
        debug("Wating for user iformation")
        user = queue.get()
        debug("User information received. Sending to client")
        await websocket.send(str(user))
        debug("User information Sent!!!")
    
    
    def make_ssl_context(self) -> ssl.SSLContext:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        certfile = RESOURCES_PATH+"/certificates/certificate.pem"
        keyfile = RESOURCES_PATH+"/certificates/key.pem"
        ssl_context.load_cert_chain(certfile, keyfile)
        return ssl_context

    @staticmethod
    def get_ip_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def start_loop(self, loop, server):
        loop.run_until_complete(server)
        loop.run_forever()
    
    def serve(self, secure: bool=False):
        if secure is True:
            PORT = S_PORT_NUMBER
            ssl_context = self.make_ssl_context()
        else:
            PORT = PORT_NUMBER
            ssl_context = None
        host = FaceRecognitionServer.get_ip_address()
        protocol = 'wss' if secure is True else 'ws'
        debug(f'Starting {protocol} on {host}:{PORT}')
        new_loop = asyncio.new_event_loop()
        start_server = websockets.serve(self.service, host, PORT, loop=new_loop, ssl=ssl_context)
        t = threading.Thread(target=self.start_loop, args=(new_loop, start_server))
        t.start()


def launch_face_recognition_servers():
    FaceRecognitionServer().serve()
    FaceRecognitionServer().serve(secure=True)


