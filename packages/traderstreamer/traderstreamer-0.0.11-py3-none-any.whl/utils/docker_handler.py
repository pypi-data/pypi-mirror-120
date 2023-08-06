import os
from dotenv import load_dotenv
from tradernetwork import ReqSocket

load_dotenv(override=True)

HOST = os.getenv('SERVER_2_HOST')


class DockerHandler:

    def __init__(self):
        self.conn = ReqSocket(20000, HOST)

    def restart(self, server: int or None, container: str):
        """
        server를 None으로 넣으면 컨테이너가 실행되고 있는 서버 정보가 없기 때문에 재실행되지 않는다.
        """
        if server is not None:
            self.conn._send_request('restart_container', server=server, container=container)
            res = self.conn._recv()
            return res['message']
        else:
            print(f'Cannot restart docker container: {container}. Not used in docker context.')

    def task_status(self, task_id: str):
        self.conn._send_request('status', task_id=task_id)
        res = self.conn._recv()
        return res['message']


if __name__ == '__main__':
    import time

    handler = DockerHandler()
    task_id = handler.restart(2, 'test_bybit_market_svc')
    print(task_id)

    while True:
        time.sleep(1)
        status = handler.task_status(task_id)
        print(status)
        if status == 'SUCCESS':
            break
        elif status == 'PENDING':
            continue