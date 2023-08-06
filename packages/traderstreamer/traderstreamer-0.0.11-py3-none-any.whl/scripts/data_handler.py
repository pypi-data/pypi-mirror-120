import os
import datetime
import threading
from pytz import timezone
from dotenv import load_dotenv
from tradernetwork import (
    PubSocket,
    PullSocket,
    ProxySocket,
)

from utils.docker_handler import DockerHandler
from utils.telegram_logger import TelegramLogger

load_dotenv(override=True)

KST = timezone('Asia/Seoul')

IS_DOCKER = bool(int(os.getenv('DOCKER', 0)))
NODE = os.getenv('NODE')


class SecondDataHandler:

    def __init__(self):
        if NODE == 'odd':
            self.server = 1
        elif NODE == 'even':
            self.server = 2
        else:
            self.server = None

        self.docker_handler = DockerHandler()
        self.task_id = None
        self.restarting_svc = None
        self.restarting = False # container는 하나씩 restart할 수 있도록 한다.
                                # restarting이 False일때만 restart할 수 있다.

        self.telegram = TelegramLogger()

        self.pub_socket = PubSocket(4005)

        sockets = {
            'bybit_sec_svc': PullSocket(4003),
            'binance_sec_svc': PullSocket(4004),
            'bybit_account_svc': PullSocket(4006),
            'bybit_bar_svc': PullSocket(4007),
            'binance_account_svc_1': PullSocket(4009),
            'binance_account_svc_2': PullSocket(4010),
        }
        self.stream_status = {svc: None for svc, _ in sockets.items()}

        # # healthcheck thread start
        # self._healthcheck_loop()

        proxy = ProxySocket(sockets)
        proxy.callback = self.callback
        proxy.start_proxy_server_loop()

    def check_stream_status(self, socket_name: str, data: dict):
        if 'account' in socket_name:
            if data['status'] == 'OFF':
                return

        self.stream_status[socket_name] = datetime.datetime.now()

    def callback(self, socket_name: str, data: dict):
        self.check_stream_status(socket_name, data)
        self.pub_socket.publish({'source': socket_name, 'data': data})

    def _healthcheck_loop(self):
        time_now = datetime.datetime.now()

        for svc, status in self.stream_status.items():
            if status is not None:
                if (time_now - status).seconds >= 5:
                    # self.task_id = self.docker_handler.restart(server=self.server, container=svc)
                    # if self.task_id is not None:
                    #     self.restarting_svc = svc
                    #     self.restarting = True
                    #     self._check_restart_done()

                    stopped_since = KST.localize(status).strftime("%Y-%m-%d %H:%M:%S.%f")
                    self.telegram.send_msg(f'📛 DATA STREAM STOPPED 📛 [SERVER {self.server}] {svc} has stopped streaming since: {stopped_since}')

        timer = threading.Timer(5, self._healthcheck_loop)
        timer.setDaemon(True)
        timer.start()

    def _check_restart_done(self):
        if self.restarting:
            status = self.docker_handler.task_status(self.task_id)

            if status == 'SUCCESS':
                print(f'{self.restarting_svc} restart success')
                self.task_id = None
                self.restarting = False
                self.restarting_svc = None
            elif status == 'PENDING':
                pass
            elif status == 'FAILURE':
                print(f'{self.restarting_svc} restart failed')
                self.task_id = None
                self.restarting = False
                self.restarting_svc = None

            timer = threading.Timer(1, self._check_restart_done)
            timer.setDaemon(True)
            timer.start()


if __name__ == '__main__':
    dh = SecondDataHandler()