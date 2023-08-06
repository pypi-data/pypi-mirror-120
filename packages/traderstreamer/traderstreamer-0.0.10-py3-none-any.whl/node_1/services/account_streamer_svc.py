import os
import datetime
import threading
from typing import List
from multiprocessing import Queue

from cointraderkr import BybitWebsocket
from tradernetwork import Service, PushSocket


class BybitAccountStreamerService(Service):

    name = None
    market = None
    push_host = None
    push_port = None
    verbose = None
    public_key = None
    private_key = None

    push_socket = None
    usdt_socket = None
    coinm_socket = None
    q = Queue()

    def main(self,
             name: str,
             market: str,
             push_host: str,
             push_port: int,
             public_key: str,
             private_key: str,
             monitor_coins: List[str] = [],
             verbose: bool = True):

        self.public_key = public_key
        self.private_key = private_key
        self.monitor_coins = monitor_coins

        self.name = name
        self.market = market
        self.push_host = push_host
        self.push_port = push_port
        self.verbose = verbose

        self.ping_status = None

        if market == 'usdt':
            self._start_usdt_socket()

        if market == 'coinm':
            self._start_coinm_socket()

        if self.ping_status:
            self._ping_loop()
            self._healthcheck_loop()

            self.push_socket = PushSocket(push_port, push_host)

            while True:
                message = self.q.get()

                if message['type'] == 'data':
                    data = message['data']
                    req_op = data.get('request', {}).get('op', '')

                    if req_op in ['auth', 'subscribe']:
                        pass

                    elif req_op == 'ping':
                        self.ping_status = self._time()

                    else:
                        self.push_socket.publish({'name': self.name, **data})

                elif message['type'] == 'stop':
                    if self.market == 'usdt':
                        self.usdt_socket.exit()
                        del self.usdt_socket

                    elif self.market == 'coinm':
                        self.coinm_socket.exit()
                        del self.coinm_socket

                    if self.push_socket is not None:
                        self.push_socket.exit()
                        del self.push_socket
                        self.push_socket = None

    def _stop(self):
        self.q.put({'type': 'stop'})
        self.stop()

    def _time(self):
        return datetime.datetime.now()

    def _start_usdt_socket(self):
        url = 'wss://stream.bytick.com/realtime_private'
        self.usdt_socket = BybitWebsocket(url,
                                          self.public_key,
                                          self.private_key,
                                          self.callback)

        self.ping_status = self._time()

        self.usdt_socket.subscribe_position()
        self.usdt_socket.subscribe_execution()
        self.usdt_socket.subscribe_order()
        self.usdt_socket.subscribe_stop_order()
        self.usdt_socket.subscribe_wallet()

    def _start_coinm_socket(self):
        url = 'wss://stream.bytick.com/realtime'
        self.coinm_socket = BybitWebsocket(url,
                                           self.public_key,
                                           self.private_key,
                                           self.callback)

        self.ping_status = self._time()

        self.coinm_socket.subscribe_position()
        self.coinm_socket.subscribe_execution()
        self.coinm_socket.subscribe_order()
        self.coinm_socket.subscribe_stop_order()
        self.coinm_socket.subscribe_wallet()

    def callback(self, data: dict):
        self.q.put({'type': 'data', 'data': data})

    def _ping_loop(self):
        for socket in [self.usdt_socket, self.coinm_socket]:
            if socket is not None:
                socket.ping()

        timer = threading.Timer(5, self._ping_loop)
        timer.setDaemon(True)
        timer.start()

    def _healthcheck_loop(self):
        time_now = self._time()

        if (self.push_socket is not None) and (self.ping_status is not None):
            if (time_now - self.ping_status).seconds >= 10:
                self.push_socket.publish({'source': 'bybit',
                                          'name': self.name,
                                          'asset_type': self.market,
                                          'type': 'socket_status',
                                          'status': 'OFF'})
            else:
                self.push_socket.publish({'source': 'bybit',
                                          'name': self.name,
                                          'asset_type': self.market,
                                          'type': 'socket_status',
                                          'status': 'ON'})

        timer = threading.Timer(1, self._healthcheck_loop)
        timer.setDaemon(True)
        timer.start()


if __name__ == '__main__':
    bybit_public_key = os.getenv('COIN_ARBIT_BYBIT_PUBLIC_KEY')
    bybit_private_key = os.getenv('COIN_ARBIT_BYBIT_PRIVATE_KEY')

    svc = BybitAccountStreamerService('bybit-account-streamer-svc',
                                      'bybit_account_streamer',
                                      options={'auto_restart': True},
                                      name='test_bybit_streamer',
                                      market='usdt',
                                      push_host='localhost',
                                      push_port=4006,
                                      public_key=bybit_public_key,
                                      private_key=bybit_private_key)
    svc.start()