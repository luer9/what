# 版本
* python 3.6.4
* vue2
* vue/cli 4.5.8
* Django 2.2.16
* neo4j 4.2.2
* d3 3.5.17
    * 查询版本: npm ls xxx -g
    * pip已经安装过的包 pip list
# 开发工具
* vscode (主要)
* pycharm 2020.1.3 测试用
* webstorm 2019.3.5 测试前端用
# 创建项目
* 前端
    * vue init webpack appfront(名字)
* 后端
    * django-admin startproject myapp(名字)
# 部署
* cd myproject
* 前端
    * npm install  (下载依赖，运行一次即可)
    * npm run dev
* 后端
    * python manage.py runserver  (启动)
# 时间
## 2021-02-09
> 之前都在前端搭建……，不算难，浪费了很长时间。
> 自我反思中……
## 2021-02-09
* 解决跨域问题
    * localhost 和 127.0.0.1 的问题！！！（主要是这个问题！！！）
    * 以及采用django-cors....一个插件来解决跨域问题（这个比较好配置）
* 实现了前后端交互

## 测试连接数据库
* testConnect.py 连接neo4j数据库、测试节点、测试关系 ✔
## 建立知识图谱
* 根据清洗过的数据，依照QASystem项目中build_medicalgraph.py建立知识图谱
* 缕清musicKG中的节点和关系
    * 节点
        * 音乐
            * 艺术家 artists
            * 乐器 musicInstruments
            * 乐理 musicTheroies  (music theroy)
            * 音乐类型 musicTypes
            * 音乐学 musicology
            * 艺术高校（中国传媒大学）musicColleges
            * 音乐作品 musicWorks
    * 关系
        * 艺术家-音乐作品：代表作品  rels_representativeWorks
        * 艺术家-艺术高校：毕业高校  rels_graduatedCollege
        * 艺术家-音乐类型：音乐风格  rels_musicstyle
        * 艺术家-艺术家：组合成员 （少女时代例子） rels_groupMember
        * 艺术家-乐器：演奏          rels_play
        * 乐器-音乐作品：代表作品    rels_representativeWork
        * 乐器-艺术家：代表人物      rels_representativeFigure
        * 乐器-音乐学：应用学科  （钢琴例子） rels_appliedScience
        * 乐器-音乐类型：适用类型 （吉他例子）rels_applicableMusicType
        * 乐器-乐器：分类 （吉他例子，isA的关系？） rels_classfication
        * 音乐类型-艺术家：代表人物   rels_representativeFigure
        * 音乐类型-乐器：代表乐器     rels_representativeMusicInstrument
        * 音乐类型-音乐作品：典型作品（代表作品） rels_representativeWork
        * 音乐学-音乐学科：学科设置   rels_subjectSetting
    * 暂时想到这么多
* 2021-02-18 
    * 完善build_musicKG.py 中 read_nodes函数 
    * 已经分离出节点 和 关系
    * export_data() 存在bug 但目前不重要  ----> 已解决  是返回值的问题  注意：python返回值不能换行……
* 2021-02-19
    * export_data() 存在bug 但目前不重要  ----> 已解决  是返回值的问题  注意：python返回值不能换行……
    * 得到所需的每个节点的属性信息 get_infor()
    * 创建知识图谱实体节点类型 create_graphnodes
        * 这里遇到了一个问题就是 创建节点数据之后，节点上没有显示姓名
            * 原因是属性太多，brower不知道选用那个显示，需要自己去指定
            * https://blog.csdn.net/w5688414/article/details/98864084

* 2021-02-20 
    * 计划建立关系，不难，然后看知识表示学习。。。。
    * 关系建立成功，neo4j数据建立成功

## 2021-02-22
* 前端升级
    * 添加了知识图谱总览页面 
    * 添加了导航  nav.vue
## 2021-02-23

* 显示知识图谱
    * 使用的技术是 d3
    * 添加的页面 all.vue  向后端  getnodes  getrels 请求数据
    * 参考：
        * http://www.molapages.xyz/molablog/page/72
        * https://github.com/molamolaxxx/KGView
        * http://www.molapages.xyz/KGView/
    * 遇到的问题：因为数据太多，页面卡顿，暂时不知道怎么解决