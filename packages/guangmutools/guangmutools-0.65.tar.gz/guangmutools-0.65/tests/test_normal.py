# -*- encoding: utf-8 -*-
'''
@文件    :test_normal.py
@说明    :
@时间    :2021/02/23 14:16:46
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import unittest
from pprint import pprint

from guangmutools.base import project_root_path
from guangmutools.base import write_params_to_localfile, read_params_from_localfile

from guangmutools.dbutils.connection_pool import Neo4jConnection
from guangmutools.dbutils.graph_db import NeoNodeHelper

class TestNormalFuncs(unittest.TestCase):
    def setUp(self):
        self.neo4j_conn = Neo4jConnection("bolt://121.14.8.80:7687", "neo4j", "Gm123456")

    def testProjectrootpath(self):
        print(project_root_path('f:\\work\\guangmu\\ms_sensitive_check\\controllers\\utils\\admin_helpers.py', 'ms_sensitive_check', 'abc', 'def'))

    def testWriteParamsFile(self):
        ret_check = write_params_to_localfile("d:/ttt.log", {"name": "刘德华", "age": 32, "nick": "Andy Lau"})
        self.assertTrue(ret_check)

    def testReadParamsFile(self):
        data = read_params_from_localfile("d:/ttt.log")

        pprint(data)
        self.assertTrue(isinstance(data, dict))

    def testNeo2pyMatcher(self):
        helper = NeoNodeHelper(self.neo4j_conn)
        pprint(helper.FindNode("id_card"))

    def testNeo2pyRawrun(self):
        helper = NeoNodeHelper(self.neo4j_conn)
        pprint(helper.RawExecute("MATCH (c)  RETURN c LIMIT 50"))

    def testNeo2pyCreate(self):
        helper = NeoNodeHelper(self.neo4j_conn)
        pprint(helper.CreateNode('account', 'caimmy', vip=1, grade=90))

    def testNeo2pyUpdate(self):
        # UpdateNode
        helper = NeoNodeHelper(self.neo4j_conn)
        nodes = helper.RawExecute("MATCH (c) WHERE c.name='caimmy' RETURN c")
        helper.UpdateNode(nodes[0], vip=0, study="yes")

    def testBuildRelationship(self):
        helper = NeoNodeHelper(self.neo4j_conn)
        node_1 = helper.EnsureNode("account", "caimmy")
        node_2 = helper.EnsureNode("email", "caimmy@hotmail.com")
        helper.BuildRelationship("email", node_1, node_2, another="caimmy@sohu.com", worker="caimmy@kingsoft.com")

    def testQueryRelationship(self):
        helper = NeoNodeHelper.Instance("bolt://121.14.8.80:7687", "neo4j", "Gm123456")
        r = helper.RawExecute("MATCH (c)-[r]->(d) WHERE c.name='caimmy' DELETE r")
        # if r:
        #     helper.DeleteNode(r[0].get("r"))
        pprint(r)