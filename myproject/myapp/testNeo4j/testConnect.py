# 测试连接 neo4j
# Author：Luer
# time：2021-02-14
from py2neo import Graph, Node, Relationship

# 连接 neo4j 输入地址、用户名、密码
test_graph = Graph(
    "http://localhost:7474",
    username = "neo4j",
    password = "52151"
)

# 测试添加节点
test_node_1 = Node("艺术家", 名字 = "周杰伦")
test_node_2 = Node("歌曲", 名字 = "稻香")
test_graph.create(test_node_1)
test_graph.create(test_node_2)

# 建立节点之间的关系

node_1_sing_node_2 = Relationship(test_node_1, "唱", test_node_2)
node_1_sing_node_2['传唱度'] = 0.99
test_graph.create(node_1_sing_node_2)

# 成功！