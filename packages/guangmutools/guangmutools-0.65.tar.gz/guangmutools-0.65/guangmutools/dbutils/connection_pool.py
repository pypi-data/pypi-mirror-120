# -*- encoding: utf-8 -*-
'''
@文件    :connection_pool.py
@说明    :连接池管理
@时间    :2021/05/06 14:59:21
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import time
import threading
from contextlib import contextmanager

from shortuuid import uuid
from py2neo import Graph

from guangmutools.decorators import singleton

class ConnectionObject:
    '''
    连接对象
    '''
    def __init__(self, handler, duration):
        '''
        :param handler 连接对象
        '''
        self.handler = handler
        self.name = uuid()
        self.start_tm = time.time()
        self.last_use_time = self.start_tm
        self.usage_tms = 0         # 连接的使用次数
        self.duration = duration
        self.occupy = False

    def take_out(self):
        '''
        取出连接
        '''
        self.usage_tms += 1
        self.occupy = True

    def put_back(self):
        '''
        放回连接
        '''
        self.last_use_time = time.time()
        self.occupy = False
        
    def check_valid(self):
        '''
        检查是否可用
        :param duration 对象的生命时长
        :return bool
        '''
        return not self.occupy and (time.time() - self.last_use_time < self.duration)

    def need_clear(self):
        return not self.occupy and self.exceed_time()

    def exceed_time(self):
        '''
        判断连接对象是否过期
        '''
        return time.time() - self.last_use_time >= self.duration

class GmConnectionPool:
    def __init__(self, start_connection=1, max_connection=0, duration=600):
        # 启动时的默认连接数 > 0
        self.start_connection = start_connection
        # 最大连接数，0表示不限制
        self.max_connection = max_connection
        # 连接过期时间，0表示不过期
        self.duration = duration
        self.mutex = threading.RLock()
        # 连接池
        self._connection_pool = []

        for i in range(self.max_connection):
            self.new_connection()
    
    def clear_connection(self, conn_obj: ConnectionObject):
        '''
        清理连接对象
        '''
        try:
            self.mutex.acquire()
            self._connection_pool.remove(conn_obj)
        finally:
            self.mutex.release()

    def new_connection(self, *args, **kwargs) -> ConnectionObject:
        '''
        创建连接对象，非用户调用
        '''
        raise NotImplementedError()

    @contextmanager
    def one_connection(self):
        '''
        取出一个可用的连接对象
        '''
        selected_conn = None
        try:
            self.mutex.acquire()
            for _conn in self._connection_pool:
                if _conn.check_valid():
                    _conn.take_out()
                    selected_conn = _conn
                    break
                else:
                    if _conn.need_clear():
                        self.clear_connection(_conn)
            # 连接池没有取用到合适的连接对象
            if not selected_conn:
                _new_conn = self.new_connection()
                _new_conn.take_out()
                selected_conn = _new_conn
        finally:
            self.mutex.release()

            yield selected_conn

            # 清理连接池
        try:
            self.mutex.acquire()
            selected_conn.put_back()
            if selected_conn.need_clear():
                self.clear_connection(selected_conn)
                print("close conn")
        finally:
            self.mutex.release()

class Neo4jConnection(GmConnectionPool):

    def __init__(self, host: str, user:str, password: str):
        self.host = host
        self.user = user
        self.password = password
        super(Neo4jConnection, self).__init__()

    def new_connection(self):
        _neo4j_conn = Graph(self.host, auth=(self.user, self.password))
        _conn_obj = ConnectionObject(_neo4j_conn, self.duration)
        self._connection_pool.append(_conn_obj)
        return _conn_obj