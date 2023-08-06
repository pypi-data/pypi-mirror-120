import os
from typing import List
from dotenv import load_dotenv

from node_1.services import (
    BybitAccountStreamerService,
    BybitBarStreamerService,
    BybitMarketStreamerService,
    BybitSecondBarService,
)
from node_2.services import (
    BinanceAccountStreamerService,
    BinanceMarketStreamerService,
    BinanceSecondBarService,
)

from node_3.services import UpbitMarketStreamerService

load_dotenv(override=True)

DOCKER = bool(int(os.getenv('DOCKER', 0)))
NODE = os.getenv('NODE', 'local')

if NODE == 'odd':
    BYBIT_PUBLIC_KEY = os.getenv('BYBIT_SERVER_1_PUBLIC_KEY')
    BYBIT_PRIVATE_KEY = os.getenv('BYBIT_SERVER_1_SECRET_KEY')
elif NODE == 'even':
    BYBIT_PUBLIC_KEY = os.getenv('BYBIT_SERVER_2_PUBLIC_KEY')
    BYBIT_PRIVATE_KEY = os.getenv('BYBIT_SERVER_2_SECRET_KEY')
else:
    BYBIT_PUBLIC_KEY = os.getenv('BYBIT_PUBLIC_KEY')
    BYBIT_PRIVATE_KEY = os.getenv('BYBIT_PRIVATE_KEY')

BINANCE_PUBLIC_KEY = os.getenv('YG_BINANCE_PUBLIC_KEY')
BINANCE_PRIVATE_KEY = os.getenv('YG_BINANCE_SECRET_KEY')

if DOCKER:
    HOST = 'host.docker.internal'
else:
    HOST = 'localhost'

def bybit_mkt_svc(market: str = 'both',
                  monitor_coins: List[str] = ['BTCUSD', 'BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'ETCUSDT'],
                  pub_port: int = 800) -> BybitMarketStreamerService:
    bybit_mkt_svc = BybitMarketStreamerService('bybit-market-streamer-svc',
                                               'bybit_market_streamer',
                                               options={'auto_restart': True},
                                               name='bybit_market_streamer',
                                               market=market,
                                               monitor_coins=monitor_coins,
                                               pub_port=pub_port,
                                               verbose=False)
    return bybit_mkt_svc

def bybit_acc_svc(name: str = '',
                  public_key: str = BYBIT_PUBLIC_KEY,
                  private_key: str = BYBIT_PRIVATE_KEY,
                  push_port: int = 1000) -> BybitAccountStreamerService:
    bybit_acc_svc = BybitAccountStreamerService('bybit-account-streamer-svc',
                                                'bybit_account_streamer',
                                                options={'auto_restart': True},
                                                name=name,
                                                market='usdt',
                                                push_host=HOST,
                                                push_port=push_port,
                                                public_key=public_key,
                                                private_key=private_key,
                                                verbose=False)
    return bybit_acc_svc

def bybit_bar_svc(public_key: str = BYBIT_PUBLIC_KEY,
                  private_key: str = BYBIT_PRIVATE_KEY,
                  monitor_coins: List[str] = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'ETCUSDT'],
                  push_port: int = 1001) -> BybitBarStreamerService:
    bybit_bar_svc = BybitBarStreamerService('bybit-bar-streamer-svc',
                                            'bybit_bar_streamer',
                                            options={'auto_restart': True},
                                            name='bybit_bar_streamer',
                                            push_host=HOST,
                                            push_port=push_port,
                                            public_key=public_key,
                                            private_key=private_key,
                                            monitor_coins=monitor_coins,
                                            verbose=False)
    return bybit_bar_svc

def binance_mkt_svc_1(market: str = 'spot',
                      monitor_coins: List[str] = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'ETCUSDT'],
                      pub_port: int = 801) -> BinanceMarketStreamerService:
    binance_mkt_svc_1 = BinanceMarketStreamerService('binance-market-streamer-svc-1',
                                                     'binance_market_streamer_1',
                                                     options={'auto_restart': True},
                                                     name='binance_market_streamer',
                                                     market=market,
                                                     monitor_coins=monitor_coins,
                                                     pub_port=pub_port,
                                                     verbose=False)
    return binance_mkt_svc_1

def binance_mkt_svc_2(market: str = 'usdt',
                      monitor_coins: List[str] = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'ETCUSDT'],
                      pub_port: int = 802) -> BinanceMarketStreamerService:
    binance_mkt_svc_2 = BinanceMarketStreamerService('binance-market-streamer-svc-1',
                                                     'binance_market_streamer_1',
                                                     options={'auto_restart': True},
                                                     name='binance_market_streamer',
                                                     market=market,
                                                     monitor_coins=monitor_coins,
                                                     pub_port=pub_port,
                                                     verbose=False)
    return binance_mkt_svc_2

def binance_acc_svc_1(public_key: str = BINANCE_PUBLIC_KEY,
                      private_key: str = BINANCE_PRIVATE_KEY,
                      monitor_coins: List[str] = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'ETCUSDT'],
                      push_port: int = 1003) -> BinanceAccountStreamerService:
    binance_acc_svc_1 = BinanceAccountStreamerService('binance-account-streamer-svc-1',
                                                      'binance_account_streamer_1',
                                                      options={'auto_restart': True},
                                                      name='binance_account_streamer',
                                                      market='margin',
                                                      push_host=HOST,
                                                      push_port=push_port,
                                                      public_key=public_key,
                                                      private_key=private_key,
                                                      monitor_coins=monitor_coins,
                                                      verbose=False)
    return binance_acc_svc_1

def binance_acc_svc_2(public_key: str = BINANCE_PUBLIC_KEY,
                      private_key: str = BINANCE_PRIVATE_KEY,
                      push_port: int = 1004) -> BinanceAccountStreamerService:
    binance_acc_svc_2 = BinanceAccountStreamerService('binance-account-streamer-svc-2',
                                                      'binance_account_streamer_2',
                                                      options={'auto_restart': True},
                                                      name='binance_account_streamer',
                                                      market='usdt',
                                                      push_host=HOST,
                                                      push_port=push_port,
                                                      public_key=public_key,
                                                      private_key=private_key,
                                                      verbose=False)
    return binance_acc_svc_2

def upbit_mkt_svc(market: str = 'spot',
                  monitor_coins: List[str] = ['BTC', 'ETH', 'ADA', 'XRP', 'DOGE', 'DOT', 'UNI', 'BCH', 'LINK', 'LTC', 'LUNA', 'ETC', 'XLM'],
                  pub_port: int = 1002) -> UpbitMarketStreamerService:
    upbit_mkt_svc = UpbitMarketStreamerService('upbit-market-streamer-svc',
                                               'upbit_market_streamer',
                                               options={'auto_restart': True},
                                               name='upbit_market_streamer',
                                               market=market,
                                               monitor_coins=monitor_coins,
                                               pub_port=pub_port,
                                               verbose=False)
    return upbit_mkt_svc

def bybit_sec_svc(mkt_ports: List[int] = [800],
                  push_port: int = 803,
                  monitor_coins: List[str] = ['coinm.BTCUSD', 'usdt.BTCUSDT', 'usdt.ETHUSDT', 'usdt.DOGEUSDT', 'usdt.ETCUSDT']) -> BybitSecondBarService:
    bybit_sec_svc = BybitSecondBarService('bybit-second-bar-svc',
                                          'bybit_second_bar',
                                          options={'auto_restart': True},
                                          push_host=HOST,
                                          push_port=push_port,
                                          sub_host=HOST,
                                          sub_ports={f'bybit_{i}': port for i, port in enumerate(mkt_ports)},
                                          monitor_coins=monitor_coins,
                                          use_timestamp='local_timestamp',
                                          verbose=False)
    return bybit_sec_svc

def binance_sec_svc(mkt_ports: List[int] = [801, 802],
                    push_port: int = 804,
                    monitor_coins: List[str] = ['spot.BTCUSDT', 'spot.ETHUSDT', 'spot.DOGEUSDT', 'spot.ETCUSDT',
                                                'usdt.BTCUSDT', 'usdt.ETHUSDT', 'usdt.DOGEUSDT', 'usdt.ETCUSDT']) -> BinanceSecondBarService:
    binance_sec_svc = BinanceSecondBarService('binance-second-bar-svc',
                                              'binance_second_bar',
                                              options={'auto_restart': True},
                                              push_host=HOST,
                                              push_port=push_port,
                                              sub_host=HOST,
                                              sub_ports={f'binance_{i}': port for i, port in enumerate(mkt_ports)},
                                              monitor_coins=monitor_coins,
                                              use_timestamp='local_timestamp',
                                              verbose=False)
    return binance_sec_svc


if __name__ == '__main__':
    bybit_public_key = os.getenv('BYBIT_PUBLIC_KEY')
    bybit_private_key = os.getenv('BYBIT_PRIVATE_KEY')

    by_acc = bybit_acc_svc(bybit_public_key, bybit_private_key, 1000)
    by_bar = bybit_bar_svc(bybit_public_key, bybit_private_key, push_port=1001)

    by_acc.start()
    by_bar.start()


    # bi1 = binance_mkt_svc_1(pub_port=3000)
    # bi2 = binance_mkt_svc_2(pub_port=2001)

    # bi_sec = binance_sec_svc([1114, 1115], 1116)

    # bi1.start()
    # bi2.start()
    # bi_sec.start()