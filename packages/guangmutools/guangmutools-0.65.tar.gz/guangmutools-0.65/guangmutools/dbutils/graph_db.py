# -*- encoding: utf-8 -*-
'''
@文件    :graph_db.py
@说明    :
@时间    :2021/05/06 14:46:26
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''
import time
from py2neo import Node, Relationship, Graph
from py2neo.matching import NodeMatcher

from .connection_pool import Neo4jConnection

class NeoNodeHelper:

    @staticmethod
    def Instance(host: str, user: str, pwd: str):
        '''
        初始化辅助实例
        '''
        return NeoNodeHelper(Neo4jConnection(host, user, pwd))

    def __init__(self, conn: Neo4jConnection):
        self.conn_handler = conn

    def RawExecute(self, cypher: str):
        '''
        直接执行cypher语句
        :param cypher str
        '''
        res = None
        with self.conn_handler.one_connection() as _conn:
            cursor = _conn.handler.run(cypher)
            try:
                res = [n for n in cursor]
            except Exception as e:
                ret = None
        return res

    def NodeMatcher(self, label: str, *args, **kwargs):
        '''
        查找节点
        :param label str 节点的类型
        '''
        with self.conn_handler.one_connection() as _conn:
            nodes_finder = NodeMatcher(_conn.handler)
            _node = nodes_finder.match(catalog, **kwargs).first()
            return _node
    
    def CreateNode(self, label: str, name: str, **kwargs):
        '''
        创建一个节点
        :param label str 节点标签
        :param name str 节点的名称属性
        '''
        with self.conn_handler.one_connection() as _conn:
            _node = Node(label, name=name, **kwargs)
            _conn.handler.create(_node)
            return _node if _node.identity else None

    def EnsureNode(self, label: str, name: str, **kwargs):
        '''
        确保一个节点存在
        :return Node
        '''
        _cur_node = None
        _match_cypher = f"MATCH (c:{label}) WHERE c.name='{name}' RETURN c LIMIT 1"
        nodes = self.RawExecute(_match_cypher)
        if not nodes:
            _cur_node = self.CreateNode(label, name, **kwargs)
        else:
            _cur_node = nodes[0].get("c")
        return _cur_node

    def MergeNode(self, label: str, name: str, **kwargs):
        '''
        合并一个节点（更新）
        该方法基本可以不用
        :return Node
        '''
        with self.conn_handler.one_connection() as _conn:
            _node = Node(label, name=name, **kwargs)
            _conn.handler.merge(_node, label, "name")
            return _node


    def DeleteNode(self, node: Node):
        '''
        删除一个节点
        '''
        with self.conn_handler.one_connection() as _conn:
            _conn.handler.delete(node)

    def UpdateNode(self, node: Node, **kwargs):
        '''
        更新节点
        '''
        with self.conn_handler.one_connection() as _conn:
            node.update(kwargs)
            _conn.push(node)
            return node

    # --- relationship operations
    def BuildRelationship(self, rel_label, node_from, node_to, **kwargs):
        with self.conn_handler.one_connection() as _conn:
            RELS = Relationship.type(rel_label)
            _conn.handler.merge(RELS(node_from, node_to, **kwargs), rel_label, "name")

    def RelationshipExists(self, node_from: Node, node_to: Node, rel_label: str) -> bool:
        '''
        判断关系是否存在
        :param node_from Node 起始节点
        :param node_to Node 结束节点
        :para rel_label str 关系标签
        :return bool
        '''
        with self.conn_handler.one_connection() as _conn:
            rel = Relationship(node_from, rel_label, node_to)
            return _conn.handler.exists(rel)