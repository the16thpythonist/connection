import socket
import json


class ConnectionInterface:
    """
    This is an Interface for connection objects. Connection objects are supposed to be the very basic building block
    for communication mostly (but not only) between different processes, and/or different programming languages.
    The connection interface enforces the behaviour to send and receive strings and objects alike, using the JSON
    format as a way of serializing objects (since web servers are among the aspired use cases).

    USAGE:
    For the actual usage of a connection only the following methods will be needed:
    - 'send' sends an object trough the connection, which is serialized in the JSON string format
    - 'receive' waits (blocking) for an incoming transmission and returns the object sent.
    --> Aside from these basic characteristics the underlying implementation of a connection might differ. It could
    for example be built on mail transfer, sockets, IOStreams... Thus the required process of creating this required
    foundation for a connection varries with the concrete implementation, but the means of how data is sent and
    received will be mostly dictated by this Interface
    """
    def __init__(self):
        pass

    def receive_length(self, length):
        raise NotImplementedError()

    def receive(self):
        raise NotImplementedError()

    def sendall_bytes(self, string):
        raise NotImplementedError()

    def sendall_string(self, string):
        raise NotImplementedError()

    def send_string(self, string):
        raise NotImplementedError()

    def send_json(self, obj):
        raise NotImplementedError()

    def send(self, obj):
        raise NotImplementedError()


class SimpleSocketConnection(ConnectionInterface):

    JSON_TYPE = b'j'
    STRING_TYPE = b's'

    HEADER_LENGTH = 10

    def __init__(self, sock):
        ConnectionInterface.__init__(self)

        self.sock = sock

    def receive_length(self, length):
        data = b''

        while len(data) < length:

            received = self.sock.recv(length - len(data))

            data += received

        return data

    def sendall_bytes(self, bytes_string):
        self.sock.sendall(bytes_string)

    def sendall_string(self, string):
        bytes_string = string.encode()
        self.sock.sendall(bytes_string)

    def send_string(self, string):
        length = self._length(string)
        self._initiate(self.STRING_TYPE, length)

        self.sendall_string(string)

    def send_json(self, obj):
        json_string = json.dumps(obj)
        self.send_string(json_string)

    def send(self, obj):
        self.send_json(obj)

    def _wait(self):
        header_bytes = self.receive_length(self.HEADER_LENGTH)
        type_byte = header_bytes[0]
        length_bytes = header_bytes[1:]

        length = int(length_bytes.decode())

        return type_byte, length

    def _initiate(self, send_type, length):
        # Assembling the header bytes from the type byte and the length bytes
        length_bytes = str(length).zfill(self.HEADER_LENGTH - 1)
        header_bytes = send_type + length_bytes

        self.sendall_bytes(header_bytes)

    def receive(self):
        send_type, length = self._wait()

        data = self.receive_length(length)

        if send_type == self.STRING_TYPE:
            data_string = data.decode()
            return data_string
        elif send_type == self.JSON_TYPE:
            data_string = data.decode()
            data_object = json.loads(data_string)
            return data_object

    @staticmethod
    def _length(string):
        return len(string.encode())
