import os
import pickle
import platform

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.WARNING)

DEF_MONGO_ADDR = 'mongodb://localhost:27017'
DEF_WIN_SQLITE3_PATH = 'C:\\_db'
DEF_LINUX_SQLITE3_PATH = '/home/hj3415/Stock/_db'

FILENAME = 'setting.pickle'
FULL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), FILENAME)


class DbSetting:
    def __init__(self):
        self.mongo_addr = DEF_MONGO_ADDR
        self.active_mongo = True
        if 'Windows' in platform.platform():
            self.sqlite3_path = DEF_WIN_SQLITE3_PATH
        elif 'Linux' in platform.platform():
            self.sqlite3_path = DEF_LINUX_SQLITE3_PATH
        else:
            raise
        self.active_sqlite3 = False

    def __str__(self):
        s = ''
        if self.active_mongo:
            s += f'Mongo db(active) : {self.mongo_addr}\n'
        if self.active_sqlite3:
            s += f'Sqlite3 db(active) : {self.sqlite3_path}\n'
        return s


def load() -> DbSetting:
    try:
        with open(FULL_PATH, "rb") as fr:
            s = pickle.load(fr)
            logger.info(s)
            return s
    except (EOFError, FileNotFoundError) as e:
        logger.error(e)
        set_default()
        # 새로 만든 파일을 다시 불러온다.
        with open(FULL_PATH, "rb") as fr:
            s = pickle.load(fr)
            logger.info(s)
            return s


def chg_mongo_addr(addr: str):
    if addr.startswith('mongodb://'):
        s = load()
        before = s.mongo_addr
        s.mongo_addr = addr
        if before != s.mongo_addr:
            print(f'Change mongo setting : {before} -> {addr}')
        with open(FULL_PATH, "wb") as fw:
            pickle.dump(s, fw)
    else:
        raise ValueError(f'Invalid mongo address : {addr}')


def turn_off_mongo():
    s = load()
    s.active_mongo = False
    print(s)
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(s, fw)


def turn_on_mongo():
    s = load()
    s.active_mongo = True
    print(s)
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(s, fw)


def chg_sqlite3_path(path: str):
    s = load()
    before = s.sqlite3_path
    s.sqlite3_path = path
    if before != path:
        print(f'Change mongo setting : {before} -> {path}')
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(s, fw)


def turn_off_sqlite3():
    s = load()
    s.active_sqlite3 = False
    print(s)
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(s, fw)


def turn_on_sqlite3():
    s = load()
    s.active_sqlite3 = True
    print(s)
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(s, fw)


def set_default():
    s = DbSetting()
    print(s)
    with open(FULL_PATH, "wb") as fw:
        pickle.dump(s, fw)
