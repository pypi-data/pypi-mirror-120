import datetime
import numpy as np
from typing import Dict, List
from tradernetwork import (
    Service,
    SubSocket,
    PushSocket,
    ProxySocket,
)

from node_1.memory import FIELD_LIST


class BybitSecondBarService(Service):

    push_socket = None
    use_timestamp = 'local_timestamp'
    latest_time = datetime.datetime.now()
    data = {}

    def main(self,
             push_host: str,
             push_port: int,
             sub_host: str,
             sub_ports: Dict[str, int],
             monitor_coins: List[str],
             use_timestamp: str = 'local_timestamp',
             verbose: bool = True):

        """
        :param sub_ports: {'bybit_1': 888}
        :param monitor_coins: ['coinm.BTCUSD', 'usdt.BTCUSDT']
        :param use_timestamp: local_timestamp, server_timestamp

        --> local_timestamp는 서버에서 데이터를 받는 즉시 찍은 시간이다.
            server_timestamp는 실제 증권사/거래소에서 찍혀서 들어온 시간이다.

        market_streamer_svc에서 데이터가 들어오지 않으면 second bar data는 publish되지 않는다.
        """

        self.verbose = verbose

        if self.push_socket is None:
            self.push_socket = PushSocket(push_port, push_host)

        self.use_timestamp = use_timestamp

        self.monitor_coins = monitor_coins
        self.data = {coin: {field: np.nan for field in FIELD_LIST}
                     for coin in monitor_coins}
        self.price = {coin: np.nan for coin in monitor_coins}
        self.latency = []

        sub_sockets = {name: SubSocket(port, sub_host) for name, port in sub_ports.items()}
        proxy_socket = ProxySocket(sub_sockets)
        proxy_socket.callback = self.callback
        proxy_socket.start_proxy_server_loop()

    def _stop(self):
        self.stop()

        if self.push_socket is not None:
            self.push_socket.exit()
            del self.push_socket
            self.push_socket = None

    def _time(self):
        return datetime.datetime.now()

    def callback(self, socket_name: str, data: dict):
        self.update_second_bar(data)

    def _set_new_bar(self, key: str):
        price = self.price[key]
        self.latency = []
        self.data[key]['timestamp'] = self._time().strftime('%Y%m%d%H%M%S%f')[:-3]
        self.data[key]['latency'] = 0
        self.data[key]['current_price'] = price
        self.data[key]['open'] = price
        self.data[key]['high'] = price
        self.data[key]['low'] = price
        self.data[key]['close'] = price
        self.data[key]['volume'] = 0
        self.data[key]['tick_cnt'] = 0
        self.data[key]['buy_cnt'] = 0
        self.data[key]['buy_amt'] = 0
        self.data[key]['sell_cnt'] = 0
        self.data[key]['sell_amt'] = 0

    def update_second_bar(self, data: dict):
        key = f'{data["asset_type"]}.{data["symbol"]}'

        data_type = data['type']
        data_time = datetime.datetime.strptime(data[self.use_timestamp], '%Y%m%d%H%M%S%f')

        time_passed = (data_time - self.latest_time).seconds

        if data_type == 'trade':
            price = float(data['price'])
            volume = float(data['size'])
            side = data['side']

            self.price[key] = price
            self.latency.append(float(data['latency']))

            if side.lower() == 'buy':
                buy_cnt = 1
                sell_cnt = 0
                buy_amt = volume
                sell_amt = 0
            elif side.lower() == 'sell':
                buy_cnt = 0
                sell_cnt = 1
                buy_amt = 0
                sell_amt = volume
            else:
                buy_cnt = 0
                sell_cnt = 0
                buy_amt = 0
                sell_amt = 0

            if self.data[key]['open'] == np.nan:
                self._set_new_bar(key)

            self.data[key]['local_timestamp'] = data['local_timestamp']
            self.data[key]['server_timestamp'] = data['server_timestamp']
            self.data[key]['current_price'] = price
            self.data[key]['close'] = price
            self.data[key]['volume'] += volume
            self.data[key]['tick_cnt'] += 1
            self.data[key]['buy_cnt'] += buy_cnt
            self.data[key]['buy_amt'] += buy_amt
            self.data[key]['sell_cnt'] += sell_cnt
            self.data[key]['sell_amt'] += sell_amt

            if price > self.data[key]['high']:
                self.data[key]['high'] = price

            if price < self.data[key]['low']:
                self.data[key]['low'] = price

        elif data_type == 'orderbook':
            asks = data['asks']
            bids = data['bids']
            self.data[key] = {
                **self.data[key],
                **asks,
                **bids
            }
        else:
            pass

        if time_passed >= 1:
            self.latest_time = data_time

            if len(self.latency) != 0:
                latency = sum(self.latency) / len(self.latency)
            else:
                latency = 0

            for coin in self.monitor_coins:
                self.data[coin]['latency'] = latency

            # 데이터 publish하
            for coin, data in self.data.items():
                pub_data = {'source': 'bybit', 'symbol': coin, 'data': data}
                self.push_socket.publish(pub_data)

            # 데이터를 새로 만든다 (꼭 전송 후 실행하기)
            for coin in self.monitor_coins:
                self._set_new_bar(coin)

            if self.verbose:
                print(f'[{self.latest_time}] Sent data')


if __name__ == '__main__':
    svc = BybitSecondBarService('bybit-second-bar-svc',
                                'bybit_second_bar',
                                options={'auto_restart': True},
                                push_host='localhost',
                                push_port=4003,
                                sub_host='localhost',
                                sub_ports={'bybit_1': 888},
                                monitor_coins=['coinm.BTCUSD', 'usdt.BTCUSDT'],
                                use_timestamp='local_timestamp')
    svc.start()