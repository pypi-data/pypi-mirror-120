"""

파이썬 cybos 서버를 실행시킨 상태에서 서버와 통신하며 여러 명령어를 실행하는 클라이언트 모듈
"""
from socket import *
import pickle
from .data import CMD, AccountData, CurrentPriceData, MarketData, TopStocksData
from . import setting

from util_hj3415 import utils

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


class Command:
    def __init__(self):
        """

        소켓 통신을 이용하여 cybos 서버에 명령어를 내리는 클래스
        """
        self.setting = setting.load()
        if self.setting.active_port == 'UDP':
            self.addr = (self.setting.addr, setting.UDP_PORT)
        else:
            raise ValueError(f'Cybos server setting error: {self.setting}')
        print(f'Set server address : {self.addr}')

    def account(self) -> AccountData:
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_sock.sendto(CMD.ACCOUNT.name.encode(), self.addr)
            raw_data, addr = udp_sock.recvfrom(setting.UDP_BUFSIZ)
            acc_data = pickle.loads(raw_data)

            # 투자종목의 항목들에 대한 여러가지 전처치
            for stock in acc_data.stocks:
                # 종목코드에 A를 빼준다.
                stock['종목코드'] = stock['종목코드'].replace('A', '')
                # 체결장부단가에서 소수점 제거
                stock['체결장부단가'] = int(stock['체결장부단가'])
            logger.info(acc_data)
        finally:
            udp_sock.close()
        return acc_data

    def _code_manager(self, code: str, cmd: CMD):
        if not utils.is_6digit(code):
            raise ValueError
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        try:
            if cmd not in [CMD.CMGR_GET_NAME, CMD.CMGR_GET_STATUS, CMD.CMGR_IS_KOSPI200]:
                raise ValueError
            udp_sock.sendto(f'{cmd.name}/{code}'.encode(), self.addr)
            raw_data, addr = udp_sock.recvfrom(setting.UDP_BUFSIZ)
            code_data = pickle.loads(raw_data)
        finally:
            udp_sock.close()
        return code_data

    def get_name(self, code: str):
        return self._code_manager(code=code, cmd=CMD.CMGR_GET_NAME)

    def get_status(self, code: str):
        return self._code_manager(code=code, cmd=CMD.CMGR_GET_STATUS)

    def is_kospi200(self, code: str):
        return self._code_manager(code=code, cmd=CMD.CMGR_IS_KOSPI200)

    def cprice(self, code) -> CurrentPriceData:
        if not utils.is_6digit(code):
            raise ValueError
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_sock.sendto(f'{CMD.CPRICE.name}/{code}'.encode(), self.addr)
            raw_data, addr = udp_sock.recvfrom(setting.UDP_BUFSIZ)
            cprice_data = pickle.loads(raw_data)
            logger.info(cprice_data)
        finally:
            udp_sock.close()
        return cprice_data

    def inquire_order(self) -> list:
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_sock.sendto(CMD.INQ.name.encode(), self.addr)
            raw_data, addr = udp_sock.recvfrom(setting.UDP_BUFSIZ)
            order_list = pickle.loads(raw_data)
            logger.info(order_list)
        finally:
            udp_sock.close()
        return order_list

    def buy_order(self, code: str, amount: int, price: int):
        if not utils.is_6digit(code):
            raise ValueError
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_sock.sendto(f'{CMD.BUY.name}/{code}/{amount}/{price}'.encode(), self.addr)
            raw_data, addr = udp_sock.recvfrom(setting.UDP_BUFSIZ)
            result = pickle.loads(raw_data)
            logger.info(result)
        finally:
            udp_sock.close()

    def sell_order(self, code: str, amount: int, price: int):
        if not utils.is_6digit(code):
            raise ValueError
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_sock.sendto(f'{CMD.SELL.name}/{code}/{amount}/{price}'.encode(), self.addr)
            raw_data, addr = udp_sock.recvfrom(setting.UDP_BUFSIZ)
            result = pickle.loads(raw_data)
            logger.info(result)
        finally:
            udp_sock.close()

    def cancel_one(self, ordernum: str):
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_sock.sendto(f'{CMD.CANCEL.name}/one/{ordernum}'.encode(), self.addr)
            raw_data, addr = udp_sock.recvfrom(setting.UDP_BUFSIZ)
            result = pickle.loads(raw_data)
            logger.info(result)
        finally:
            udp_sock.close()

    def cancel_all(self, code: str):
        if not utils.is_6digit(code):
            raise ValueError
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_sock.sendto(f'{CMD.CANCEL.name}/all/{code}'.encode(), self.addr)
            raw_data, addr = udp_sock.recvfrom(setting.UDP_BUFSIZ)
            result = pickle.loads(raw_data)
            logger.info(result)
        finally:
            udp_sock.close()

    def get_market_info(self) -> MarketData:
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_sock.sendto(CMD.MARKET_INFO.name.encode(), self.addr)
            raw_data, addr = udp_sock.recvfrom(setting.UDP_BUFSIZ)
            market_info = pickle.loads(raw_data)
            logger.info(market_info)
        finally:
            udp_sock.close()
        return market_info

    def get_top_n_stocks(self, market: str = 'all', n: int = 5) -> TopStocksData:
        if market not in ['kospi', 'kosdaq', 'all']:
            raise ValueError(f'Invalid market type : {market}')
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        try:
            udp_sock.sendto(f'{CMD.TOP_STOCKS.name}/{market}/{n}'.encode(), self.addr)
            raw_data, addr = udp_sock.recvfrom(setting.UDP_BUFSIZ)
            top_n_data = pickle.loads(raw_data)
            logger.info(top_n_data)
        finally:
            udp_sock.close()
        return top_n_data
