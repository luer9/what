# -*- coding: utf-8 -*-
from Model.neo4j_models import Neo4j_Handle

import os


# 初始化neo4j
def init_neo4j():
    neo4jconn = Neo4j_Handle()
    print("-->", neo4jconn)
    neo4jconn.connectNeo4j()
    return neo4jconn


# 初始化
neo4jconn = init_neo4j()