import os
import datetime
import threading
import traceback
from typing import List
from multiprocessing import Queue
from binance.exceptions import BinanceAPIException

from tradernetwork import Service, PushSocket
from cointraderkr import (
    BinanceAPI,
    BinanceWebsocket,
)


class BinanceAccountStreamerService(Service):

    name = None
    market = None
    push_host = None
    push_port = None
    verbose = None
    public_key = None
    private_key = None
    streaming = False

    api = None
    push_socket = None
    margin_socket = None
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

        self.api = BinanceAPI(self.public_key, self.private_key)

        self.name = name
        self.market = market
        self.push_host = push_host
        self.push_port = push_port
        self.verbose = verbose

        self.ping_status = {}

        if market == 'margin':
            self._start_margin_socket()

        if market == 'usdt':
            self._start_usdt_socket()

        if market == 'coinm':
            self._start_coinm_socket()

        if any(list(self.ping_status.values())):
            self._ping_loop()
            self._healthcheck_loop()

            self.push_socket = PushSocket(push_port, push_host)

            while True:
                message = self.q.get()

                if message['type'] == 'data':
                    data = message['data']

                    if market == 'margin':
                        evt = data.get('event_type')
                        delta = data.get('balance_delta')

                        asset_type = data.get('type')

                        if evt == 'balanceUpdate' and abs(float(delta)) == 0.00000009:
                            if asset_type == 'spot_account':
                                self.ping_status['SPOT'] = self._time()
                            else:
                                symbol = data.get('symbol')
                                self.ping_status[symbol] = self._time()
                        else:
                            self.push_socket.publish(data)

                    if market == 'usdt':
                        p = data.get('a', {}).get('P', [{}])
                        p = p[0] if p else {}
                        m = data.get('a', {}).get('m')

                        if p.get('s') == '1000SHIBUSDT' and m == 'MARGIN_TYPE_CHANGE':
                            self.ping_status[self.market] = self._time()
                        else:
                            self.push_socket.publish(data)

                    if market == 'coinm':
                        """
                        TODO!! Coinm 추가하기
                        """
                        pass

                elif message['type'] == 'stop':
                    if self.market == 'margin':
                        self.margin_socket.close()
                        del self.margin_socket

                    elif self.market == 'usdt':
                        self.usdt_socket.close()
                        del self.usdt_socket

                    elif self.market == 'coinm':
                        self.coinm_socket.close()
                        del self.coinm_socket

                    if self.push_socket is not None:
                        self.push_socket.exit()
                        del self.push_socket
                        self.push_socket = None

    def _stop(self):
        print('STOPPING!!!!!')
        self.q.put({'type': 'stop'})
        self.stop()
        self.streaming = False

    def _time(self):
        return datetime.datetime.now()

    def _start_margin_socket(self):
        try:
            self.margin_socket = BinanceWebsocket(self.public_key,
                                                  self.private_key,
                                                  self.callback,
                                                  self.monitor_coins)
            self.margin_socket.stream_spot_margin_account_data()
            self.margin_socket.start()

            for symbol in self.monitor_coins + ['SPOT']:
                self.ping_status[symbol] = self._time()

            self.streaming = True
        except:
            traceback.print_exc()

    def _start_usdt_socket(self):
        try:
            self.usdt_socket = BinanceWebsocket(self.public_key,
                                                self.private_key,
                                                self.callback,
                                                self.monitor_coins)
            self.usdt_socket.stream_usdt_futures_account_data()
            self.usdt_socket.start()

            self.ping_status[self.market] = self._time()

            self.streaming = True
        except:
            traceback.print_exc()

    def _start_coinm_socket(self):
        try:
            self.coinm_socket = BinanceWebsocket(self.public_key,
                                                 self.private_key,
                                                 self.callback,
                                                 self.monitor_coins)
            self.coinm_socket.stream_coinm_futures_account_data()
            self.coinm_socket.start()

            self.ping_status[self.market] = self._time()

            self.streaming = True
        except:
            traceback.print_exc()

    def callback(self, data: dict):
        self.q.put({'type': 'data', 'data': data})

    def _ping_margin_socket(self):
        # mock 데이터 보내기
        mock_data = {
            'type': '',
            'symbol': '',
            'event_type': 'balanceUpdate',
            'balance_delta': '0.00000009'
        }
        self.q.put({'type': 'data', 'data': {**mock_data, 'type': 'spot_account'}})

        for symbol in self.monitor_coins:
            try:
                # self.api.transfer_isolated_margin_account(from_wallet='SPOT',
                #                                           to_wallet='ISOLATED_MARGIN',
                #                                           asset='USDT',
                #                                           symbol=symbol,
                #                                           amount=0.00000009)
                # self.api.transfer_isolated_margin_account(from_wallet='ISOLATED_MARGIN',
                #                                           to_wallet='SPOT',
                #                                           asset='USDT',
                #                                           symbol=symbol,
                #                                           amount=0.00000009)

                self.q.put({'type': 'data', 'data': {**mock_data,
                                                     'type': 'isolated_margin_account',
                                                     'symbol': symbol}})
            except:
                traceback.print_exc()
                print('ERROR PERFORMING TRANSFER ACCOUNT')

    def _ping_usdt_socket(self):
        # try:
        #     self.api.change_usdt_futures_margin_type(symbol='1000SHIBUSDT', marginType='ISOLATED')
        # except BinanceAPIException:
        #     self.api.change_usdt_futures_margin_type(symbol='1000SHIBUSDT', marginType='CROSSED')

        mock_data = {
            'a': {
                'P': [{
                    's': '1000SHIBUSDT'
                }],
                'm': 'MARGIN_TYPE_CHANGE'
            }
        }
        self.q.put({'type': 'data', 'data': mock_data})


    def _ping_coinm_socket(self):
        try:
            self.api.change_coinm_futures_margin_type(symbol='THEATAUSD_PERP', marginType='ISOLATED')
        except BinanceAPIException:
            self.api.change_coinm_futures_margin_type(symbol='THEATAUSD_PERP', marginType='CROSSED')

    def _ping_loop(self):
        if self.streaming:
            if self.market == 'margin':
                self._ping_margin_socket()

            if self.market == 'usdt':
                self._ping_usdt_socket()

            if self.market == 'coinm':
                self._ping_coinm_socket()

            timer = threading.Timer(3, self._ping_loop)
            timer.setDaemon(True)
            timer.start()

    def _healthcheck_loop(self):
        if self.streaming:
            time_now = self._time()

            if (self.push_socket is not None) and (self.ping_status is not None):
                if any([(time_now - ping_status).seconds >= 10 for _, ping_status in self.ping_status.items()]):
                    self.push_socket.publish({'source': 'binance',
                                              'asset_type': self.market,
                                              'type': 'socket_status',
                                              'status': 'OFF'})
                else:
                    self.push_socket.publish({'source': 'binance',
                                              'asset_type': self.market,
                                              'type': 'socket_status',
                                              'status': 'ON'})

            timer = threading.Timer(1, self._healthcheck_loop)
            timer.setDaemon(True)
            timer.start()


if __name__ == '__main__':
    import time
    from dotenv import load_dotenv

    load_dotenv(override=True)

    binance_public_key = os.getenv('YG_BINANCE_PUBLIC_KEY')
    binance_private_key = os.getenv('YG_BINANCE_SECRET_KEY')

    svc = BinanceAccoundStreamerService('bybit-account-streamer-svc',
                                        'bybit_account_streamer',
                                        options={'auto_restart': True},
                                        name='test_bybit_streamer',
                                        market='usdt',
                                        push_host='localhost',
                                        push_port=1113,
                                        public_key=binance_public_key,
                                        private_key=binance_private_key,
                                        monitor_coins=['BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'ETCUSDT'])
    svc.start()

    # while True:
    #     time.sleep(20)
    #     svc._stop()

    # def print_data(data):
    #     print(data)
    #
    # api = BinanceWebsocket(public_key=binance_public_key,
    #                        secret_key=binance_private_key,
    #                        callback=print_data,
    #                        monitor_coins=['BTCUSDT', 'ETHUSDT'])
    # api.stream_spot_margin_account_data()
    # api.start()

    # restapi = BinanceAPI(binance_public_key, binance_private_key)
    #
    # import time

    # while True:
    #     print('\n')
    #     time.sleep(5)
    #     try:
    #         for symbol in ['BTCUSDT', 'ETHUSDT']:
    #             restapi.transfer_isolated_margin_account(from_wallet='SPOT',
    #                                                      to_wallet='ISOLATED_MARGIN',
    #                                                      asset='USDT',
    #                                                      symbol=symbol,
    #                                                      amount=0.00000009)
    #             restapi.transfer_isolated_margin_account(from_wallet='ISOLATED_MARGIN',
    #                                                      to_wallet='SPOT',
    #                                                      asset='USDT',
    #                                                      symbol=symbol,
    #                                                      amount=0.00000009)
    #     except:
    #         traceback.print_exc()