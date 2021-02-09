# 版本
    * python 3.6.4
    * vue2
    * vue/cli 4.5.8
    * Django 2.2.16
    * neo4j 4.2.2
# 开发工具
    * vscode (主要)
    * pycharm 2020.1.3 测试用
    * webstorm 2019.3.5 测试用
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