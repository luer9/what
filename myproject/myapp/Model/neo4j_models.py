# -*- coding: utf-8 -*-
from py2neo import Graph,Node,Relationship,NodeMatcher

class Neo4j_Handle():
  graph = None
  matcher = None
  def __init__(self):
    print("Neo4j Init ...")

  def connectNeo4j(self):
    self.graph = Graph("http://127.0.0.1:7474", username="neo4j", password="52151")

  def searchall(self):
    answer = self.graph.run("MATCH (n1)- [rel] -> (n2) RETURN n1.name as source,n2.name as target,rel.name as rela").data()
    return answer
  
  # 返回所有的节点name和其标签
  def getnodes(self):
    answer = self.graph.run("match (n) return distinct labels(n) as type,n.name as name").data()
    return answer 