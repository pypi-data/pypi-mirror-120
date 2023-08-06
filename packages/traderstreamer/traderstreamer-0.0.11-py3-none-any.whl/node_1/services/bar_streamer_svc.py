import pytz
import datetime
import traceback
import threading
from typing import List
from cointraderkr import BybitAPI
from multiprocessing import Queue
from tradernetwork import Service, PushSocket


class BybitBarStreamerService(Service):

    name = None
    market = None
    push_host = None
    push_port = None
    verbose = None
    public_key = None
    private_key = None
    monitor_coins = None

    push_socket = None
    api = None
    data = {}
    last_hour_time = None
    pub_socket = None
    q = Queue()

    def main(self,
             name: str,
             push_host: str,
             push_port: int,
             public_key: str,
             private_key: str,
             monitor_coins: List[str] = ['BTCUSDT'],
             verbose: bool = True):

        self.name = name
        self.push_host = push_host
        self.push_port = push_port
        self.public_key = public_key
        self.private_key = private_key
        self.monitor_coins = monitor_coins
        self.verbose = verbose

        self.api = BybitAPI(self.public_key, self.private_key)

        self.push_socket = PushSocket(push_port, push_host)

        self._request_loop()

        while True:
            message = self.q.get()

            if message['type'] == 'data':
                data = message['data']
                self.push_socket.publish(data)

                if self.verbose:
                    print(data)

            elif message['type'] == 'stop':
                if self.push_socket is not None:
                    self.push_socket.exit()
                    del self.push_socket
                    self.push_socket = None

    def _stop(self):
        self.q.put({'type': 'stop'})
        self.stop()

    def _request_loop(self):
        if self.push_socket is not None:
            time_now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))

            if self.last_hour_time is None:
                self._request_data()
            else:
                if len(set([d['data']['timestamp'] for _, d in self.data.items()])) != 1:
                    self._request_data()

                if (time_now - self.last_hour_time).seconds >= 3600:
                    self._request_data()
                else:
                    for symbol, data in self.data.items():
                        self.push_socket.publish(data)

                    if self.verbose:
                        print(f'[{time_now}] Sent data')

            timer = threading.Timer(1, self._request_loop)
            timer.setDaemon(True)
            timer.start()

    def _request_data(self):
        for symbol in self.monitor_coins:
            t = threading.Thread(target=self._request_hour_data, args=(symbol,))
            t.start()

    def _request_hour_data(self, symbol: str):
        try:
            yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
            # yesterday = (datetime.datetime.now() - datetime.timedelta(seconds=3600)).strftime('%Y-%m-%d %H:%M:%S')
            data = self.api.get_usdt_futures_data(symbol, '60m', yesterday)
            data['timestamp'] = data['start_at'].shift(-1)
            data = data[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            data = data[data['timestamp'].notna()]
            curr_data: dict = data.iloc[-1].to_dict()
            self.last_hour_time = curr_data['timestamp']
            curr_data['timestamp'] = curr_data['timestamp'].strftime('%Y%m%d%H%M%S')
            curr_data = {
                'source': 'bybit',
                'symbol': f'usdt.{symbol}',
                'data': curr_data
            }
            self.data[symbol] = curr_data
            self.q.put({'type': 'data', 'data': curr_data})
        except:
            traceback.print_exc()


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    load_dotenv(override=True)

    bybit_public_key = os.getenv('BYBIT_PUBLIC_KEY')
    bybit_private_key = os.getenv('BYBIT_PRIVATE_KEY')

    svc = BybitBarStreamerService('bybit-bar-streamer-svc',
                                  'bybit_bar_streamer',
                                  options={'auto_restart': True},
                                  name='bybit-bar-streamer',
                                  push_host='localhost',
                                  push_port=1010,
                                  public_key=bybit_public_key,
                                  private_key=bybit_private_key,
                                  monitor_coins=['BTCUSDT', 'ETHUSDT', 'XRPUSDT'])
    svc.start()