import os
import datetime
import threading
import traceback
from typing import List
from dotenv import load_dotenv
from multiprocessing import Queue

from scripts.services import (
    bybit_mkt_svc,
    bybit_acc_svc,
    bybit_bar_svc,
    binance_mkt_svc_1,
    binance_mkt_svc_2,
    binance_acc_svc_1,
    binance_acc_svc_2,
    upbit_mkt_svc,
    bybit_sec_svc,
    binance_sec_svc,
)

load_dotenv(override=True)

DOCKER = bool(int(os.getenv('DOCKER', 0)))

if DOCKER:
    HOST = 'host.docker.internal'
else:
    HOST = 'localhost'


class ServiceNode:

    err_q = Queue()
    streaming = False

    def __init__(self,
                 svc_name: str,
                 port_range: List[int] = list(range(1000, 1011)),
                 odd_even: str = None):

        if len(port_range) < 11:
            raise Exception('port range should have at least 11 ports')

        self.svc_name = svc_name
        self.odd_even = odd_even

        self.services = {
            'bybit_market_svc': [bybit_mkt_svc, {'pub_port': port_range[0]}],
            'bybit_account_svc': [bybit_acc_svc, {'push_port': port_range[6]}],
            'bybit_coin_arbit_account_svc': [bybit_acc_svc, {
                'name': 'coin_arbit',
                'public_key': os.getenv('COIN_ARBIT_BYBIT_PUBLIC_KEY'),
                'private_key': os.getenv('COIN_ARBIT_BYBIT_PRIVATE_KEY'),
                'push_port': port_range[6],
            }],
            'bybit_trend_emamacross_account_svc': [bybit_acc_svc, {
                'name': 'trend_emamacross',
                'public_key': os.getenv('TREND_EMAMACROSS_BYBIT_PUBLIC_KEY'),
                'private_key': os.getenv('TREND_EMAMACROSS_BYBIT_PRIVATE_KEY'),
                'push_port': port_range[6],
            }],
            'bybit_bar_svc': [bybit_bar_svc, {'push_port': port_range[7]}],

            'binance_market_svc_1': [binance_mkt_svc_1, {'pub_port': port_range[1]}],
            'binance_market_svc_2': [binance_mkt_svc_2, {'pub_port': port_range[2]}],
            'binance_account_svc_1': [binance_acc_svc_1, {'push_port': port_range[9]}],
            'binance_account_svc_2': [binance_acc_svc_2, {'push_port': port_range[10]}],

            'upbit_market_svc': [upbit_mkt_svc, {'pub_port': port_range[8]}],

            'bybit_sec_svc': [bybit_sec_svc, {'mkt_ports': [port_range[0]], 'push_port': port_range[3]}],
            'binance_sec_svc': [binance_sec_svc, {'mkt_ports': [port_range[1], port_range[2]], 'push_port': port_range[4]}]
        }

        if (svc_name in ['bybit_market_svc',
                         'bybit_account_svc',
                         'bybit_coin_arbit_account_svc',
                         'bybit_trend_emamacross_account_svc',
                         'bybit_bar_svc',
                         'binance_market_svc_1',
                         'binance_market_svc_2',
                         'binance_account_svc_1',
                         'binance_account_svc_2',
                         'upbit_market_svc']) and \
                (self.odd_even is not None):
            self._monitor()
        else:
            self.start()

        while True:
            err = self.err_q.get()
            raise Exception(err)

    def _time(self):
        return datetime.datetime.now()

    def start(self):
        self.streaming = True

        service = self.services[self.svc_name][0]
        params = self.services[self.svc_name][1]
        self.svc = service(**params)

        self.svc.start()

    def stop(self):
        self.streaming = False
        self.svc._stop()
        del self.svc

    def _monitor(self):
        try:
            time_now = self._time()

            five_mins_after = (time_now + datetime.timedelta(minutes=5)).hour

            if five_mins_after == 0:
                five_mins_after = 24

            def _start():
                if self.odd_even == 'even':
                    return not self.streaming and five_mins_after % 2 == 0
                else:
                    return not self.streaming and five_mins_after % 2 != 0

            def _stop():
                if self.odd_even == 'even':
                    return self.streaming and time_now.hour % 2 != 0 and not (five_mins_after % 2 == 0)
                else:
                    return self.streaming and time_now.hour % 2 == 0 and not (five_mins_after % 2 != 0)

            if _start():
                print(f'\n[{time_now}] Streaming start')
                self.start()

            if _stop():
                print(f'\n[{time_now}] Streaming stop')
                self.stop()
                self.err_q.put('STOP')
        except:
            traceback.print_exc()
            self.err_q.put('ERROR')

        timer = threading.Timer(1, self._monitor)
        timer.setDaemon(True)
        timer.start()


if __name__ == '__main__':
    node = ServiceNode(svc_name='binance_account_svc_1')