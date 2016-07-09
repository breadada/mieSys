# mieSys
最小广告系统

## 平台环境

* Centos 7
* Python2.7(numpy, scipy, sklearn, pandas; MySQLdb, flask)
* Nginx 1.6.3
* uWSGI
* Mysql

## 功能模块

* Cookie分发：标记当前用户，作为本站唯一标识

* 日志系统：记录用户访问日志和点击日志等

* 行为定向：根据用户点击记录确定用户的性别和兴趣标签

* 广告检索：根据用户标签，去广告库检索相关广告

* CTR预估：对召回的广告进行点击率预估，按照点击率从高到低的顺序将广告放在相应广告位上。

## 业务逻辑：

<center>![主页](http://7xqgba.com1.z0.glb.clouddn.com/64.jpg)</center>

用户第一次访问系统时，将看到上述页面，与此同时将获得一个服务器分发的Cookie。随后，用户在网站上所有点击行为都将被记录，供后期离线程序使用。

<center>![主页](http://7xqgba.com1.z0.glb.clouddn.com/62.jpg)</center>

当用户第二次访问系统时，将看到上述页面，此时页面广告是根据用户点击历史所推荐并排序的结果。

## 运行方法

* 启动Flask
> python server.p runserver --host 0.0.0.0

* 启动uWSGI
> uwsgi config.ini

* 启动离线计算
> python run.py


