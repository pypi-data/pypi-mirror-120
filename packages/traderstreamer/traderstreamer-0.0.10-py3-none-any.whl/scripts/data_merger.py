import os
from dotenv import load_dotenv
from tradernetwork import (
    PubSocket,
    SubSocket,
    ProxySocket
)

load_dotenv(override=True)

SERVER_1_HOST = os.getenv('SERVER_1_HOST')
SERVER_2_HOST = os.getenv('SERVER_2_HOST')


class DataMerger:

    def __init__(self):
        self.pub_socket = PubSocket(4011)

        sockets = {
            'server_1': SubSocket(4005, SERVER_1_HOST),
            'server_2': SubSocket(4005, SERVER_2_HOST)
        }

        proxy = ProxySocket(sockets)
        proxy.callback = self.callback
        proxy.start_proxy_server_loop()

    def callback(self, socket_name: str, data: dict):
        self.pub_socket.publish({'server': socket_name, **data})


if __name__ == '__main__':
    dm = DataMerger()