from django.http import HttpResponse
from utils.pre_load import neo4jconn
import json
# https://www.runoob.com/django/django-views-fbv-cbv.html
def musicQA(request):
    issue = request.GET.get("issue")
    ans = "这是答案！" 
    return HttpResponse(ans)

def getrels(request):
    print("来了没！！！！！！！")
    ctx = {}
    db = neo4jconn
 
    searchResult = {}
    # 整个知识图谱
    searchResult = db.searchall()
    print("--->", searchResult)
        # searchResult = sortDict(searchResult)
    searchResult = json.dumps(searchResult, ensure_ascii=False)
        # print(json.loads(json.dumps(searchResult)))
    return HttpResponse(searchResult)

def getnodes(request):
    print("---------->得到所有的节点name和标签",)
    ctx = {}
    db = neo4jconn

    searchRes = {}

    searchRes = db.getnodes()
    print("-----> ans: ", searchRes)
    searchRes = json.dumps(searchRes, ensure_ascii=False)
        # print(json.loads(json.dumps(searchResult)))
    return HttpResponse(searchRes)