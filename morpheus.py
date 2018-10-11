import socket, pickle
import interal_jnet_port_forwarding as jnet_port_forwarding
import typing

def on_connection(_func:typing.Callable) -> typing.Callable:
    def _wrapper(_cls):
        setattr(_cls, 'on_accept_connection', _func)
        return _cls
    return _wrapper

class Server:
    @jnet_port_forwarding.greet()
    @jnet_port_forwarding.PortManager.forward_port()
    def __enter__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'listening on {self.port} at "{self.main_host}"')
        self._socket.bind((self.main_host, self.port))
        self._socket.listen(self._max_connections)
        return self
    def accept_connections(self):
        while True:
            try:
                c, addr = self._socket.accept()
            except:
                pass
            else:
                '''
                print(f'Recieved connnection from {addr[0]}')
                _data = c.recv(_rec_size)
                print(f'Got {_data} from {addr[0]}')
                c.sendall(pickle.dumps(on_recieve(pickle.loads(_data))))
                '''
                self.__class__.on_accept_connection(c, addr)
    @jnet_port_forwarding.PortManager.reset_mapping
    def __exit__(self, *args):
        print(self.__dict__)
        self._socket.close()



class Client:
    def __init__(self, _host:str, _port:int) -> None:
        self.host, self.port = _host, _port
    def __enter__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))
        return self
    def send_data(self, _data):
        print('in here', _data)
        val = pickle.dumps(_data)
        print('val', val)
        self._socket.sendall(val)
        result = self._socket.recv(1024)
        print('got result here', result)
        return pickle.loads(result)
    def __exit__(self, *args):
        pass

if __name__ == '__main__':

    def recieve_connection(_client, addr):
        print('this is new here')
        print(f'Recieved connnection from {addr[0]}')
        _data = _client.recv(1024)
        print(f'Got {_data} from {addr[0]}')
        _client.sendall(pickle.dumps({'echo':pickle.loads(_data)}))
    
    @on_connection(recieve_connection)
    class Manage_Server(Server):
        _max_connections = 5
        main_host = ''
        lan_ip = jnet_port_forwarding.PortManager.get_my_ip()
        root = 'PASSWORD'
        port = 6000
        from_port = 8423
        forward_ports = True

    with Manage_Server() as server:
        server.accept_connections()
