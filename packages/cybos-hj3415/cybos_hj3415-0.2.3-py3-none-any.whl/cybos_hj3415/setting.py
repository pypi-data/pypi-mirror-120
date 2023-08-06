import os
import pickle

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)

DEF_SERVER_ADDR = '192.168.0.174'

# 서버측에서 설정할 포트와 버퍼크기임.
UDP_PORT = 21567
TCP_PORT = 21568
UDP_BUFSIZ = 65507
TCP_BUFSIZ = 1024

FILENAME = 'setting.pickle'
FULL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), FILENAME)


def load() -> dict:
    """
    return  {'addr': cybos서버주소, 'tcp_port': TCP_PORT, 'udp_port': UDP_PORT}
    """
    try:
        with open(FULL_PATH, "rb") as fr:
            p_dict = pickle.load(fr)
            logger.info(p_dict)
            return p_dict
    except (EOFError, FileNotFoundError) as e:
        logger.error(e)
        set_default()
        # 새로 만든 파일을 다시 불러온다.
        with open(FULL_PATH, "rb") as fr:
            p_dict = pickle.load(fr)
            logger.info(p_dict)
            return p_dict


def chg_addr(addr: str):
    p_dict = load()
    before = p_dict['addr']
    p_dict['addr'] = addr
    if before != addr:
        print(f'Change mongo setting : {before} -> {addr}')
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(p_dict, fw)


def set_tcp(port: int = TCP_PORT):
    p_dict = load()
    before = p_dict['tcp_port']
    p_dict['tcp_port'] = port
    p_dict['udp_port'] = ''
    if before != port:
        print(f'Change tcp port setting : {before} -> {port}')
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(p_dict, fw)


def set_udp(port: int = UDP_PORT):
    p_dict = load()
    before = p_dict['udp_port']
    p_dict['udp_port'] = port
    p_dict['tcp_port'] = ''
    if before != port:
        print(f'Change udp port setting : {before} -> {port}')
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(p_dict, fw)


def set_default():
    pickle_dict = {'addr': DEF_SERVER_ADDR, 'tcp_port': '', 'udp_port': UDP_PORT}

    with open(FULL_PATH, "wb") as fw:
        pickle.dump(pickle_dict, fw)


